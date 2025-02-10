from PyQt5.QtWidgets import QApplication
import sys
from scripts.board import ChessBoard


if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = ChessBoard()
    board.show()
    sys.exit(app.exec_())

