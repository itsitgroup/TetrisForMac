"""
Tetris-like Game for Mac with Apple Silicon
GameBoard module - defines the GameBoard class for managing the game state
"""

class GameBoard:
    """Class representing the game board"""
    
    def __init__(self, width, height):
        """Initialize a new game board"""
        self.width = width
        self.height = height
        self.board = [[None for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, tetromino, dx=0, dy=0):
        """Check if the tetromino can be placed at the given position"""
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    # Calculate the position on the board
                    board_x = tetromino.x + x + dx
                    board_y = tetromino.y + y + dy
                    
                    # Check if the position is out of bounds
                    if (board_x < 0 or board_x >= self.width or 
                        board_y < 0 or board_y >= self.height):
                        return False
                    
                    # Check if the position is already occupied
                    if board_y >= 0 and self.board[board_y][board_x]:
                        return False
        
        return True
    
    def lock_piece(self, tetromino):
        """Lock the tetromino in place on the board"""
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    # Calculate the position on the board
                    board_x = tetromino.x + x
                    board_y = tetromino.y + y
                    
                    # Only place the piece if it's within the board
                    if (0 <= board_x < self.width and 
                        0 <= board_y < self.height):
                        self.board[board_y][board_x] = tetromino.color
    
    def clear_lines(self):
        """Clear completed lines and return the number of lines cleared"""
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            # Check if the line is complete
            if all(self.board[y]):
                lines_cleared += 1
                
                # Move all lines above down
                for y2 in range(y, 0, -1):
                    self.board[y2] = self.board[y2 - 1][:]
                
                # Clear the top line
                self.board[0] = [None for _ in range(self.width)]
            else:
                y -= 1
        
        return lines_cleared
    
    def is_game_over(self):
        """Check if the game is over (pieces stacked to the top)"""
        # Check if any cell in the top row is filled
        return any(self.board[0])
    
    def reset(self):
        """Reset the game board"""
        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]
