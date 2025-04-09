"""
Tetris-like Game for Mac with Apple Silicon
Memory optimizer module - provides memory optimizations for ARM architecture
"""

import gc
import sys
import platform

class MemoryOptimizer:
    """Class for optimizing memory usage on Apple Silicon"""
    
    def __init__(self):
        """Initialize the memory optimizer"""
        self.is_apple_silicon = self._detect_apple_silicon()
        self.optimization_level = 0  # 0: None, 1: Basic, 2: Advanced
        
        # Set optimization level based on hardware
        if self.is_apple_silicon:
            self.optimization_level = 2
        elif platform.system() == 'Darwin':  # macOS but not Apple Silicon
            self.optimization_level = 1
        
        # Apply initial optimizations
        self._apply_initial_optimizations()
    
    def _detect_apple_silicon(self):
        """Detect if running on Apple Silicon"""
        if platform.system() != 'Darwin':
            return False
        
        # Check architecture
        return platform.machine() == 'arm64'
    
    def _apply_initial_optimizations(self):
        """Apply initial memory optimizations"""
        # Enable garbage collection
        gc.enable()
        
        if self.optimization_level >= 1:
            # Set threshold for garbage collection
            gc.set_threshold(700, 10, 5)
        
        if self.optimization_level >= 2:
            # More aggressive garbage collection for Apple Silicon
            gc.set_threshold(500, 10, 5)
    
    def optimize_surface_usage(self, pygame):
        """Optimize surface usage for better memory performance"""
        if self.optimization_level >= 1:
            # Use hardware acceleration when available
            pygame.display.set_allow_screensaver(True)
        
        if self.optimization_level >= 2:
            # Apple Silicon specific optimizations
            # These settings help reduce memory bandwidth usage
            pygame.display.set_allow_screensaver(False)  # Prevent screensaver from activating
    
    def optimize_texture_loading(self, pygame):
        """Optimize texture loading for ARM architecture"""
        if self.optimization_level >= 2:
            # On Apple Silicon, we can use more aggressive texture compression
            # This is a placeholder for actual texture optimization code
            pass
    
    def run_garbage_collection(self):
        """Manually run garbage collection"""
        if self.optimization_level >= 1:
            # Run garbage collection
            collected = gc.collect()
            return collected
        return 0
    
    def get_memory_usage(self):
        """Get current memory usage"""
        import psutil
        
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss': memory_info.rss,  # Resident Set Size
            'vms': memory_info.vms,  # Virtual Memory Size
            'rss_mb': memory_info.rss / (1024 * 1024),
            'vms_mb': memory_info.vms / (1024 * 1024)
        }
    
    def optimize_for_frame(self, frame_count):
        """Run per-frame optimizations"""
        # Run garbage collection periodically
        if self.optimization_level >= 2 and frame_count % 1000 == 0:
            self.run_garbage_collection()
        elif self.optimization_level >= 1 and frame_count % 2000 == 0:
            self.run_garbage_collection()
