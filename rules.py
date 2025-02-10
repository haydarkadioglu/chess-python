from constants import BOARD_SIZE, DIRECTIONS

class MoveRules:
    @staticmethod
    def get_valid_moves(piece, current_pos, board):
        piece_type = piece.piece_type
        if piece_type == 'pawn':
            return MoveRules._get_pawn_moves(piece, current_pos, board)
        elif piece_type == 'rook':
            return MoveRules._get_line_moves(piece, current_pos, board, DIRECTIONS['STRAIGHT'])
        elif piece_type == 'bishop':
            return MoveRules._get_line_moves(piece, current_pos, board, DIRECTIONS['DIAGONAL'])
        elif piece_type == 'knight':
            return MoveRules._get_knight_moves(piece, current_pos, board)
        elif piece_type == 'queen':
            return MoveRules._get_line_moves(piece, current_pos, board, 
                                           DIRECTIONS['STRAIGHT'] + DIRECTIONS['DIAGONAL'])
        elif piece_type == 'king':
            return MoveRules._get_king_moves(piece, current_pos, board)
        return []

    @staticmethod
    def _get_pawn_moves(piece, current_pos, board):
        row, col = current_pos
        moves = []
        direction = -1 if piece.color == 'white' else 1
        
        # Forward move
        next_row = row + direction
        if 0 <= next_row < BOARD_SIZE:
            if not board.get_piece_at(next_row, col):
                moves.append((next_row, col))
                # Initial two-square move
                if not piece.has_moved:
                    two_ahead = row + (2 * direction)
                    if 0 <= two_ahead < BOARD_SIZE and not board.get_piece_at(two_ahead, col):
                        moves.append((two_ahead, col))

        # Diagonal captures
        for dcol in [-1, 1]:
            new_row, new_col = row + direction, col + dcol
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                target = board.get_piece_at(new_row, new_col)
                if target and target.color != piece.color:
                    moves.append((new_row, new_col))
                    
        return moves

    @staticmethod
    def _get_line_moves(piece, current_pos, board, directions):
        moves = []
        row, col = current_pos
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                target = board.get_piece_at(r, c)
                if not target:
                    moves.append((r, c))
                else:
                    if target.color != piece.color:
                        moves.append((r, c))
                    break
                r, c = r + dr, c + dc
                
        return moves

    @staticmethod
    def _get_knight_moves(piece, current_pos, board):
        moves = []
        row, col = current_pos
        
        for dr, dc in DIRECTIONS['KNIGHT']:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                target = board.get_piece_at(r, c)
                if not target or target.color != piece.color:
                    moves.append((r, c))
        
        return moves

    @staticmethod
    def _get_king_moves(piece, current_pos, board):
        moves = []
        row, col = current_pos
        
        for dr, dc in DIRECTIONS['STRAIGHT'] + DIRECTIONS['DIAGONAL']:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                target = board.get_piece_at(r, c)
                if not target or target.color != piece.color:
                    moves.append((r, c))
        
        return moves