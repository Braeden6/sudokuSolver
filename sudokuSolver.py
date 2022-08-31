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
    # constants
    DFS = 0
    BFS = 1

    def __init__(self, random = 0):
        self.random = random

    '''
    EFFECTS:  Checks if array has a duplicate non zero value
    '''
    def checkArray(self, arr):
        arr = arr[arr != 0]
        return len(arr) == len(set(arr))

    '''
    EFFECTS:  Checks if board is valid and does not have any
    duplicate numbers in each row, columns, and section.
    '''
    def checkBoard(self, board):
        for i in range(9):
            lowBound = 3*int(i/3)
            upperBound = 3 + 3*int(i/3)
            section = np.concatenate((board[(i%3)*3][lowBound:upperBound], 
                                    board[(i%3)*3+1][lowBound:upperBound], 
                                    board[(i%3)*3+2][lowBound:upperBound]))
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

    '''
    EFFECTS: checks if board in complete and has a value in each
    location
    '''
    def gameComplete(self, board):
        indexes = np.where(board == 0)
        return len(indexes[0]) != 0

    '''
    EFFECTS: takes list of boards remove one at index location
    and appends all possible next boards to list. (see find zero
    for location of next added value)
    '''
    def getNextBoards(self, bst, index):
        board = bst.pop(index)
        index = self.findZero(board)
        for i in range(1,10):
            board[index] = i
            if self.checkBoard(board):
                bst.append(np.copy(board))
        return bst

    '''
    EFFECTS: solves given board using either BFS or DFS
    '''
    def solveBoard(self, board, searchType):
        bst = [np.copy(board)]
        if searchType == self.DFS:
            while(self.gameComplete(bst[len(bst) - 1])):
                bst = self.getNextBoards(bst, len(bst) - 1)
        if searchType == self.BFS:
            while(self.gameComplete(bst[0])):
                bst = self.getNextBoards(bst, 0)
        return bst[len(bst) - 1]


if __name__ == "__main__":
    AMOUNT = 20
    data = pd.read_csv("data/sudoku.csv", nrows=AMOUNT)

    solver = Solver(0.1)

    start_time = time.time()
    for i in range(AMOUNT):
        solverAnswer = solver.solveBoard(convertStringToBoard(data["puzzle"][i]), solver.DFS)
    end_time = time.time()

    print("Depth First Search Solver:" )
    print("Average Completion Time:",(end_time - start_time)/AMOUNT)

    start_time = time.time()
    for i in range(AMOUNT):
        solverAnswer = solver.solveBoard(convertStringToBoard(data["puzzle"][i]), solver.BFS)
    end_time = time.time()

    print("Breadth First Search Solver:" )
    print("Average Completion Time:",(end_time - start_time)/AMOUNT)
