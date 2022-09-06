from operator import index
import pandas as pd
import numpy as np
import time



'''
EFFECTS: Converts String of numbers to a 2d array sudoku board. 
First index is top left, left to right then top to bottom.
REQUIRES: input must be string, only digits 0-9, and length of 81
'''
def convertStringToBoard(string):
    if isinstance(string, str) and len(string) != 81 and not string.isdigit():
        raise Exception("Error with input string", string)
    board = np.zeros((9,9))
    array = [int(x) for x in string]
    for i in range(9):
        board[i] =  array[i*9:(i+1)*9]
    return board

class Solver():
    # Search Options
    DFS = 0
    BFS = 1
    # Find Next In Priority
    FIRST_ZERO = 0
    MOST_NEIGHBOURING = 1
    MOST_UNIQUE_NEIGHBOURING = 2


    def __init__(self, searchType = 0, findNextPriority = 0, random = 0, enableHeuristics = False):
        self.enableHeuristics = enableHeuristics
        self.searchType = searchType
        self.random = random
        self.setSearch(findNextPriority)

    def setSearch(self, findNextPriority):
        if findNextPriority == self.FIRST_ZERO:
            self.findNext = self.findZero
        elif findNextPriority == self.MOST_NEIGHBOURING:
            self.findNext = self.findIndexWithMostTotal
        elif findNextPriority == self.MOST_UNIQUE_NEIGHBOURING:
            self.findNext = self.findIndexWithMostNumbers

    '''
    EFFECTS:  Checks if array has a duplicate non zero value
    '''
    def checkArray(self, arr):
        arr = arr[arr != 0]
        return len(arr) == len(set(arr))


    def getBoardSection(self, board, i, j):
        lowBound = 3*j
        upperBound = 3 + 3*j
        section = np.concatenate((board[i*3][lowBound:upperBound], 
                                board[i*3+1][lowBound:upperBound], 
                                board[i*3+2][lowBound:upperBound]))
        return section
    
    
    '''
    EFFECTS:  Checks if board is valid and does not have any
    duplicate numbers in each row, columns, and section.
    '''
    def checkBoard(self, board):
        for i in range(9):
            section = self.getBoardSection(board,(i%3),int(i/3))
            if not (self.checkArray(board[:,i]) and self.checkArray(board[i,:]) and self.checkArray(section)):
                return False
        return True

    '''
    EFFECTS: returns tuple of indexes of the first zero or a random zero,
    with probability of self.random.
    First index is top left, left to right then top to bottom. 
    '''
    def findZero(self, board):
        indexes = np.where(board == 0)
        if np.random.rand() < self.random:
            index = np.random.randint(len(indexes[0]))
            return (indexes[0][index], indexes[1][index])
        else:
            return (indexes[0][0], indexes[1][0])
    
    def getListOfAffectingCells(self, board):
        indexes = np.where(board == 0)
        list = []
        for i in range(len(indexes[0])):
            colRowSectionCells = np.concatenate((board[:,indexes[1][i]], board[indexes[0][i],:],
                                        self.getBoardSection(board,int(indexes[0][i]/3), int(indexes[1][i]/3))))
            colRowSectionCells = colRowSectionCells[colRowSectionCells != 0]
            list.append(colRowSectionCells)
        return (list, indexes)

    def findIndexWithMostTotal(self, board):
        list, indexes = self.getListOfAffectingCells(board)
        count = []
        for cells in list:
            count.append(len(cells))
        index = np.argmax(count)
        return (indexes[0][index], indexes[1][index])
    
    def findIndexWithMostNumbers(self, board):
        list, indexes = self.getListOfAffectingCells(board)
        count = []
        for cells in list:
            count.append(len(set(cells)))
        index = np.argmax(count)
        return (indexes[0][index], indexes[1][index])


    def getSections(self, board, func = lambda section: section):
        sections = []
        for j in range(3):
            for i in range(3):
                sections.append(func(self.getBoardSection(board, i, j)))
        return sections

    def getPossibleLocations(self, board):
        diff = lambda section: np.setdiff1d(range(1,10), section)
        sectionsDiffs = self.getSections(board, diff)
        indexes = np.where(board == 0)
        possibleLocations = []
        for i in range(3):
            for j in range(3):
                notInSection = sectionsDiffs[i + 3*j]
                for num in notInSection:
                    availableSpots = []
                    for index in range(len(indexes[0])):
                        indexI = indexes[0][index]
                        indexJ = indexes[1][index]
                        if i*3 <= indexI < 3 + i*3 and j*3 <= indexJ < 3 + j*3:
                            newBoard = np.copy(board)
                            newBoard[indexI][indexJ] = num
                            if self.checkBoard(newBoard):
                                availableSpots.append((indexI,indexJ))
                    possibleLocations.append((num, availableSpots))
        return possibleLocations

    def fillBoard(self, board):
        # !!! loop fill board? how often can it solve boards?
        possibleLocations = self.getPossibleLocations(board)
        for locations in possibleLocations:
            if len(locations[1]) == 1:
                self.pastBoards.append(np.copy(board))
                board[locations[1][0][0]][locations[1][0][1]] = locations[0]
        return board


    '''
    EFFECTS: checks if board in complete and has a value in each
    location
    '''
    def gameComplete(self, board):
        indexes = np.where(board == 0)
        return len(indexes[0]) == 0

    '''
    EFFECTS: takes list of boards remove one at index location
    and appends all possible next boards to list. (see find zero
    for location of next added value)
    '''
    def getNextBoards(self, bst, index):
        board = bst.pop(index)
        if self.enableHeuristics:
            board = self.fillBoard(board)
            if self.gameComplete(board):
                bst.append(board)
                return bst
        self.pastBoards.append(np.copy(board))
        index = self.findNext(board)
        for i in range(1,10):
            board[index] = i
            if self.checkBoard(board):
                bst.append(np.copy(board))
        return bst

    '''
    EFFECTS: solves given board using either BFS or DFS
    '''
    def solveBoard(self, board):
        self.pastBoards = [np.copy(board)]
        bst = [np.copy(board)]
        if self.searchType == self.DFS:
            while(not self.gameComplete(bst[len(bst) - 1])):
                bst = self.getNextBoards(bst, len(bst) - 1)
            self.pastBoards.append(np.copy(bst[len(bst) - 1]))  
        if self.searchType == self.BFS:
            while(not self.gameComplete(bst[0])):
                bst = self.getNextBoards(bst, 0)
            self.pastBoards.append(np.copy(bst[0]))  
        return bst[len(bst) - 1]


