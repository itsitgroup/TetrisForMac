"""
Tetris-like Game for Mac with Apple Silicon
Enhanced game mechanics module - implements additional game features
"""

class GameMechanics:
    """Class for enhanced game mechanics"""
    
    def __init__(self, game_board):
        """Initialize game mechanics"""
        self.game_board = game_board
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.combo_count = 0
        self.back_to_back_tetris = False
    
    def calculate_score(self, lines_cleared, drop_height=0, t_spin=False):
        """Calculate score based on lines cleared and other factors"""
        # Base points for lines cleared
        line_points = {
            1: 100,   # Single
            2: 300,   # Double
            3: 500,   # Triple
            4: 800    # Tetris
        }
        
        # No lines cleared
        if lines_cleared == 0:
            # Only award points for hard drop
            return drop_height
        
        # Calculate base score
        base_score = line_points.get(lines_cleared, 0) * self.level
        
        # Apply combo bonus
        if lines_cleared > 0:
            self.combo_count += 1
            combo_bonus = 50 * self.combo_count * self.level
        else:
            self.combo_count = 0
            combo_bonus = 0
        
        # Apply back-to-back bonus for consecutive Tetris clears
        b2b_bonus = 0
        if lines_cleared == 4:
            if self.back_to_back_tetris:
                b2b_bonus = 400 * self.level
            self.back_to_back_tetris = True
        elif lines_cleared > 0:
            self.back_to_back_tetris = False
        
        # Apply T-spin bonus
        t_spin_bonus = 0
        if t_spin:
            t_spin_bonus = 400 * lines_cleared * self.level
        
        # Calculate total score
        total_score = base_score + combo_bonus + b2b_bonus + t_spin_bonus + drop_height
        
        # Update score
        self.score += total_score
        
        # Update lines cleared
        self.lines_cleared += lines_cleared
        
        # Update level (every 10 lines)
        self.level = (self.lines_cleared // 10) + 1
        
        return total_score
    
    def get_ghost_piece_position(self, tetromino):
        """Get the position of the ghost piece (preview of where piece will land)"""
        # Create a copy of the current tetromino
        ghost_y = tetromino.y
        
        # Move the ghost piece down until it hits something
        while self.game_board.is_valid_position(tetromino, dy=ghost_y - tetromino.y + 1):
            ghost_y += 1
        
        return ghost_y
    
    def perform_wall_kick(self, tetromino, rotation_direction):
        """Attempt to perform wall kick when rotation would cause collision"""
        # Standard SRS wall kick data
        # Format: (test_index, (original_rotation, new_rotation)): [(x_offset, y_offset), ...]
        
        # I piece has different wall kick data than other pieces
        if tetromino.shape_index == 0:  # I piece
            wall_kick_data = {
                (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
                (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
                (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
                (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
                (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
                (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
                (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
                (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
            }
        else:  # JLSTZ pieces
            wall_kick_data = {
                (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
                (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
            }
        
        # O piece doesn't need wall kicks
        if tetromino.shape_index == 3:  # O piece
            return False
        
        # Calculate original and new rotation states
        original_rotation = tetromino.rotation
        new_rotation = (original_rotation + (1 if rotation_direction else -1)) % 4
        
        # Get wall kick data for this rotation
        kick_data = wall_kick_data.get((original_rotation, new_rotation), [])
        
        # Try each wall kick offset
        for offset_x, offset_y in kick_data:
            if self.game_board.is_valid_position(tetromino, dx=offset_x, dy=offset_y):
                # Apply the offset
                tetromino.x += offset_x
                tetromino.y += offset_y
                return True
        
        # If no wall kick worked, return False
        return False
    
    def is_t_spin(self, tetromino, board):
        """Check if the last move was a T-spin"""
        # Only T pieces can perform T-spins
        if tetromino.shape_index != 5:  # T piece
            return False
        
        # Count filled corners around the T piece
        corners_filled = 0
        corners = [
            (tetromino.x, tetromino.y),  # Top-left
            (tetromino.x + 2, tetromino.y),  # Top-right
            (tetromino.x, tetromino.y + 2),  # Bottom-left
            (tetromino.x + 2, tetromino.y + 2)  # Bottom-right
        ]
        
        for x, y in corners:
            # Check if corner is outside the board or filled
            if (x < 0 or x >= board.width or 
                y < 0 or y >= board.height or 
                (0 <= y < board.height and 0 <= x < board.width and board.board[y][x])):
                corners_filled += 1
        
        # T-spin requires at least 3 corners filled
        return corners_filled >= 3
