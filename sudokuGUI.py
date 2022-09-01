import sys
import pandas as pd
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject
import sudokuSolver

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
    
    def updateBoard(self, game):
        self.game = game
        self.setValue(self.game[self.index])

    def getIndex(self):
        return self.index
    
    


class MyWidget(QObject):
    def __init__(self):
        super().__init__()
        self.board = []
        self.selected = None
        self.solver = sudokuSolver.Solver()

        self.boardLayout = QtWidgets.QGridLayout()
        self.toolBar = QtWidgets.QToolBar()

        mainUIFile = QFile('ui/mainWindow.ui')
        loader = QUiLoader()
        self.ui = loader.load(mainUIFile)
        

        data = pd.read_csv("data/sudoku.csv", nrows=1)
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
                

        
        self.ui.actionNew_Game.triggered.connect(self.newGame)

        self.ui.widget.setLayout(self.boardLayout)
        self.ui.centralwidget.installEventFilter(self)
    
    def newGame(self):
        index = np.random.randint(1000)
        data = pd.read_csv("data/sudoku.csv", skiprows = index, nrows=1, names= ["puzzle", "answer"])
        self.game = sudokuSolver.convertStringToBoard(data["puzzle"][0])
        for row in self.board:
            for square in row:
                square.updateBoard(self.game)
    
    def childClicked(self, selected):
        if self.selected != None:
            self.selected.setStyleSheet("background-color: white;")
        self.selected = selected
        selected.setStyleSheet("background-color: grey;")
    
    def eventFilter(self, widget, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            if (event.key() > 47 and event.key() < 58):
                self.selected.setValue(event.key() - 48)
                # !!!
                print(self.solver.checkBoard(self.game))
                return True
        return super(MyWidget, self).eventFilter(widget, event)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.ui.show()
    sys.exit(app.exec())
    
    # widget.ui.resize(500,500)

