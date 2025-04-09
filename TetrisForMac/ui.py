"""
Tetris-like Game for Mac with Apple Silicon
UI module - handles user interface elements
"""

import pygame
import os

class UI:
    """Class for managing user interface elements"""
    
    def __init__(self, screen_width, screen_height, block_size):
        """Initialize UI elements"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        
        # Load fonts
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.large_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.medium_font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        # Create assets directory
        self.assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        os.makedirs(self.assets_dir, exist_ok=True)
        
        # Load background image or create a placeholder
        self.background_path = os.path.join(self.assets_dir, 'background.png')
        self._create_placeholder_background()
        try:
            self.background = pygame.image.load(self.background_path)
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except pygame.error:
            # Create a simple gradient background if image loading fails
            self.background = self._create_gradient_background(screen_width, screen_height)
        
        # Create logo
        self.logo_path = os.path.join(self.assets_dir, 'logo.png')
        self._create_placeholder_logo()
        try:
            self.logo = pygame.image.load(self.logo_path)
            self.logo = pygame.transform.scale(self.logo, (300, 100))
        except pygame.error:
            # Create a text logo if image loading fails
            self.logo = self._create_text_logo(300, 100)
    
    def _create_placeholder_background(self):
        """Create a placeholder background image if it doesn't exist"""
        if not os.path.exists(self.background_path):
            # Create a simple gradient background
            surface = self._create_gradient_background(800, 700)
            pygame.image.save(surface, self.background_path)
    
    def _create_gradient_background(self, width, height):
        """Create a gradient background"""
        surface = pygame.Surface((width, height))
        
        # Create a dark blue to black gradient
        for y in range(height):
            # Calculate gradient color
            color_value = max(0, 50 - int(y / height * 50))
            color = (0, color_value, color_value * 2)
            
            # Draw a horizontal line with this color
            pygame.draw.line(surface, color, (0, y), (width, y))
        
        # Add some subtle grid lines
        for x in range(0, width, 40):
            for y in range(0, height, 40):
                pygame.draw.rect(surface, (30, 30, 40), (x, y, 40, 40), 1)
        
        return surface
    
    def _create_placeholder_logo(self):
        """Create a placeholder logo if it doesn't exist"""
        if not os.path.exists(self.logo_path):
            # Create a text-based logo
            surface = self._create_text_logo(300, 100)
            pygame.image.save(surface, self.logo_path)
    
    def _create_text_logo(self, width, height):
        """Create a text-based logo"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw "TETRIS" text with block-like styling
        logo_font = pygame.font.SysFont('Arial', 48, bold=True)
        text = logo_font.render("TETRIS", True, (0, 255, 255))
        
        # Add a shadow
        shadow = logo_font.render("TETRIS", True, (0, 100, 100))
        surface.blit(shadow, (6, 26))
        
        # Add main text
        surface.blit(text, (5, 25))
        
        # Add "FOR MAC" subtitle
        subtitle_font = pygame.font.SysFont('Arial', 20)
        subtitle = subtitle_font.render("FOR MAC (APPLE SILICON)", True, (200, 200, 200))
        surface.blit(subtitle, (width//2 - subtitle.get_width()//2, 75))
        
        return surface
    
    def draw_text(self, surface, text, font, color, x, y, align="left"):
        """Draw text with specified alignment"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if align == "left":
            text_rect.topleft = (x, y)
        elif align == "center":
            text_rect.midtop = (x, y)
        elif align == "right":
            text_rect.topright = (x, y)
        
        surface.blit(text_surface, text_rect)
        return text_rect
    
    def draw_panel(self, surface, x, y, width, height, title=None):
        """Draw a panel with optional title"""
        # Draw panel background
        pygame.draw.rect(surface, (0, 0, 0, 180), (x, y, width, height))
        pygame.draw.rect(surface, (100, 100, 100), (x, y, width, height), 2)
        
        # Draw title if provided
        if title:
            title_rect = self.draw_text(surface, title, self.medium_font, (255, 255, 255), 
                                       x + width//2, y + 5, align="center")
            # Draw separator line
            pygame.draw.line(surface, (100, 100, 100), 
                            (x + 10, title_rect.bottom + 5), 
                            (x + width - 10, title_rect.bottom + 5), 2)
            
            return title_rect.bottom + 10
        return y + 10
    
    def draw_game_info(self, surface, score, level, lines, next_piece, x, y, width):
        """Draw game information panel"""
        panel_height = 300
        y_offset = self.draw_panel(surface, x, y, width, panel_height, "GAME INFO")
        
        # Draw score
        self.draw_text(surface, "SCORE", self.small_font, (200, 200, 200), x + 10, y_offset + 10)
        self.draw_text(surface, f"{score}", self.large_font, (255, 255, 255), x + 10, y_offset + 35)
        
        # Draw level
        self.draw_text(surface, "LEVEL", self.small_font, (200, 200, 200), x + 10, y_offset + 75)
        self.draw_text(surface, f"{level}", self.large_font, (255, 255, 100), x + 10, y_offset + 100)
        
        # Draw lines cleared
        self.draw_text(surface, "LINES", self.small_font, (200, 200, 200), x + 10, y_offset + 140)
        self.draw_text(surface, f"{lines}", self.large_font, (100, 255, 100), x + 10, y_offset + 165)
        
        # Draw next piece preview
        self.draw_text(surface, "NEXT", self.small_font, (200, 200, 200), x + width//2, y_offset + 10, align="center")
        
        # Draw next piece
        if next_piece:
            preview_x = x + width//2 - len(next_piece.shape[0]) * self.block_size // 2
            preview_y = y_offset + 50
            
            for y_idx, row in enumerate(next_piece.shape):
                for x_idx, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            surface, 
                            next_piece.color,
                            (preview_x + x_idx * self.block_size, 
                             preview_y + y_idx * self.block_size,
                             self.block_size, self.block_size)
                        )
                        pygame.draw.rect(
                            surface, 
                            (0, 0, 0),
                            (preview_x + x_idx * self.block_size, 
                             preview_y + y_idx * self.block_size,
                             self.block_size, self.block_size),
                            1
                        )
    
    def draw_controls(self, surface, x, y, width):
        """Draw controls information panel"""
        panel_height = 200
        y_offset = self.draw_panel(surface, x, y, width, panel_height, "CONTROLS")
        
        controls = [
            ("←/→", "Move Left/Right"),
            ("↑", "Rotate"),
            ("↓", "Soft Drop"),
            ("Space", "Hard Drop"),
            ("P", "Pause Game"),
            ("M", "Mute Sound"),
            ("R", "Restart (Game Over)")
        ]
        
        for i, (key, action) in enumerate(controls):
            # Draw key
            key_rect = self.draw_text(surface, key, self.medium_font, (255, 255, 100), 
                                     x + 20, y_offset + i * 25)
            # Draw action
            self.draw_text(surface, action, self.small_font, (200, 200, 200), 
                          key_rect.right + 15, y_offset + i * 25)
    
    def draw_game_over(self, surface, score):
        """Draw game over overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Draw game over text
        self.draw_text(surface, "GAME OVER", self.title_font, (255, 50, 50), 
                      self.screen_width // 2, self.screen_height // 2 - 60, align="center")
        
        # Draw final score
        self.draw_text(surface, f"Final Score: {score}", self.large_font, (255, 255, 255), 
                      self.screen_width // 2, self.screen_height // 2, align="center")
        
        # Draw restart instruction
        self.draw_text(surface, "Press R to Restart", self.medium_font, (200, 200, 200), 
                      self.screen_width // 2, self.screen_height // 2 + 50, align="center")
    
    def draw_pause(self, surface):
        """Draw pause overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        # Draw pause text
        self.draw_text(surface, "PAUSED", self.title_font, (255, 255, 255), 
                      self.screen_width // 2, self.screen_height // 2 - 30, align="center")
        
        # Draw continue instruction
        self.draw_text(surface, "Press P to Continue", self.medium_font, (200, 200, 200), 
                      self.screen_width // 2, self.screen_height // 2 + 30, align="center")
    
    def draw_level_up(self, surface, level):
        """Draw level up notification"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        surface.blit(overlay, (0, 0))
        
        # Draw level up text
        self.draw_text(surface, f"LEVEL {level}!", self.title_font, (255, 255, 100), 
                      self.screen_width // 2, self.screen_height // 2, align="center")
