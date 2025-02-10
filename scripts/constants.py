# Board dimensions
BOARD_SIZE = 8

# Move directions
DIRECTIONS = {
    'DIAGONAL': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
    'STRAIGHT': [(0, 1), (0, -1), (1, 0), (-1, 0)],
    'KNIGHT': [(2, 1), (2, -1), (-2, 1), (-2, -1),
               (1, 2), (1, -2), (-1, 2), (-1, -2)]
}