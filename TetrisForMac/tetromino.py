"""
Tetris-like Game for Mac with Apple Silicon
Tetromino module - defines the Tetromino class and shapes
"""

import random
from colors import COLORS

# Tetromino shapes (each shape is a 4x4 grid)
SHAPES = [
    # I piece
    [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    # J piece
    [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    # L piece
    [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ],
    # O piece
    [
        [1, 1],
        [1, 1]
    ],
    # S piece
    [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    # T piece
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    # Z piece
    [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
]

# Colors for each tetromino shape
SHAPE_COLORS = [
    COLORS['CYAN'],     # I piece
    COLORS['BLUE'],     # J piece
    COLORS['ORANGE'],   # L piece
    COLORS['YELLOW'],   # O piece
    COLORS['GREEN'],    # S piece
    COLORS['PURPLE'],   # T piece
    COLORS['RED']       # Z piece
]

class Tetromino:
    """Class representing a tetromino piece"""
    
    def __init__(self, x, y):
        """Initialize a new random tetromino"""
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = SHAPE_COLORS[self.shape_index]
        self.x = x
        self.y = y
        self.rotation = 0
    
    def rotate(self, clockwise=True):
        """Rotate the tetromino"""
        # Special case for O piece (no rotation needed)
        if self.shape_index == 3:
            return
        
        # Create a new rotated shape
        old_shape = self.shape
        height = len(old_shape)
        width = len(old_shape[0])
        
        if clockwise:
            # Clockwise rotation
            new_shape = [[0 for _ in range(height)] for _ in range(width)]
            for y in range(height):
                for x in range(width):
                    new_shape[x][height - 1 - y] = old_shape[y][x]
        else:
            # Counter-clockwise rotation
            new_shape = [[0 for _ in range(height)] for _ in range(width)]
            for y in range(height):
                for x in range(width):
                    new_shape[width - 1 - x][y] = old_shape[y][x]
        
        self.shape = new_shape
        self.rotation = (self.rotation + (1 if clockwise else -1)) % 4
    
    def get_positions(self):
        """Get the absolute positions of all blocks in the tetromino"""
        positions = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((self.x + x, self.y + y))
        return positions
