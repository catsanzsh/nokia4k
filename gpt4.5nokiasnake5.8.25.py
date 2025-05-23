import pygame
import random
import numpy

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GPT4.5Snake')
clock = pygame.time.Clock()

# Audio setup
pygame.mixer.init()

def beep(frequency=440, duration_ms=100):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = numpy.linspace(0, duration_ms / 1000, n_samples, False)
    wave = numpy.sin(2 * numpy.pi * frequency * t)
    audio = numpy.stack((wave, wave), axis=-1)
    audio = (audio * 32767).astype(numpy.int16)
    sound = pygame.sndarray.make_sound(audio)
    sound.play()

# Snake and food setup
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (CELL_SIZE, 0)
food = (200, 200)

# Game vars
score = 0
font = pygame.font.SysFont("Consolas", 20)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)

    # Move snake
    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake = [head] + snake[:-1]

    # Check collision with food
    if head == food:
        snake.append(snake[-1])
        score += 1
        beep(frequency=500, duration_ms=150)
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

    # Check collision with walls or itself
    if (head in snake[1:] or head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT):
        beep(frequency=200, duration_ms=400)
        running = False

    # Render
    screen.fill((0, 0, 0))

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, (255, 0, 0), (*food, CELL_SIZE, CELL_SIZE))

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (5, 5))

    pygame.display.flip()
    clock.tick(10)

# Credits Display
screen.fill((0, 0, 0))
credits_text = [
    "GPT4.5Snake",
    "",
    "Created with Python 3.13 and Pygame",
    "Audio generated programmatically",
    "",
    "Engine inspired by Nokia Snake",
    "",
    f"Your Score: {score}",
    "Thanks for playing!",
]

y_pos = 100
for line in credits_text:
    text_surface = font.render(line, True, (255, 255, 255))
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_pos))
    y_pos += 30

pygame.display.flip()
pygame.time.wait(5000)
pygame.quit()
