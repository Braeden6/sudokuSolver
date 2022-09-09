import unittest
import sys
sys.path.insert(1, "../")
import sudokuSolver
import numpy as np
import pandas as pd



class TestSolver(unittest.TestCase):
    AMOUNT_OF_BOARDS_TESTED = 20

    def test_convertStringToBoard_CorrectInput(self):
        self.assertTrue(np.array_equal(sudokuSolver.convertStringToBoard("0"*81), np.zeros((9,9))), 
            msg="All zero base case for converStringToBoard is incorrect")
        self.assertTrue(np.array_equal(sudokuSolver.convertStringToBoard("9"*81), np.ones((9,9))*9), 
            msg="All nines base case for converStringToBoard is incorrect")
        self.assertTrue(np.array_equal(sudokuSolver.convertStringToBoard(("145"*3 + "367"*3 + "289"*3)*3), 
            np.reshape(np.array([   1,4,5,1,4,5,1,4,5,
                                    3,6,7,3,6,7,3,6,7,
                                    2,8,9,2,8,9,2,8,9,
                                    1,4,5,1,4,5,1,4,5,
                                    3,6,7,3,6,7,3,6,7,
                                    2,8,9,2,8,9,2,8,9,
                                    1,4,5,1,4,5,1,4,5,
                                    3,6,7,3,6,7,3,6,7,
                                    2,8,9,2,8,9,2,8,9]), (9,9))), 
            msg="Bunch of numbers case for converStringToBoard is incorrect")

    def test_convertStringToBoard_IncorrectInput(self):
        with self.assertRaises(Exception): sudokuSolver.convertStringToBoard(45)
        with self.assertRaises(Exception): sudokuSolver.convertStringToBoard("5"*80)
        with self.assertRaises(Exception): sudokuSolver.convertStringToBoard("5"*80+"a")
    
    def test_Solver_DFS_firstZero_noHeuristics(self):
        solver = sudokuSolver.Solver(random=0.0, findNextPriority= sudokuSolver.Solver.FIRST_ZERO, searchType= sudokuSolver.Solver.DFS)
        data = pd.read_csv("../data/sudoku.csv", nrows=self.AMOUNT_OF_BOARDS_TESTED)
        for i in range(len(data)):
            self.assertTrue(np.array_equal(
                    solver.solveBoard(sudokuSolver.convertStringToBoard(data["puzzle"][i])),
                    sudokuSolver.convertStringToBoard(data["solution"][i])),
                    msg= "Failed on board " + str(i))
    
    def test_Solver_BFS_firstZero_noHeuristics(self):
        solver = sudokuSolver.Solver(random=0.0, findNextPriority= sudokuSolver.Solver.FIRST_ZERO, searchType= sudokuSolver.Solver.BFS)
        data = pd.read_csv("../data/sudoku.csv", nrows=self.AMOUNT_OF_BOARDS_TESTED)
        for i in range(len(data)):
            self.assertTrue(np.array_equal(
                    solver.solveBoard(sudokuSolver.convertStringToBoard(data["puzzle"][i])),
                    sudokuSolver.convertStringToBoard(data["solution"][i])),
                    msg= "Failed on board " + str(i))
    
    def test_Solver_BFS_mostNeighbours_noHeuristics(self):
        solver = sudokuSolver.Solver(random=0.0, findNextPriority= sudokuSolver.Solver.MOST_NEIGHBOURING, searchType= sudokuSolver.Solver.BFS)
        data = pd.read_csv("../data/sudoku.csv", nrows=self.AMOUNT_OF_BOARDS_TESTED)
        for i in range(len(data)):
            self.assertTrue(np.array_equal(
                    solver.solveBoard(sudokuSolver.convertStringToBoard(data["puzzle"][i])),
                    sudokuSolver.convertStringToBoard(data["solution"][i])),
                    msg= "Failed on board " + str(i))
    
    def test_Solver_BFS_mostUniqueNeighbours_noHeuristics(self):
        solver = sudokuSolver.Solver(random=0.0, findNextPriority= sudokuSolver.Solver.MOST_UNIQUE_NEIGHBOURING, searchType= sudokuSolver.Solver.BFS)
        data = pd.read_csv("../data/sudoku.csv", nrows=self.AMOUNT_OF_BOARDS_TESTED)
        for i in range(len(data)):
            self.assertTrue(np.array_equal(
                    solver.solveBoard(sudokuSolver.convertStringToBoard(data["puzzle"][i])),
                    sudokuSolver.convertStringToBoard(data["solution"][i])),
                    msg= "Failed on board " + str(i))
    
    def test_Solver_BFS_mostUniqueNeighbours_withHeuristics(self):
        solver = sudokuSolver.Solver(random=0.0, findNextPriority= sudokuSolver.Solver.MOST_UNIQUE_NEIGHBOURING, searchType= sudokuSolver.Solver.BFS, enableHeuristics= True)
        data = pd.read_csv("../data/sudoku.csv", nrows=self.AMOUNT_OF_BOARDS_TESTED)
        for i in range(len(data)):
            self.assertTrue(np.array_equal(
                    solver.solveBoard(sudokuSolver.convertStringToBoard(data["puzzle"][i])),
                    sudokuSolver.convertStringToBoard(data["solution"][i])),
                    msg= "Failed on board " + str(i))

    def test_Solver_BFS_mostUniqueNeighbours_withHeuristics_withRandomness(self):
        solver = sudokuSolver.Solver(random=0.2, findNextPriority= sudokuSolver.Solver.FIRST_ZERO, searchType= sudokuSolver.Solver.BFS, enableHeuristics= True)
        data = pd.read_csv("../data/sudoku.csv", nrows=self.AMOUNT_OF_BOARDS_TESTED)
        for i in range(len(data)):
            self.assertTrue(np.array_equal(
                    solver.solveBoard(sudokuSolver.convertStringToBoard(data["puzzle"][i])),
                    sudokuSolver.convertStringToBoard(data["solution"][i])),
                    msg= "Failed on board " + str(i))
    
    # more test need example: randomness does not work with findNextPriority not First zero




        

if __name__ == "__main__":
    unittest.main()