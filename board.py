from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from piece import *
from rules import MoveRules

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
        self.setMinimumSize(60, 60)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw base square
        painter.fillRect(self.rect(), self.current_color)
        
        if self.is_selected:
            # Draw thick green border for selected square
            pen = QPen(QColor(76, 175, 80), 3)  # Thicker green border
            painter.setPen(pen)
            painter.drawRect(1, 1, self.width()-2, self.height()-2)
        
        elif self.is_highlighted:
            # Draw green border
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

class ChessBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess Board')
        self.setGeometry(100, 100, 600, 600)
        
        # Create main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout()
        central_widget.setLayout(self.layout)
        
        # Create board squares
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.highlighted_squares = []
        
        light_color = QColor(255, 206, 158)
        dark_color = QColor(209, 139, 71)
        
        # Create squares and initial piece setup
        for row in range(8):
            for col in range(8):
                color = light_color if (row + col) % 2 == 0 else dark_color
                square = ChessSquare(row, col, color)
                self.squares[row][col] = square
                self.layout.addWidget(square, row, col)
                
                # Add initial pieces
                if row == 1:  # Black pawns
                    square.piece = Pawn('black', square)
                elif row == 6:  # White pawns
                    square.piece = Pawn('white', square)
                elif row in [0, 7]:  # Other pieces
                    piece_color = 'black' if row == 0 else 'white'
                    if col in [0, 7]:
                        square.piece = Rook(piece_color, square)
                    elif col in [1, 6]:
                        square.piece = Knight(piece_color, square)
                    elif col in [2, 5]:
                        square.piece = Bishop(piece_color, square)
                    elif col == 3:
                        square.piece = Queen(piece_color, square)
                    elif col == 4:
                        square.piece = King(piece_color, square)
                
                if square.piece:
                    square.piece.mousePressEvent = lambda e, s=square: self.square_clicked(s)
        
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.current_player = 'white'  # Track whose turn it is
        self.selected_square = None    # Track selected square
    
    def get_piece_at(self, row, col):
        """Helper method to get piece at given position"""
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.squares[row][col].piece
        return None

    def filter_valid_moves(self, piece, current_pos, moves):
        filtered_moves = []
        row, col = current_pos

        # For pieces that move in lines (Queen, Rook, Bishop)
        if piece.piece_type in ['queen', 'rook', 'bishop']:
            directions = []
            if piece.piece_type in ['queen', 'rook']:
                directions.extend(DIRECTIONS['STRAIGHT'])
            if piece.piece_type in ['queen', 'bishop']:
                directions.extend(DIRECTIONS['DIAGONAL'])

            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    target_piece = self.get_piece_at(r, c)
                    if target_piece is None:
                        filtered_moves.append((r, c))
                    else:
                        if target_piece.color != piece.color:
                            filtered_moves.append((r, c))
                        break
                    r, c = r + dr, c + dc

        # For Knight
        elif piece.piece_type == 'knight':
            for r, c in moves:
                target_piece = self.get_piece_at(r, c)
                if target_piece is None or target_piece.color != piece.color:
                    filtered_moves.append((r, c))

        # For Pawn
        elif piece.piece_type == 'pawn':
            direction = -1 if piece.color == 'white' else 1
            
            # Forward moves
            r = row + direction
            if self.get_piece_at(r, col) is None:
                filtered_moves.append((r, col))
                # Initial two-square move
                if not piece.has_moved:
                    r = row + (2 * direction)
                    if self.get_piece_at(r, col) is None:
                        filtered_moves.append((r, col))
            
            # Diagonal captures
            for dc in [-1, 1]:
                r, c = row + direction, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    target_piece = self.get_piece_at(r, c)
                    if target_piece and target_piece.color != piece.color:
                        filtered_moves.append((r, c))

        return filtered_moves

    def square_clicked(self, square):
        if self.selected_piece:
            # Get all valid moves for the selected piece
            valid_moves = MoveRules.get_valid_moves(self.selected_piece, 
                                                  (self.selected_square.row, self.selected_square.col), 
                                                  self)
            
            # Check if clicked square is a valid move
            if (square.row, square.col) in valid_moves:
                # Move the piece
                old_square = self.selected_piece.parent()
                
                # Remove piece from old square
                old_square.piece = None
                
                # Remove captured piece if any
                if square.piece:
                    square.piece.setParent(None)
                
                # Move piece to new square
                square.piece = self.selected_piece
                self.selected_piece.setParent(square)
                self.selected_piece.has_moved = True
                
                # Switch turns
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                
                # Clear selection and highlights
                self.clear_highlights()
                self.selected_piece = None
                self.selected_square = None
                
            elif square.piece and square.piece.color == self.current_player:
                # Select new piece
                self.clear_highlights()
                self.selected_piece = square.piece
                self.selected_square = square
                square.select_square()
                self.highlighted_squares.append(square)
                
                # Show valid moves
                for row, col in valid_moves:
                    target_square = self.squares[row][col]
                    target_square.highlight_move()
                    self.highlighted_squares.append(target_square)
        
        elif square.piece and square.piece.color == self.current_player:
            # First piece selection
            self.selected_piece = square.piece
            self.selected_square = square
            square.select_square()
            self.highlighted_squares.append(square)
            
            # Show valid moves
            valid_moves = MoveRules.get_valid_moves(square.piece, 
                                                  (square.row, square.col), 
                                                  self)
            
            for row, col in valid_moves:
                target_square = self.squares[row][col]
                target_square.highlight_move()
                self.highlighted_squares.append(target_square)

    def clear_highlights(self):
        for square in self.highlighted_squares:
            square.reset_color()
        self.highlighted_squares.clear()
        self.selected_piece = None

