from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from scripts.piece import *
from scripts.rules import MoveRules
from scripts.square import ChessSquare

class ChessBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess Board')
        self.setFixedSize(480, 480)
        
        # Create main widget without margins
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create grid layout with zero spacing
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(self.layout)
        
        # Set layout properties to remove any automatic spacing
        central_widget.setContentsMargins(0, 0, 0, 0)
        
        # Create board squares
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        light_color = QColor(255, 206, 158)
        dark_color = QColor(209, 139, 71)
        
        for row in range(8):
            for col in range(8):
                color = light_color if (row + col) % 2 == 0 else dark_color
                square = ChessSquare(row, col, color)
                self.squares[row][col] = square
                self.layout.addWidget(square, row, col)
                
                # Add pieces
                piece = None
                if row == 1:  # Black pawns
                    piece = Pawn('black')
                elif row == 6:  # White pawns
                    piece = Pawn('white')
                elif row in [0, 7]:  # Other pieces
                    color = 'black' if row == 0 else 'white'
                    if col in [0, 7]:
                        piece = Rook(color)
                    elif col in [1, 6]:
                        piece = Knight(color)
                    elif col in [2, 5]:
                        piece = Bishop(color)
                    elif col == 3:
                        piece = Queen(color)
                    elif col == 4:
                        piece = King(color)
                
                if piece:
                    piece.setParent(square)
                    square.piece = piece
        
        # Initialize game state
        self.selected_piece = None
        self.selected_square = None
        self.highlighted_squares = []
        self.current_player = 'white'
    
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
                # Remove captured piece if any
                if square.piece:
                    square.piece.setParent(None)
                    square.piece = None
                
                # Move piece to new square
                old_square = self.selected_square
                old_square.piece = None
                square.piece = self.selected_piece
                self.selected_piece.setParent(square)
                
                # Mark piece as moved
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
                
                # Show valid moves for new selection
                valid_moves = MoveRules.get_valid_moves(square.piece, 
                                                      (square.row, square.col), 
                                                      self)
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

