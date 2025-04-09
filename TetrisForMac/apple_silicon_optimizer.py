"""
Tetris-like Game for Mac with Apple Silicon
Apple Silicon optimization module - provides specific optimizations for M-series chips
"""

import platform
import os
import sys
import subprocess

class AppleSiliconOptimizer:
    """Class for optimizing game performance on Apple Silicon"""
    
    def __init__(self):
        """Initialize the optimizer"""
        self.is_apple_silicon = self._detect_apple_silicon()
        self.optimization_level = 0  # 0: None, 1: Basic, 2: Advanced
        
        # Set optimization level based on hardware
        if self.is_apple_silicon:
            self.optimization_level = 2
        elif platform.system() == 'Darwin':  # macOS but not Apple Silicon
            self.optimization_level = 1
    
    def _detect_apple_silicon(self):
        """Detect if running on Apple Silicon"""
        if platform.system() != 'Darwin':
            return False
        
        # Check architecture
        arch = platform.machine()
        if arch == 'arm64':
            return True
        
        # Additional check using sysctl on macOS
        try:
            result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                                   capture_output=True, text=True)
            cpu_info = result.stdout.strip()
            return 'Apple M' in cpu_info
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fall back to architecture check only
            return arch == 'arm64'
    
    def get_optimization_settings(self):
        """Get optimization settings based on detected hardware"""
        settings = {
            'use_metal': False,
            'texture_compression': False,
            'memory_optimization': False,
            'thread_count': 4,
            'vsync': True,
            'power_save_mode': False
        }
        
        if self.optimization_level >= 1:
            # Basic optimizations for all macOS
            settings['vsync'] = True
            settings['thread_count'] = 8
        
        if self.optimization_level >= 2:
            # Advanced optimizations for Apple Silicon
            settings['use_metal'] = True
            settings['texture_compression'] = True
            settings['memory_optimization'] = True
            settings['thread_count'] = 16  # M-series chips have more cores
            settings['power_save_mode'] = True  # Better battery life on laptops
        
        return settings
    
    def apply_pygame_optimizations(self):
        """Apply Pygame-specific optimizations"""
        import pygame
        
        # Set SDL environment variables for better performance
        if self.optimization_level >= 1:
            os.environ['SDL_HINT_RENDER_VSYNC'] = '1'
            os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = '1'
        
        if self.optimization_level >= 2:
            # Apple Silicon specific optimizations
            os.environ['SDL_HINT_RENDER_DRIVER'] = 'metal'
            os.environ['SDL_HINT_VIDEO_HIGHDPI_DISABLED'] = '0'  # Enable HiDPI support
            os.environ['SDL_HINT_VIDEO_MAC_FULLSCREEN_SPACES'] = '1'
            
            # Set OpenGL attributes for better performance
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
            pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)
    
    def optimize_display(self, screen_width, screen_height):
        """Optimize display settings for the current hardware"""
        import pygame
        
        flags = pygame.DOUBLEBUF
        
        if self.optimization_level >= 2:
            # Use hardware acceleration on Apple Silicon
            flags |= pygame.HWSURFACE
            
            # Check if we should use fullscreen
            if screen_width >= 1024 and screen_height >= 768:
                flags |= pygame.RESIZABLE
        
        return flags
    
    def get_system_info(self):
        """Get detailed system information"""
        info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'is_apple_silicon': self.is_apple_silicon,
            'optimization_level': self.optimization_level
        }
        
        # Add more detailed info for macOS
        if platform.system() == 'Darwin':
            try:
                # Get macOS version
                result = subprocess.run(['sw_vers', '-productVersion'], 
                                       capture_output=True, text=True)
                info['macos_version'] = result.stdout.strip()
                
                # Get CPU info
                result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                                       capture_output=True, text=True)
                info['cpu_model'] = result.stdout.strip()
                
                # Get RAM info
                result = subprocess.run(['sysctl', '-n', 'hw.memsize'], 
                                       capture_output=True, text=True)
                info['ram_bytes'] = int(result.stdout.strip())
                info['ram_gb'] = info['ram_bytes'] / (1024**3)
                
                # Get GPU info if possible
                result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                       capture_output=True, text=True)
                info['gpu_info'] = result.stdout.strip()
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
        
        return info
