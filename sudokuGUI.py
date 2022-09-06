import sys
from turtle import update
import pandas as pd
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui, QtTest
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject
import sudokuSolver
import time

class SudokuSquare(QtWidgets.QPushButton):

    def __init__(self, index, game, widget, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = widget
        self.game = game
        self.index = index

        self.setMinimumSize(50,50)
        self.setStyleSheet("background-color: white; border-color: black; ")

        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.setValue(self.game[self.index])
        self.layout = QtWidgets.QVBoxLayout()
        
        self.setLayout(self.layout)
        self.layout.addWidget(self.text)

        self.clicked.connect(self.squareSelected)

    @QtCore.Slot()
    def squareSelected(self):
        self.parent.childClicked(self)

    def setValue(self, value):
        self.game[self.index] = value
        if self.game[self.index] != 0:
            self.text.setText(str(int(self.game[self.index])))
        else:
            self.text.setText("")
    
    def updateSquare(self, game):
        self.game = game
        self.setValue(self.game[self.index])

    def getIndex(self):
        return self.index
    

class MyWidget(QObject):
    def __init__(self, parent):
        super(MyWidget, self).__init__(parent)
        self.board = []
        self.pastMoves = []
        self.running = False
        self.selected = None
        self.parent = parent 
        self.solver = sudokuSolver.Solver()
        self.timer = QtTest.QTest()

        self.boardLayout = QtWidgets.QGridLayout()
        self.toolBar = QtWidgets.QToolBar()

        mainUIFile = QFile('ui/mainWindow.ui')
        loader = QUiLoader()
        self.ui = loader.load(mainUIFile)

        self.ui.stackedWidget.setCurrentIndex(0)
        

        index = np.random.randint(1000)
        data = pd.read_csv("data/sudoku.csv", skiprows = index, nrows=1, names= ["puzzle", "answer"])
        self.game = sudokuSolver.convertStringToBoard(data["puzzle"][0])

        for i in range(9):
            self.board.append([])
            for j in range(9):
                newLayout = QtWidgets.QGridLayout()
                newLayout.setContentsMargins(0,0,0,0)
                square = getattr(self.ui, "square" + str(i) + str(j))
                self.board[i].append(SudokuSquare((i,j), self.game, square, self))
                newLayout.addWidget(self.board[i][j])
                square.setLayout(newLayout)
        self.board = np.array(self.board)
        self.newGame()      

        
        self.ui.actionNew_Game.triggered.connect(self.newGame)
        self.ui.actionSolver.triggered.connect(self.openSolverBuilder)

        self.ui.widgetBoard.setLayout(self.boardLayout)
        self.ui.mainWidget.installEventFilter(self)
        self.ui.pushButtonUndo.clicked.connect(self.undoMove)
        self.ui.pushButtonSolveGame.clicked.connect(self.solveGame)
    
    def openSolverBuilder(self):
        self.ui.actionNew_Game.setEnabled(False)
        self.ui.actionSolver_BFS.setEnabled(False)
        self.ui.actionSolver_DFS.setEnabled(False)
        self.ui.stackedWidget.setCurrentIndex(1)
    
    def openMainWindow(self):
        self.ui.actionNew_Game.setEnabled(True)
        self.ui.actionSolver_BFS.setEnabled(True)
        self.ui.actionSolver_DFS.setEnabled(True)
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def solveGame(self):
        self.solver = sudokuSolver.Solver(random=0.0, 
                                            findNextPriority=self.ui.comboBoxPriority.currentIndex(), 
                                            searchType=self.ui.comboBoxSearchType.currentIndex(), 
                                            enableHeuristics=self.ui.checkBoxHeuristics.isChecked())
        self.solver.solveBoard(self.game)
        self.openMainWindow()
        for board in self.solver.pastBoards:
            self.updateBoard(board)
            self.timer.qWait(10)

    def updateLeftNumberDisplay(self):
        for i in range(1,10):
            label = getattr(self.ui, "labelLeft" + str(i))
            if np.count_nonzero(self.game == i) == 9:
                label.setText("")
            else:
                label.setText(str(i))

    def updateUI(self, value, square = None):
        if square == None:
            square = self.selected
        square.setValue(value)
        self.updateLeftNumberDisplay()
        
    
    def undoMove(self):
        if len(self.pastMoves) != 0:
            square, num = self.pastMoves.pop()
            self.updateUI(num, square)
    
    def newGame(self):
        index = np.random.randint(1000)
        data = pd.read_csv("data/sudoku.csv", skiprows = index, nrows=1, names= ["puzzle", "answer"])
        self.game = sudokuSolver.convertStringToBoard(data["puzzle"][0])
        self.updateBoard(self.game)
        self.updateLeftNumberDisplay()
        self.pastMoves = []
        
    def updateBoard(self, board):
        for row in self.board:
            for square in row:
                square.updateSquare(board)


    def updateSelectedDisplay(self, cellColour = "white", rowColColour = "white"):
        if self.selected != None:
            for square in self.board[:,self.selected.index[1]]:
                square.setStyleSheet("background-color: " + rowColColour + ";")
            for square in self.board[self.selected.index[0],:]:
                square.setStyleSheet("background-color: " + rowColColour + ";")
            self.selected.setStyleSheet("background-color: " + cellColour + ";")
    
    def childClicked(self, selected):
        self.updateSelectedDisplay()
        self.selected = selected
        self.updateSelectedDisplay("grey" , "light grey")        
    
    def eventFilter(self, widget, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            if (event.key() > 48 and event.key() < 58 and self.selected != None and self.selected.game[self.selected.index] == 0):
                self.pastMoves.append((self.selected, self.selected.game[self.selected.index]))
                self.updateUI(event.key() - 48)
                print(self.solver.checkBoard(self.game))
                print(self.solver.gameComplete(self.game))
                return True
        return super(MyWidget, self).eventFilter(widget, event)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget(app)
    widget.ui.show()
    sys.exit(app.exec())
    
    # widget.ui.resize(500,500)

