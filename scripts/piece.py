from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from scripts.constants import BOARD_SIZE, DIRECTIONS

class ChessPiece(QLabel):
    def __init__(self, piece_type, color, parent=None):
        super().__init__(parent)
        self.piece_type = piece_type
        self.color = color  # 'white' or 'black'
        self.has_moved = False
        
        # Load piece image
        self.load_image()
        
        # Make label draggable
        self.setMouseTracking(True)
    
    def setParent(self, parent):
        super().setParent(parent)
        if parent:
            # Reload and rescale image when parent changes
            self.load_image()
            self.show()  # Make sure piece is visible
    
    def load_image(self):
        # Image path format: 'images/{color}_{piece}.png'
        image_path = f"images/{self.color}_{self.piece_type}.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)
        self.setAlignment(Qt.AlignCenter)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Forward the click to the parent square
            if self.parent():
                self.parent().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        # TODO: Implement drag functionality
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # TODO: Implement piece placement logic
            pass

class Pawn(ChessPiece):
    def __init__(self, color, parent=None):
        super().__init__("pawn", color, parent)
        
    def valid_moves(self, current_pos):
        row, col = current_pos
        moves = []
        direction = -1 if self.color == 'white' else 1
        
        # Forward move
        if 0 <= row + direction < BOARD_SIZE:
            moves.append((row + direction, col))
            
            # Initial two-square move
            if not self.has_moved and 0 <= row + (2 * direction) < BOARD_SIZE:
                moves.append((row + (2 * direction), col))
        
        # Diagonal captures (will be filtered based on opponent pieces later)
        for dcol in [-1, 1]:
            new_row, new_col = row + direction, col + dcol
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                moves.append((new_row, new_col))
                
        return moves

class Rook(ChessPiece):
    def __init__(self, color, parent=None):
        super().__init__("rook", color, parent)
        
    def valid_moves(self, current_pos):
        moves = []
        row, col = current_pos
        
        for dr, dc in DIRECTIONS['STRAIGHT']:
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                moves.append((r, c))
                r, c = r + dr, c + dc
                
        return moves

class Knight(ChessPiece):
    def __init__(self, color, parent=None):
        super().__init__("knight", color, parent)
        
    def valid_moves(self, current_pos):
        moves = []
        row, col = current_pos
        
        for dr, dc in DIRECTIONS['KNIGHT']:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                moves.append((r, c))
                
        return moves

class Bishop(ChessPiece):
    def __init__(self, color, parent=None):
        super().__init__("bishop", color, parent)
        
    def valid_moves(self, current_pos):
        moves = []
        row, col = current_pos
        
        for dr, dc in DIRECTIONS['DIAGONAL']:
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                moves.append((r, c))
                r, c = r + dr, c + dc
                
        return moves

class Queen(ChessPiece):
    def __init__(self, color, parent=None):
        super().__init__("queen", color, parent)
        
    def valid_moves(self, current_pos):
        moves = []
        row, col = current_pos
        
        for dr, dc in DIRECTIONS['STRAIGHT'] + DIRECTIONS['DIAGONAL']:
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                moves.append((r, c))
                r, c = r + dr, c + dc
                
        return moves

class King(ChessPiece):
    def __init__(self, color, parent=None):
        super().__init__("king", color, parent)
        
    def valid_moves(self, current_pos):
        moves = []
        row, col = current_pos
        
        for dr, dc in DIRECTIONS['STRAIGHT'] + DIRECTIONS['DIAGONAL']:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                moves.append((r, c))
                
        return moves