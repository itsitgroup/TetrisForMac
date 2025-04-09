"""
Tetris-like Game for Mac with Apple Silicon
Sound effects module - handles game sounds
"""

import pygame
import os
import wave
import struct
import math

class SoundEffects:
    """Class for managing sound effects"""
    
    def __init__(self):
        """Initialize sound effects"""
        # Sound file paths
        self.sound_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')
        os.makedirs(self.sound_dir, exist_ok=True)
        
        # Sound effect file paths
        self.sound_files = {
            'rotate': os.path.join(self.sound_dir, 'rotate.wav'),
            'move': os.path.join(self.sound_dir, 'move.wav'),
            'drop': os.path.join(self.sound_dir, 'drop.wav'),
            'clear_line': os.path.join(self.sound_dir, 'clear_line.wav'),
            'game_over': os.path.join(self.sound_dir, 'game_over.wav'),
            'level_up': os.path.join(self.sound_dir, 'level_up.wav')
        }
        
        # Create placeholder sound files if they don't exist
        self._create_placeholder_sounds()
        
        # Initialize mixer with error handling
        self.sound_enabled = False
        try:
            pygame.mixer.init()
            self.sound_enabled = True
            
            # Load sound effects
            self.sounds = {}
            for name, path in self.sound_files.items():
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except pygame.error:
                    print(f"Warning: Could not load sound {path}")
        except pygame.error as e:
            print(f"Sound system disabled: {e}")
            self.sounds = {}
    
    def _create_placeholder_sounds(self):
        """Create placeholder sound files for testing"""
        try:
            import wave
            import struct
            
            # Parameters for simple beep sounds
            for name, freq in [
                ('rotate', 440),  # A4
                ('move', 330),    # E4
                ('drop', 220),    # A3
                ('clear_line', 660),  # E5
                ('game_over', 110),   # A2
                ('level_up', 880)     # A5
            ]:
                if not os.path.exists(self.sound_files[name]):
                    self._generate_beep(self.sound_files[name], freq)
        except ImportError:
            print("Warning: Could not create placeholder sounds")
    
    def _generate_beep(self, filename, freq, duration=0.2):
        """Generate a simple beep sound file"""
        sample_rate = 44100
        amplitude = 32767  # Max value for 16-bit audio
        num_samples = int(duration * sample_rate)
        
        # Extract sound name from filename
        sound_name = os.path.basename(filename).split('.')[0]
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                # Calculate base value with sine wave
                sine_val = math.sin(2 * math.pi * freq * t)
                
                # Apply envelope (fade in/out)
                if t < 0.05:
                    # Fade in
                    envelope = t / 0.05
                elif t > duration - 0.05:
                    # Fade out
                    envelope = (duration - t) / 0.05
                else:
                    # Sustain
                    envelope = 1.0
                
                # Apply sound-specific volume adjustments
                volume_adjust = 0.5  # Base volume adjustment
                if sound_name == 'game_over':
                    volume_adjust = 0.3
                elif sound_name == 'move':
                    volume_adjust = 0.4
                elif sound_name == 'rotate':
                    volume_adjust = 0.45
                elif sound_name == 'clear_line':
                    volume_adjust = 0.6
                elif sound_name == 'level_up':
                    volume_adjust = 0.7
                elif sound_name == 'drop':
                    volume_adjust = 0.35
                
                # Calculate final value, ensuring it stays within 16-bit range
                value = int(sine_val * envelope * volume_adjust * amplitude)
                value = max(-32768, min(32767, value))  # Clamp to 16-bit range
                
                data = struct.pack('<h', value)
                wav_file.writeframes(data)
    
    def play(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def set_volume(self, volume):
        """Set volume for all sound effects (0.0 to 1.0)"""
        if self.sound_enabled:
            for sound in self.sounds.values():
                sound.set_volume(volume)
