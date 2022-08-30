import pandas as pd
#from sklearn.neural_network import MLPClassifier
import numpy as np
import time



# data = pd.read_csv("sudoku.csv")


board = "070000043040009610800634900094052000358460020000800530080070091902100005007040802"
answer = "679518243543729618821634957794352186358461729216897534485276391962183475137945862"





'''
EFFECTS: Converts String of numbers to a 2d array sudoku board. 
First index is top left of board and last index is bottom right
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


def checkArray(arr):
    arr = arr[arr != 0]
    return len(arr) == len(set(arr))

def checkBoard(board):
    for i in range(9):
        lowBound = 3*int(i/3)
        upperBound = 3 + 3*int(i/3)
        section = np.concatenate((board[(i%3)*3][lowBound:upperBound], board[(i%3)*3+1][lowBound:upperBound], board[(i%3)*3+2][lowBound:upperBound]))
        if not (checkArray(board[:,i]) and checkArray(board[i,:]) and checkArray(section)):
            return False
    return True

def findZero(board):
    indexes = np.where(board == 0)
    if len(indexes[0]) == 0:
        return False
    return (indexes[0][0], indexes[1][0])

def getNextBoards(bst, index):
    board = bst.pop(index)
    index = findZero(board)
    for i in range(1,10):
        board[index] = i
        if checkBoard(board):
            bst.append(np.copy(board))
    return bst

# 0 = depth first search
# 1 = breadth first search
def solveBoard(board, searchType):
    bst = [np.copy(board)]
    if searchType == 0:
        while(findZero(bst[len(bst) - 1]) != False):
            bst = getNextBoards(bst, len(bst) - 1)
    if searchType == 1:
        while(findZero(bst[0]) != False):
            bst = getNextBoards(bst, 0)
    return bst[len(bst) - 1]
    
AMOUNT = 10
data = pd.read_csv("sudoku.csv", nrows=AMOUNT)


start_time = time.time()
differentSolutions = 0

for i in range(AMOUNT):
    solverAnswer = solveBoard(convertStringToBoard(data["puzzle"][i]), 0)
    if not np.array_equal(solverAnswer, convertStringToBoard(data["solution"][i])):
        differentSolutions += 1

end_time = time.time()

print("Depth First Search Solver:" )
print("Average Completion Time:",(end_time - start_time)/AMOUNT)
print("Amount of different solutions:", differentSolutions)

start_time = time.time()
differentSolutions = 0

for i in range(AMOUNT):
    solverAnswer = solveBoard(convertStringToBoard(data["puzzle"][i]), 1)
    if not np.array_equal(solverAnswer, convertStringToBoard(data["solution"][i])):
        differentSolutions += 1

end_time = time.time()

print("Breadth First Search Solver:" )
print("Average Completion Time:",(end_time - start_time)/AMOUNT)
print("Amount of different solutions:", differentSolutions)