def getResults(data, solver, solverType):
    start_time = time.time()
    for i in range(len(data)):
        bst = solver.solveBoard(convertStringToBoard(data["puzzle"][i]))
    end_time = time.time()
    print(solverType)
    print("Average Completion Time:",(end_time - start_time)/AMOUNT)


if __name__ == "__main__":
    AMOUNT = 1
    data = pd.read_csv("data/sudoku.csv", nrows=AMOUNT)
    
    #solver = Solver(random=0.0, findNextPriority= Solver.FIRST_ZERO, searchType= Solver.DFS)
    #getResults(data, solver, "Depth First Search Solver with First Zero Search:" )

    #solver = Solver(random=0.0, findNextPriority= Solver.FIRST_ZERO, searchType= Solver.BFS)
    #getResults(data, solver, "Breadth First Search Solver with First Zero Search:" )

    #solver = Solver(random=0.0, findNextPriority= Solver.MOST_NEIGHBOURING, searchType= Solver.DFS)
    #getResults(data, solver, "Depth First Search Solver with Most Neighbouring Numbers:" )

    #solver = Solver(random=0.0, findNextPriority= Solver.MOST_UNIQUE_NEIGHBOURING, searchType= Solver.DFS)
    #getResults(data, solver, "Depth First Search Solver with Most Unique Neighbouring Numbers:" )

    #solver = Solver(random=0.0, findNextPriority= Solver.FIRST_ZERO, searchType= Solver.DFS, enableHeuristics=True)
    #getResults(data, solver, "Depth First Search Solver with First Zero Search and Heuristics:" )

    solver = Solver(random=0.0, findNextPriority= Solver.MOST_NEIGHBOURING, searchType= Solver.DFS, enableHeuristics=True)
    getResults(data, solver, "Depth First Search Solver with Most Neighbouring Numbers and Heuristics:" )

    solver = Solver(random=0.0, findNextPriority= Solver.MOST_UNIQUE_NEIGHBOURING, searchType= Solver.DFS, enableHeuristics=True)
    getResults(data, solver, "Depth First Search Solver with Most Unique Neighbouring Numbers and Heuristics:" )
