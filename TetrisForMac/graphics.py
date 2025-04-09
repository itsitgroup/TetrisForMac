"""
Tetris-like Game for Mac with Apple Silicon
Graphics module - handles game graphics and animations
"""

import pygame
import random
import math

class Graphics:
    """Class for managing game graphics and animations"""
    
    def __init__(self, block_size):
        """Initialize graphics"""
        self.block_size = block_size
        
        # Block styles
        self.block_styles = {
            "classic": self._draw_classic_block,
            "rounded": self._draw_rounded_block,
            "gradient": self._draw_gradient_block,
            "3d": self._draw_3d_block
        }
        
        # Default style
        self.current_style = "3d"
        
        # Particle effects
        self.particles = []
        
        # Line clear animation
        self.line_clear_animations = []
        
        # Level up animation
        self.level_up_animation = None
        
        # Background effects
        self.background_stars = self._create_stars(100)
    
    def _create_stars(self, count):
        """Create background stars"""
        stars = []
        for _ in range(count):
            stars.append({
                'x': random.randint(0, 800),
                'y': random.randint(0, 700),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(100, 255)
            })
        return stars
    
    def update_stars(self):
        """Update background stars"""
        for star in self.background_stars:
            # Move stars down slowly
            star['y'] += star['speed']
            
            # Wrap around when reaching bottom
            if star['y'] > 700:
                star['y'] = 0
                star['x'] = random.randint(0, 800)
            
            # Twinkle effect
            star['brightness'] = max(100, min(255, star['brightness'] + random.randint(-10, 10)))
    
    def draw_stars(self, surface):
        """Draw background stars"""
        for star in self.background_stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            pygame.draw.circle(surface, color, (int(star['x']), int(star['y'])), star['size'])
    
    def _draw_classic_block(self, surface, x, y, color):
        """Draw a classic block (simple square)"""
        pygame.draw.rect(surface, color, (x, y, self.block_size, self.block_size))
        pygame.draw.rect(surface, (0, 0, 0), (x, y, self.block_size, self.block_size), 1)
    
    def _draw_rounded_block(self, surface, x, y, color):
        """Draw a rounded block"""
        radius = 3
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1, border_radius=radius)
    
    def _draw_gradient_block(self, surface, x, y, color):
        """Draw a gradient block"""
        # Create a surface for the block
        block_surface = pygame.Surface((self.block_size, self.block_size))
        
        # Create gradient
        r, g, b = color
        for i in range(self.block_size):
            # Lighten color towards top-left, darken towards bottom-right
            gradient_factor = i / self.block_size
            gradient_color = (
                min(255, int(r * (1 + 0.3 - gradient_factor * 0.6))),
                min(255, int(g * (1 + 0.3 - gradient_factor * 0.6))),
                min(255, int(b * (1 + 0.3 - gradient_factor * 0.6)))
            )
            pygame.draw.line(block_surface, gradient_color, (0, i), (i, 0))
            pygame.draw.line(block_surface, gradient_color, (i, self.block_size-1), (self.block_size-1, i))
        
        # Draw border
        pygame.draw.rect(block_surface, (0, 0, 0), (0, 0, self.block_size, self.block_size), 1)
        
        # Blit to main surface
        surface.blit(block_surface, (x, y))
    
    def _draw_3d_block(self, surface, x, y, color):
        """Draw a 3D block with lighting effect"""
        # Base color
        r, g, b = color
        
        # Top face (lighter)
        top_color = (min(255, int(r * 1.3)), min(255, int(g * 1.3)), min(255, int(b * 1.3)))
        pygame.draw.rect(surface, top_color, (x, y, self.block_size, self.block_size))
        
        # Right face (darker)
        right_color = (int(r * 0.8), int(g * 0.8), int(b * 0.8))
        right_points = [
            (x + self.block_size, y),
            (x + self.block_size - 4, y + 4),
            (x + self.block_size - 4, y + self.block_size - 4),
            (x + self.block_size, y + self.block_size)
        ]
        pygame.draw.polygon(surface, right_color, right_points)
        
        # Bottom face (darkest)
        bottom_color = (int(r * 0.6), int(g * 0.6), int(b * 0.6))
        bottom_points = [
            (x, y + self.block_size),
            (x + 4, y + self.block_size - 4),
            (x + self.block_size - 4, y + self.block_size - 4),
            (x + self.block_size, y + self.block_size)
        ]
        pygame.draw.polygon(surface, bottom_color, bottom_points)
        
        # Highlight
        highlight_points = [
            (x, y),
            (x + 4, y + 4),
            (x + self.block_size - 4, y + 4),
            (x + self.block_size, y)
        ]
        pygame.draw.polygon(surface, (255, 255, 255, 100), highlight_points)
        
        # Outline
        pygame.draw.rect(surface, (0, 0, 0), (x, y, self.block_size, self.block_size), 1)
    
    def draw_block(self, surface, x, y, color):
        """Draw a block using the current style"""
        self.block_styles[self.current_style](surface, x, y, color)
    
    def draw_ghost_piece(self, surface, tetromino, ghost_y, board_x, board_y):
        """Draw ghost piece (preview of where piece will land)"""
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    # Calculate position
                    pos_x = board_x + (tetromino.x + x) * self.block_size
                    pos_y = board_y + (ghost_y + y) * self.block_size
                    
                    # Draw ghost block (semi-transparent outline)
                    pygame.draw.rect(
                        surface,
                        (*tetromino.color[:3], 100),  # Semi-transparent
                        (pos_x, pos_y, self.block_size, self.block_size),
                        2  # Outline only
                    )
    
    def add_particles(self, x, y, color, count=10):
        """Add particles at the specified position"""
        for _ in range(count):
            self.particles.append({
                'x': x,
                'y': y,
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-3, 0),
                'size': random.uniform(2, 5),
                'color': color,
                'life': random.uniform(20, 40)
            })
    
    def update_particles(self):
        """Update particle positions and remove dead particles"""
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Apply gravity
            particle['dy'] += 0.1
            
            # Decrease life
            particle['life'] -= 1
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, surface):
        """Draw all particles"""
        for particle in self.particles:
            # Calculate alpha based on remaining life
            alpha = min(255, int(particle['life'] * 6))
            
            # Create a surface with per-pixel alpha
            s = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            
            # Draw the particle
            pygame.draw.circle(
                s,
                (*particle['color'][:3], alpha),
                (particle['size'], particle['size']),
                int(particle['size'])
            )
            
            # Blit to main surface
            surface.blit(s, (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def add_line_clear_animation(self, y, board_x, board_y, width):
        """Add line clear animation"""
        self.line_clear_animations.append({
            'y': y,
            'board_x': board_x,
            'board_y': board_y,
            'width': width,
            'progress': 0,
            'max_progress': 15
        })
    
    def update_line_clear_animations(self):
        """Update line clear animations"""
        for anim in self.line_clear_animations[:]:
            # Update progress
            anim['progress'] += 1
            
            # Remove completed animations
            if anim['progress'] >= anim['max_progress']:
                self.line_clear_animations.remove(anim)
    
    def draw_line_clear_animations(self, surface):
        """Draw line clear animations"""
        for anim in self.line_clear_animations:
            # Calculate animation progress (0 to 1)
            progress = anim['progress'] / anim['max_progress']
            
            # Calculate position and size
            x = anim['board_x']
            y = anim['board_y'] + anim['y'] * self.block_size
            width = anim['width'] * self.block_size
            
            # Draw white flash that fades out
            alpha = int(255 * (1 - progress))
            s = pygame.Surface((width, self.block_size), pygame.SRCALPHA)
            s.fill((255, 255, 255, alpha))
            surface.blit(s, (x, y))
    
    def start_level_up_animation(self, level):
        """Start level up animation"""
        self.level_up_animation = {
            'level': level,
            'progress': 0,
            'max_progress': 60  # 1 second at 60 FPS
        }
    
    def update_level_up_animation(self):
        """Update level up animation"""
        if self.level_up_animation:
            # Update progress
            self.level_up_animation['progress'] += 1
            
            # Remove completed animation
            if self.level_up_animation['progress'] >= self.level_up_animation['max_progress']:
                self.level_up_animation = None
    
    def draw_level_up_animation(self, surface, screen_width, screen_height):
        """Draw level up animation"""
        if self.level_up_animation:
            # Calculate animation progress (0 to 1)
            progress = self.level_up_animation['progress'] / self.level_up_animation['max_progress']
            
            # Create a surface with per-pixel alpha
            s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            
            # Calculate alpha (fade in, then fade out)
            if progress < 0.3:
                alpha = int(255 * (progress / 0.3))
            else:
                alpha = int(255 * (1 - (progress - 0.3) / 0.7))
            
            # Fill with semi-transparent black
            s.fill((0, 0, 0, min(150, alpha // 2)))
            
            # Draw text
            font = pygame.font.SysFont('Arial', 48, bold=True)
            text = font.render(f"LEVEL {self.level_up_animation['level']}!", True, (255, 255, 0))
            
            # Calculate position with a bounce effect
            bounce = math.sin(progress * math.pi) * 20
            x = screen_width // 2 - text.get_width() // 2
            y = screen_height // 2 - text.get_height() // 2 - bounce
            
            # Draw text with glow effect
            glow_size = 10
            for i in range(glow_size, 0, -2):
                glow_alpha = alpha * (i / glow_size) * 0.5
                glow_surface = pygame.Surface((text.get_width() + i*2, text.get_height() + i*2), pygame.SRCALPHA)
                pygame.draw.rect(
                    glow_surface,
                    (255, 255, 0, int(glow_alpha)),
                    (0, 0, text.get_width() + i*2, text.get_height() + i*2),
                    border_radius=i
                )
                s.blit(glow_surface, (x - i, y - i))
            
            # Draw main text
            s.blit(text, (x, y))
            
            # Blit to main surface
            surface.blit(s, (0, 0))
    
    def change_block_style(self):
        """Change the current block style"""
        styles = list(self.block_styles.keys())
        current_index = styles.index(self.current_style)
        self.current_style = styles[(current_index + 1) % len(styles)]
        return self.current_style
