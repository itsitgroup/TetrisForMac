#!/usr/bin/env python3
"""
Tetris-like Game for Mac with Apple Silicon
Main game file with integrated Apple Silicon optimizations
"""

import pygame
import sys
import random
import os
from tetromino import Tetromino
from game_board import GameBoard
from colors import COLORS
from sound_effects import SoundEffects
from game_mechanics import GameMechanics
from ui import UI
from graphics import Graphics
from apple_silicon_optimizer import AppleSiliconOptimizer
from metal_renderer import MetalRenderer
from memory_optimizer import MemoryOptimizer
from input_handler import InputHandler

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_POSITION_X = (SCREEN_WIDTH - BOARD_WIDTH * BLOCK_SIZE) // 2
BOARD_POSITION_Y = 50

# Initialize Apple Silicon optimizations
apple_silicon_optimizer = AppleSiliconOptimizer()
optimization_settings = apple_silicon_optimizer.get_optimization_settings()

# Apply Pygame optimizations
apple_silicon_optimizer.apply_pygame_optimizations()

# Initialize memory optimizer
memory_optimizer = MemoryOptimizer()

# Set up the display with optimized flags
display_flags = apple_silicon_optimizer.optimize_display(SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), display_flags)
pygame.display.set_caption("Tetris for Mac (Apple Silicon)")

# Initialize Metal renderer if available
metal_renderer = MetalRenderer(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)

# Initialize input handler
input_handler = InputHandler()
input_handler.setup()

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

