from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt
from scripts.event_handler import ChessEventHandler


class ChessSquare(QWidget):
    def __init__(self, row, col, color):
        super().__init__()
        self.row = row
        self.col = col
        self.base_color = color
        self.current_color = color
        self.piece = None
        self.is_highlighted = False
        self.is_selected = False  # New flag for selected square
        self.is_checkmate = False  # New flag for checkmate highlight
        self.setFixedSize(60, 60)
        self.setContentsMargins(0, 0, 0, 0)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Draw base color
        painter.fillRect(self.rect(), self.current_color)
        
        # Draw checkmate/check highlight
        if self.is_checkmate:
            overlay = QColor(255, 0, 0, 120)  # Semi-transparent red
            painter.fillRect(self.rect(), overlay)
        
        # Draw selection/move highlights
        if self.is_selected:
            pen = QPen(QColor(76, 175, 80), 3)
            painter.setPen(pen)
            painter.drawRect(1, 1, self.width()-2, self.height()-2)
        elif self.is_highlighted:
            pen = QPen(QColor(76, 175, 80), 2)
            painter.setPen(pen)
            painter.drawRect(1, 1, self.width()-2, self.height()-2)
            
            # Draw green circle in center
            painter.setBrush(QColor(76, 175, 80, 120))
            painter.setPen(Qt.NoPen)
            circle_size = min(self.width(), self.height()) // 3
            x = (self.width() - circle_size) // 2
            y = (self.height() - circle_size) // 2
            painter.drawEllipse(x, y, circle_size, circle_size)
    
    def highlight_move(self):
        self.is_highlighted = True
        self.update()
    
    def select_square(self):
        self.is_selected = True
        self.update()
        
    def reset_color(self):
        self.is_highlighted = False
        self.is_selected = False
        self.update()

    def mousePressEvent(self, event):
        ChessEventHandler.handle_square_click(self, event)
