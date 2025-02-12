from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from scripts.piece import *
from scripts.rules import MoveRules
from scripts.square import ChessSquare
from scripts.constants import BOARD_SIZE
from scripts.game_state import GameState

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
        self.game_over = False
    
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

    def make_move(self, target_square):
        # Remove captured piece if any
        if target_square.piece:
            target_square.piece.deleteLater()
            target_square.piece = None

        # Move piece to new square
        old_square = self.selected_square
        old_square.piece = None
        target_square.piece = self.selected_piece
        self.selected_piece.setParent(target_square)
        
        # Mark piece as moved
        self.selected_piece.has_moved = True
        
        # Switch turns
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        opponent_color = 'black' if self.current_player == 'white' else 'white'
        
        # Reset all highlights
        self.clear_highlights()
        self.reset_all_squares()
        
        # Check for check/checkmate
        if GameState.is_check(self, self.current_player):
            # Highlight king in check
            king_pos = GameState.find_king(self, self.current_player)
            if king_pos:
                king_square = self.squares[king_pos[0]][king_pos[1]]
                king_square.is_checkmate = True
                king_square.update()
            
            if GameState.is_checkmate(self, self.current_player):
                QMessageBox.information(self, 'Checkmate!', 
                                      f'{opponent_color.capitalize()} wins!')
                self.game_over = True
            else:
                # Only highlight defensive moves using get_defensive_moves
                defensive_moves = GameState.get_defensive_moves(self, self.current_player)
                for _, _, move in defensive_moves:  # Unpack piece, start, end positions
                    target = self.squares[move[0]][move[1]]
                    target.highlight_move()
                    self.highlighted_squares.append(target)
        
        # Clear selection
        self.selected_piece = None
        self.selected_square = None

    def reset_all_squares(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.squares[row][col].is_checkmate = False
                self.squares[row][col].update()

    def square_clicked(self, square):
        if self.game_over:
            return

        # If a piece is already selected
        if self.selected_piece:
            # If we're in check, only allow defensive moves
            if GameState.is_check(self, self.current_player):
                defensive_moves = GameState.get_defensive_moves(self, self.current_player)
                valid_defensive_moves = []
                
                # Find moves for the selected piece
                for piece, start, end in defensive_moves:
                    if piece == self.selected_piece:
                        valid_defensive_moves.append(end)
                
                if (square.row, square.col) in valid_defensive_moves:
                    self.make_move(square)
                elif square.piece and square.piece.color == self.current_player:
                    # Select new piece and show its defensive moves
                    self.clear_highlights()
                    self.selected_piece = square.piece
                    self.selected_square = square
                    square.select_square()
                    self.highlighted_squares.append(square)
                    
                    # Show only this piece's defensive moves
                    for piece, start, end in defensive_moves:
                        if piece == self.selected_piece:
                            target = self.squares[end[0]][end[1]]
                            target.highlight_move()
                            self.highlighted_squares.append(target)
            else:
                # Normal move handling when not in check
                valid_moves = MoveRules.get_valid_moves(self.selected_piece, 
                                                      (self.selected_square.row, self.selected_square.col), 
                                                      self)
                
                if (square.row, square.col) in valid_moves:
                    # Check if move would put/leave player in check
                    if not GameState.would_be_in_check(self, self.selected_piece,
                                                     (self.selected_square.row, self.selected_square.col),
                                                     (square.row, square.col)):
                        self.make_move(square)
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

