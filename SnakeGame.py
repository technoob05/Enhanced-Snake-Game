import math
import random
import pygame
import tkinter as tk 
from tkinter import messagebox
from pygame import mixer
import sys
import time

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
CELL_SIZE = 25

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Game states
MENU = 'menu'
PLAYING = 'playing'
PAUSED = 'paused'
GAME_OVER = 'game_over'

class SoundManager:
    def __init__(self):
        self.theme_music = mixer.Sound('ThemeSong.wav')
        self.snack_sound = mixer.Sound('snack.wav')
        self.lose_sound = mixer.Sound('lose.wav')
        self.power_up_sound = mixer.Sound('snack.wav')  # New sound for power-ups
        
        # Set volume levels
        self.theme_music.set_volume(0.5)
        self.snack_sound.set_volume(0.7)
        self.lose_sound.set_volume(0.7)
        
    def play_theme(self):
        self.theme_music.play(-1)
        
    def stop_theme(self):
        self.theme_music.stop()

class PowerUp:
    def __init__(self, pos, power_type):
        self.pos = pos
        self.type = power_type  # 'speed', 'slow', 'points', 'invincible'
        self.color = GOLD
        self.duration = 5  # Duration in seconds
        self.spawn_time = time.time()
        
    def draw(self, surface):
        x = self.pos[0] * CELL_SIZE
        y = self.pos[1] * CELL_SIZE
        pygame.draw.rect(surface, self.color, (x+1, y+1, CELL_SIZE-2, CELL_SIZE-2))
        
    def is_expired(self):
        return time.time() - self.spawn_time > 10  # Disappear after 10 seconds

class Cube:
    def __init__(self, start, dirnx=1, dirny=0, color=RED):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        
    def draw(self, surface, eyes=False):
        x = self.pos[0] * CELL_SIZE
        y = self.pos[1] * CELL_SIZE
        
        pygame.draw.rect(surface, self.color, (x+1, y+1, CELL_SIZE-2, CELL_SIZE-2))
        if eyes:
            center = CELL_SIZE // 2
            radius = 3
            eye1 = (x + center - radius, y + 8)
            eye2 = (x + CELL_SIZE - radius * 2, y + 8)
            pygame.draw.circle(surface, BLACK, eye1, radius)
            pygame.draw.circle(surface, BLACK, eye2, radius)