def main():
    """Main game function"""
    global screen
    
    # Create game components
    game_board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT)
    sound_effects = SoundEffects()
    game_mechanics = GameMechanics(game_board)
    ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
    graphics = Graphics(BLOCK_SIZE)
    
    # Game state variables
    current_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
    next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
    ghost_y = 0
    
    # Game timing
    fall_time = 0
    fall_speed = 0.5  # seconds
    last_fall_time = pygame.time.get_ticks()
    
    # Game flags
    game_over = False
    paused = False
    muted = False
    last_level = 1
    
    # Frame counter for memory optimization
    frame_count = 0
    
    # Print system info
    system_info = apple_silicon_optimizer.get_system_info()
    print(f"Running on: {system_info['system']} {system_info['release']}")
    print(f"Architecture: {system_info['machine']}")
    print(f"Apple Silicon: {system_info['is_apple_silicon']}")
    print(f"Optimization level: {system_info['optimization_level']}")
    print(f"Metal rendering: {metal_renderer.is_enabled}")
    
    # Main game loop
    running = True
    while running:
        # Increment frame counter
        frame_count += 1
        
        # Run memory optimizations
        memory_optimizer.optimize_for_frame(frame_count)
        
        # Calculate time since last piece movement
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_fall_time) / 1000.0
        
        # Get all events
        events = pygame.event.get()
        
        # Process input with optimized handler
        input_actions = input_handler.process_events(events)
        
        # Check for quit
        if input_actions['quit']:
            running = False
        
        # Handle game actions
        if not game_over and not paused:
            if input_actions['move_left']:
                if game_board.is_valid_position(current_piece, dx=-1):
                    current_piece.x -= 1
                    sound_effects.play('move')
            
            if input_actions['move_right']:
                if game_board.is_valid_position(current_piece, dx=1):
                    current_piece.x += 1
                    sound_effects.play('move')
            
            if input_actions['move_down']:
                if game_board.is_valid_position(current_piece, dy=1):
                    current_piece.y += 1
                    sound_effects.play('move')
                else:
                    # Lock the piece in place if it can't move down
                    game_board.lock_piece(current_piece)
                    sound_effects.play('drop')
                    
                    # Add particles at the landing position
                    for y, row in enumerate(current_piece.shape):
                        for x, cell in enumerate(row):
                            if cell:
                                pos_x = BOARD_POSITION_X + (current_piece.x + x) * BLOCK_SIZE + BLOCK_SIZE // 2
                                pos_y = BOARD_POSITION_Y + (current_piece.y + y) * BLOCK_SIZE + BLOCK_SIZE // 2
                                graphics.add_particles(pos_x, pos_y, current_piece.color)
                    
                    # Check for completed lines
                    lines = game_board.clear_lines()
                    if lines > 0:
                        # Add line clear animations
                        for y in range(BOARD_HEIGHT - 1, -1, -1):
                            if all(game_board.board[y]):
                                graphics.add_line_clear_animation(
                                    y, BOARD_POSITION_X, BOARD_POSITION_Y, BOARD_WIDTH
                                )
                        
                        # Play sound effect
                        sound_effects.play('clear_line')
                        
                        # Update score and level
                        drop_height = current_piece.y
                        game_mechanics.calculate_score(lines, drop_height)
                        
                        # Check for level up
                        if game_mechanics.level > last_level:
                            sound_effects.play('level_up')
                            graphics.start_level_up_animation(game_mechanics.level)
                            last_level = game_mechanics.level
                            fall_speed = max(0.05, 0.5 - (game_mechanics.level - 1) * 0.05)
                    
                    # Get next piece
                    current_piece = next_piece
                    next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
                    
                    # Check if game is over
                    if not game_board.is_valid_position(current_piece):
                        game_over = True
                        sound_effects.play('game_over')
            
            if input_actions['rotate']:
                # Save original rotation
                original_rotation = current_piece.rotation
                
                # Rotate the piece
                current_piece.rotate()
                
                # Check if rotation is valid, if not try wall kick
                if not game_board.is_valid_position(current_piece):
                    # Try wall kick
                    if game_mechanics.perform_wall_kick(current_piece, True):
                        sound_effects.play('rotate')
                    else:
                        # Rotate back if wall kick failed
                        current_piece.rotate(clockwise=False)
                else:
                    sound_effects.play('rotate')
            
            if input_actions['hard_drop']:
                # Hard drop
                drop_height = 0
                while game_board.is_valid_position(current_piece, dy=1):
                    current_piece.y += 1
                    drop_height += 1
                
                # Lock the piece and get a new one
                game_board.lock_piece(current_piece)
                sound_effects.play('drop')
                
                # Add particles at the landing position
                for y, row in enumerate(current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            pos_x = BOARD_POSITION_X + (current_piece.x + x) * BLOCK_SIZE + BLOCK_SIZE // 2
                            pos_y = BOARD_POSITION_Y + (current_piece.y + y) * BLOCK_SIZE + BLOCK_SIZE // 2
                            graphics.add_particles(pos_x, pos_y, current_piece.color)
                
                # Check for completed lines
                lines = game_board.clear_lines()
                if lines > 0:
                    # Add line clear animations
                    for y in range(BOARD_HEIGHT - 1, -1, -1):
                        if all(game_board.board[y]):
                            graphics.add_line_clear_animation(
                                y, BOARD_POSITION_X, BOARD_POSITION_Y, BOARD_WIDTH
                            )
                    
                    # Play sound effect
                    sound_effects.play('clear_line')
                    
                    # Update score with hard drop bonus
                    game_mechanics.calculate_score(lines, drop_height)
                    
                    # Check for level up
                    if game_mechanics.level > last_level:
                        sound_effects.play('level_up')
                        graphics.start_level_up_animation(game_mechanics.level)
                        last_level = game_mechanics.level
                        fall_speed = max(0.05, 0.5 - (game_mechanics.level - 1) * 0.05)
                
                current_piece = next_piece
                next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
                
                if not game_board.is_valid_position(current_piece):
                    game_over = True
                    sound_effects.play('game_over')
            
            if input_actions['change_style']:
                # Change block style
                new_style = graphics.change_block_style()
                print(f"Block style changed to: {new_style}")
        
        # Global controls (work even when paused or game over)
        if input_actions['pause']:
            # Toggle pause
            paused = not paused
        
        if input_actions['mute']:
            # Toggle mute
            muted = not muted
            sound_effects.set_volume(0.0 if muted else 1.0)
        
        if input_actions['restart'] and game_over:
            # Reset game
            game_board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT)
            game_mechanics = GameMechanics(game_board)
            current_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
            next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
            game_over = False
            last_level = 1
            fall_speed = 0.5
        
        # Update game state if not paused or game over
        if not paused and not game_over:
            # Update ghost piece position
            ghost_y = game_mechanics.get_ghost_piece_position(current_piece)
            
            # Move piece down automatically after fall_speed seconds
            fall_time += delta_time
            if fall_time >= fall_speed:
                if game_board.is_valid_position(current_piece, dy=1):
                    current_piece.y += 1
                else:
                    # Lock the piece in place if it can't move down
                    game_board.lock_piece(current_piece)
                    sound_effects.play('drop')
                    
                    # Add particles at the landing position
                    for y, row in enumerate(current_piece.shape):
                        for x, cell in enumerate(row):
                            if cell:
                                pos_x = BOARD_POSITION_X + (current_piece.x + x) * BLOCK_SIZE + BLOCK_SIZE // 2
                                pos_y = BOARD_POSITION_Y + (current_piece.y + y) * BLOCK_SIZE + BLOCK_SIZE // 2
                                graphics.add_particles(pos_x, pos_y, current_piece.color)
                    
                    # Check for completed lines
                    lines = game_board.clear_lines()
                    if lines > 0:
                        # Add line clear animations
                        for y in range(BOARD_HEIGHT - 1, -1, -1):
                            if all(game_board.board[y]):
                                graphics.add_line_clear_animation(
                                    y, BOARD_POSITION_X, BOARD_POSITION_Y, BOARD_WIDTH
                                )
                        
                        # Play sound effect
                        sound_effects.play('clear_line')
                        
                        # Update score
                        game_mechanics.calculate_score(lines)
                        
                        # Check for level up
                        if game_mechanics.level > last_level:
                            sound_effects.play('level_up')
                            graphics.start_level_up_animation(game_mechanics.level)
                            last_level = game_mechanics.level
                            fall_speed = max(0.05, 0.5 - (game_mechanics.level - 1) * 0.05)
                    
                    # Get next piece
                    current_piece = next_piece
                    next_piece = Tetromino(BOARD_WIDTH // 2 - 1, 0)
                    
                    # Check if game is over
                    if not game_board.is_valid_position(current_piece):
                        game_over = True
                        sound_effects.play('game_over')
                
                fall_time = 0
            
            last_fall_time = current_time
            
            # Update animations
            graphics.update_particles()
            graphics.update_line_clear_animations()
            graphics.update_level_up_animation()
            graphics.update_stars()
        
        # Start Metal frame if available
        using_metal = metal_renderer.begin_frame()
        
        # Draw everything
        # Draw background
        screen.fill(COLORS['BLACK'])
        graphics.draw_stars(screen)
        
        # Draw game board background
        pygame.draw.rect(
            screen, 
            COLORS['DARK_GRAY'], 
            (BOARD_POSITION_X - 2, BOARD_POSITION_Y - 2, 
             BOARD_WIDTH * BLOCK_SIZE + 4, BOARD_HEIGHT * BLOCK_SIZE + 4)
        )
        pygame.draw.rect(
            screen, 
            COLORS['GRAY'], 
            (BOARD_POSITION_X - 2, BOARD_POSITION_Y - 2, 
             BOARD_WIDTH * BLOCK_SIZE + 4, BOARD_HEIGHT * BLOCK_SIZE + 4),
            2
        )
        
        # Draw board grid and locked pieces
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                # Draw grid
                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    (BOARD_POSITION_X + x * BLOCK_SIZE, 
                     BOARD_POSITION_Y + y * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE),
                    1
                )
                
                # Draw locked pieces
                if game_board.board[y][x]:
                    graphics.draw_block(
                        screen,
                        BOARD_POSITION_X + x * BLOCK_SIZE,
                        BOARD_POSITION_Y + y * BLOCK_SIZE,
                        game_board.board[y][x]
                    )
        
        # Draw ghost piece
        if not game_over and not paused:
            graphics.draw_ghost_piece(
                screen, current_piece, ghost_y, 
                BOARD_POSITION_X, BOARD_POSITION_Y
            )
        
        # Draw current piece
        if current_piece and not game_over:
            for y, row in enumerate(current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        graphics.draw_block(
                            screen,
                            BOARD_POSITION_X + (current_piece.x + x) * BLOCK_SIZE,
                            BOARD_POSITION_Y + (current_piece.y + y) * BLOCK_SIZE,
                            current_piece.color
                        )
        
        # Draw UI elements
        ui.draw_game_info(
            screen, 
            game_mechanics.score, 
            game_mechanics.level, 
            game_mechanics.lines_cleared,
            next_piece,
            50, 100, 200
        )
        
        ui.draw_controls(screen, 50, 450, 200)
        
        # Draw logo at the top
        screen.blit(ui.logo, (SCREEN_WIDTH // 2 - ui.logo.get_width() // 2, 10))
        
        # Draw animations
        graphics.draw_particles(screen)
        graphics.draw_line_clear_animations(screen)
        graphics.draw_level_up_animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Draw game over or pause overlay
        if game_over:
            ui.draw_game_over(screen, game_mechanics.score)
        elif paused:
            ui.draw_pause(screen)
        
        # Draw mute indicator
        if muted:
            ui.draw_text(screen, "MUTED", ui.small_font, COLORS['RED'], 
                        SCREEN_WIDTH - 80, 10)
        
        # Apply Metal post-processing if available
        if using_metal:
            screen = metal_renderer.apply_post_processing(screen)
            metal_renderer.end_frame()
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Clean up
    if metal_renderer.is_enabled:
        metal_renderer.cleanup()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
