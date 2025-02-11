from scripts.constants import BOARD_SIZE
from scripts.rules import MoveRules

class GameState:
    @staticmethod
    def find_king(board, color):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece.piece_type == 'king' and piece.color == color:
                    return (row, col)
        return None

    @staticmethod
    def is_check(board, color):
        king_pos = GameState.find_king(board, color)
        if not king_pos:
            return False

        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == opponent_color:
                    valid_moves = MoveRules.get_valid_moves(piece, (row, col), board)
                    if king_pos in valid_moves:
                        return True
        return False

    @staticmethod
    def is_checkmate(board, color):
        if not GameState.is_check(board, color):
            return False

        # Try all possible moves to see if any can get out of check
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == color:
                    valid_moves = MoveRules.get_valid_moves(piece, (row, col), board)
                    for move in valid_moves:
                        # Try move and see if still in check
                        if not GameState.would_be_in_check(board, piece, (row, col), move):
                            return False
        return True

    @staticmethod
    def is_stalemate(board, color):
        if GameState.is_check(board, color):
            return False

        # Check if any legal move exists
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == color:
                    valid_moves = MoveRules.get_valid_moves(piece, (row, col), board)
                    for move in valid_moves:
                        if not GameState.would_be_in_check(board, piece, (row, col), move):
                            return False
        return True

    @staticmethod
    def would_be_in_check(board, piece, from_pos, to_pos):
        # Simulate move and check if it results in check
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Store current state
        original_piece = board.get_piece_at(to_row, to_col)

        # Make temporary move
        board.squares[to_row][to_col].piece = piece
        board.squares[from_row][from_col].piece = None

        # Check if in check
        in_check = GameState.is_check(board, piece.color)

        # Restore original position
        board.squares[from_row][from_col].piece = piece
        board.squares[to_row][to_col].piece = original_piece

        return in_check

    @staticmethod
    def get_defensive_moves(board, color):
        """Get all possible moves that can get out of check"""
        defensive_moves = []
        king_pos = GameState.find_king(board, color)
        if not king_pos:
            return defensive_moves

        # For each piece of the defending color
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == color:
                    # Get all valid moves for this piece
                    valid_moves = MoveRules.get_valid_moves(piece, (row, col), board)
                    # Filter moves that would get out of check
                    for move in valid_moves:
                        if not GameState.would_be_in_check(board, piece, (row, col), move):
                            defensive_moves.append((piece, (row, col), move))
        
        return defensive_moves

    @staticmethod
    def get_legal_defensive_moves(board, color):
        """Get only the legal moves that can get out of check"""
        legal_moves = []

        # Find all possible defensive moves
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == color:
                    # Get valid moves for this piece
                    valid_moves = MoveRules.get_valid_moves(piece, (row, col), board)
                    # Check which moves actually get out of check
                    for move in valid_moves:
                        if not GameState.would_be_in_check(board, piece, (row, col), move):
                            legal_moves.append(move)

        return legal_moves