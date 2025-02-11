from PyQt5.QtCore import Qt

class ChessEventHandler:
    @staticmethod
    def handle_square_click(square, event):
        if event.button() == Qt.LeftButton:
            board = square.parent().parent()
            board.square_clicked(square)