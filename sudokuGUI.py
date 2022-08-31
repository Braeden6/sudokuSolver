import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class SudokuSquare(QtWidgets.QPushButton):

    def __init__(self, parent=None, value = 0):
        super().__init__()
        self.parent = parent
        self.value = value


        self.setMinimumSize(50,50)
        self.setStyleSheet("background-color: white; border-color: black; ")

        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        if self.value != 0:
            self.text.setText(str(value))
        self.layout = QtWidgets.QVBoxLayout()
        
        self.setLayout(self.layout)
        self.layout.addWidget(self.text)

        self.clicked.connect(self.squareSelected)

    @QtCore.Slot()
    def squareSelected(self):
        self.parent.childClicked(self)

    def setValue(self, value):
        self.text.setText(value)
    
    


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.board = []
        self.selected = None
        self.layout = QtWidgets.QGridLayout(self)
        for i in range(9):
            self.board.append([])
            for j in range(9):
                self.board[i].append(SudokuSquare(self, i*j%4))
                self.layout.addWidget(self.board[i][j],i,j)
        self.setLayout(self.layout)

        self.installEventFilter(self)
    
    def childClicked(self, selected):
        if self.selected != None:
            self.selected.setStyleSheet("background-color: white;")
        self.selected = selected
        selected.setStyleSheet("background-color: grey;")
    
    def eventFilter(self, widget, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            if (event.key() > 48 and event.key() < 58):
                self.selected.setValue(str(event.key() - 48))
        



        

        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(500,500)
    widget.show()

    sys.exit(app.exec())