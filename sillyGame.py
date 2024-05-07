import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
BLOCK_SIZE = 20

def draw_block(position, color):
    x, y = position
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + BLOCK_SIZE, y)
    glVertex2f(x + BLOCK_SIZE, y + BLOCK_SIZE)
    glVertex2f(x, y + BLOCK_SIZE)
    glEnd()

class SnakeGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.snake = [(0, 0)]  # Initial snake position
        self.direction = 'right'  # Initial snake direction
        self.food_position = self.generate_food_position()  # Initial food position
        self.game_running = True

    def generate_food_position(self):
        return (random.randrange(0, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE, 
                random.randrange(0, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)

    def draw_snake(self):
        for segment in self.snake:
            draw_block(segment, (0, 1, 0))  # Green color for the snake

    def draw_food(self):
        draw_block(self.food_position, (1, 0, 0))  # Red color for the food

    def move_snake(self):
        x, y = self.snake[0]
        if self.direction == 'up':
            y += BLOCK_SIZE
        elif self.direction == 'down':
            y -= BLOCK_SIZE
        elif self.direction == 'left':
            x -= BLOCK_SIZE
        elif self.direction == 'right':
            x += BLOCK_SIZE

        if (x, y) == self.food_position:
            self.snake.append(self.snake[-1])
            self.food_position = self.generate_food_position()
        else:
            self.snake.pop()

        self.snake.insert(0, (x, y))

    def handle_input(self, key):
        if key == pygame.K_UP and self.direction != 'down':
            self.direction = 'up'
        elif key == pygame.K_DOWN and self.direction != 'up':
            self.direction = 'down'
        elif key == pygame.K_LEFT and self.direction != 'right':
            self.direction = 'left'
        elif key == pygame.K_RIGHT and self.direction != 'left':
            self.direction = 'right'

    def game_over(self):
        x, y = self.snake[0]
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or len(self.snake) != len(set(self.snake)):
            return True
        return False

    def run(self):
        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF|OPENGL)
        gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(event.key)

            self.move_snake()

            if self.game_over():
                self.reset_game()  # Reset the game if it's over

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.draw_snake()
            self.draw_food()
            pygame.display.flip()
            clock.tick(10)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
