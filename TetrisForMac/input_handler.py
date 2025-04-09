"""
Tetris-like Game for Mac with Apple Silicon
Input handler module - provides optimized input handling for Apple Silicon
"""

import pygame
import platform

class InputHandler:
    """Class for handling input with optimizations for Apple Silicon"""
    
    def __init__(self):
        """Initialize the input handler"""
        self.is_apple_silicon = self._detect_apple_silicon()
        self.key_repeat_delay = 150  # ms
        self.key_repeat_interval = 50  # ms
        
        # Optimize key repeat settings for Apple Silicon
        if self.is_apple_silicon:
            self.key_repeat_delay = 120  # Slightly faster initial repeat
            self.key_repeat_interval = 40  # Faster repeat rate
        
        # Key state tracking
        self.pressed_keys = {}
        self.key_hold_time = {}
        self.last_repeat_time = {}
    
    def _detect_apple_silicon(self):
        """Detect if running on Apple Silicon"""
        if platform.system() != 'Darwin':
            return False
        
        # Check architecture
        return platform.machine() == 'arm64'
    
    def setup(self):
        """Set up input handling"""
        # Configure key repeat
        pygame.key.set_repeat(self.key_repeat_delay, self.key_repeat_interval)
    
    def process_events(self, events):
        """Process input events with optimizations for Apple Silicon"""
        current_time = pygame.time.get_ticks()
        result = {
            'quit': False,
            'move_left': False,
            'move_right': False,
            'move_down': False,
            'rotate': False,
            'hard_drop': False,
            'pause': False,
            'mute': False,
            'restart': False,
            'change_style': False
        }
        
        for event in events:
            if event.type == pygame.QUIT:
                result['quit'] = True
            
            elif event.type == pygame.KEYDOWN:
                # Track key press time
                self.pressed_keys[event.key] = True
                self.key_hold_time[event.key] = current_time
                self.last_repeat_time[event.key] = current_time
                
                # Process key presses
                if event.key == pygame.K_LEFT:
                    result['move_left'] = True
                elif event.key == pygame.K_RIGHT:
                    result['move_right'] = True
                elif event.key == pygame.K_DOWN:
                    result['move_down'] = True
                elif event.key == pygame.K_UP:
                    result['rotate'] = True
                elif event.key == pygame.K_SPACE:
                    result['hard_drop'] = True
                elif event.key == pygame.K_p:
                    result['pause'] = True
                elif event.key == pygame.K_m:
                    result['mute'] = True
                elif event.key == pygame.K_r:
                    result['restart'] = True
                elif event.key == pygame.K_b:
                    result['change_style'] = True
            
            elif event.type == pygame.KEYUP:
                # Clear key state
                self.pressed_keys[event.key] = False
                if event.key in self.key_hold_time:
                    del self.key_hold_time[event.key]
                if event.key in self.last_repeat_time:
                    del self.last_repeat_time[event.key]
        
        # Handle key repeats with custom timing for smoother experience on Apple Silicon
        if self.is_apple_silicon:
            for key in self.pressed_keys:
                if not self.pressed_keys[key] or key not in self.key_hold_time:
                    continue
                
                hold_duration = current_time - self.key_hold_time[key]
                if hold_duration >= self.key_repeat_delay:
                    time_since_last_repeat = current_time - self.last_repeat_time[key]
                    if time_since_last_repeat >= self.key_repeat_interval:
                        # Trigger repeat action
                        self.last_repeat_time[key] = current_time
                        
                        if key == pygame.K_LEFT:
                            result['move_left'] = True
                        elif key == pygame.K_RIGHT:
                            result['move_right'] = True
                        elif key == pygame.K_DOWN:
                            result['move_down'] = True
        
        return result
    
    def get_touch_input(self):
        """Get touch input for trackpad gestures on Apple Silicon Macs"""
        # This is a placeholder for actual touch input handling
        # In a real implementation, this would use PyObjC to access trackpad events
        
        result = {
            'swipe_left': False,
            'swipe_right': False,
            'swipe_down': False,
            'tap': False,
            'double_tap': False
        }
        
        # Only attempt to get touch input on Apple Silicon
        if not self.is_apple_silicon:
            return result
        
        # Placeholder for actual touch input detection
        
        return result