class Snake:
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body = [self.head]
        self.dirnx = 0
        self.dirny = 1
        self.turns = {}
        self.speed = 10
        self.score = 0
        self.high_score = 0
        self.is_invincible = False
        self.power_up_end_time = 0
        
    def move(self):
        keys = pygame.key.get_pressed()
        
        # Only allow turning if not moving in the opposite direction
        if keys[pygame.K_LEFT] and self.dirnx != 1:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_RIGHT] and self.dirnx != -1:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_UP] and self.dirny != 1:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_DOWN] and self.dirny != -1:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
        # Move body
        for i, cube in enumerate(self.body):
            p = cube.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Handle wrapping around screen edges
                if cube.dirnx == -1 and cube.pos[0] <= 0:
                    cube.pos = (GRID_SIZE-1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= GRID_SIZE-1:
                    cube.pos = (0, cube.pos[1])
                elif cube.dirny == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], GRID_SIZE-1)
                elif cube.dirny == 1 and cube.pos[1] >= GRID_SIZE-1:
                    cube.pos = (cube.pos[0], 0)
                else:
                    cube.move(cube.dirnx, cube.dirny)

    def apply_power_up(self, power_type):
        duration = 5  # seconds
        if power_type == 'speed':
            self.speed = 15
        elif power_type == 'slow':
            self.speed = 5
        elif power_type == 'invincible':
            self.is_invincible = True
        self.power_up_end_time = time.time() + duration

    def check_power_up_expiration(self):
        if time.time() > self.power_up_end_time:
            self.speed = 10
            self.is_invincible = False

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.speed = 10
        self.is_invincible = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        if dx == 1:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))
            
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        self.score += 10

    def draw(self, surface):
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Enhanced Snake Game')
        
        self.clock = pygame.time.Clock()
        self.sound_manager = SoundManager()
        self.state = MENU
        self.snake = Snake(RED, (10, 10))
        self.snack = Cube(self.random_position(), color=GREEN)
        self.power_up = None
        self.background = pygame.image.load('Snakebackground.png')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Font initialization
        self.font = pygame.font.Font(None, 36)
        
    def random_position(self):
        while True:
            x = random.randrange(GRID_SIZE)
            y = random.randrange(GRID_SIZE)
            if not any(cube.pos == (x, y) for cube in self.snake.body):
                return (x, y)

    def spawn_power_up(self):
        if random.random() < 0.1 and not self.power_up:  # 10% chance to spawn
            power_types = ['speed', 'slow', 'points', 'invincible']
            self.power_up = PowerUp(self.random_position(), random.choice(power_types))

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.window, WHITE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.window, WHITE, (0, y), (WINDOW_WIDTH, y))

    def draw_menu(self):
        self.window.fill(BLACK)
        title = self.font.render('SNAKE GAME', True, WHITE)
        start_text = self.font.render('Press SPACE to Start', True, WHITE)
        high_score_text = self.font.render(f'High Score: {self.snake.high_score}', True, WHITE)
        
        self.window.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//3))
        self.window.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, WINDOW_HEIGHT//2))
        self.window.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, WINDOW_HEIGHT*2//3))

    def draw_game(self):
        self.window.fill(BLACK)
        self.window.blit(self.background, (0, 0))
        self.draw_grid()
        self.snake.draw(self.window)
        self.snack.draw(self.window)
        if self.power_up:
            self.power_up.draw(self.window)
            
        # Draw score
        score_text = self.font.render(f'Score: {self.snake.score}', True, WHITE)
        self.window.blit(score_text, (10, 10))

    def handle_collision(self):
        # Snake-Snack collision
        if self.snake.head.pos == self.snack.pos:
            self.sound_manager.snack_sound.play()
            self.snake.add_cube()
            self.snack = Cube(self.random_position(), color=GREEN)
            self.spawn_power_up()

        # Snake-PowerUp collision
        if self.power_up and self.snake.head.pos == self.power_up.pos:
            self.sound_manager.power_up_sound.play()
            self.snake.apply_power_up(self.power_up.type)
            self.power_up = None

        # Snake-Self collision
        if not self.snake.is_invincible:
            for cube in self.snake.body[1:]:
                if self.snake.head.pos == cube.pos:
                    self.sound_manager.lose_sound.play()
                    self.state = GAME_OVER
                    return True
        return False

    def run(self):
        self.sound_manager.play_theme()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.state == MENU:
                            self.state = PLAYING
                        elif self.state == GAME_OVER:
                            self.snake.reset((10, 10))
                            self.state = MENU
                    elif event.key == pygame.K_p and self.state == PLAYING:
                        self.state = PAUSED
                    elif event.key == pygame.K_p and self.state == PAUSED:
                        self.state = PLAYING

            if self.state == MENU:
                self.draw_menu()
            elif self.state == PLAYING:
                self.snake.move()
                self.snake.check_power_up_expiration()
                if self.power_up and self.power_up.is_expired():
                    self.power_up = None
                if self.handle_collision():
                    continue
                self.draw_game()
            elif self.state == PAUSED:
                pause_text = self.font.render('PAUSED', True, WHITE)
                self.window.blit(pause_text, (WINDOW_WIDTH//2 - pause_text.get_width()//2, WINDOW_HEIGHT//2))
            elif self.state == GAME_OVER:
                game_over_text = self.font.render('GAME OVER', True, WHITE)
                restart_text = self.font.render('Press SPACE to Return to Menu', True, WHITE)
                final_score_text = self.font.render(f'Final Score: {self.snake.score}', True, WHITE)
                
                self.window.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//3))
                self.window.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2))
                self.window.blit(final_score_text, (WINDOW_WIDTH//2 - final_score_text.get_width()//2, WINDOW_HEIGHT*2//3))

            pygame.display.update()
            self.clock.tick(self.snake.speed)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()