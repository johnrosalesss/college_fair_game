import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Constants
WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 20
FPS = 40
GREEN = (11, 89, 65)
WHITE = (255, 255, 255)

# Set up the game window with initial windowed mode
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('St. Paul University Manila Mini-Game Made by BS Computer Science Students Batch 2023')

# Load food image
food_img = pygame.image.load("food.png")
food_img = pygame.transform.scale(food_img, (CELL_SIZE * 2, CELL_SIZE * 2))

# Load music file
pygame.mixer.music.load("bgm.mp3")  
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Snake and Food
snake = [(200, 200)]
snake_direction = (1, 0)
food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

# Game variables
score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True
game_over = False
welcome_screen = True
fullscreen = False

# Functions
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, WHITE, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food():
    screen.blit(food_img, (food[0], food[1]))

def move_snake():
    global score
    head = snake[0]
    new_head = (head[0] + snake_direction[0] * CELL_SIZE, head[1] + snake_direction[1] * CELL_SIZE)
    snake.insert(0, new_head)

    head_rect = pygame.Rect(new_head[0], new_head[1], CELL_SIZE, CELL_SIZE)
    food_rect = pygame.Rect(food[0], food[1], CELL_SIZE * 2, CELL_SIZE * 2)

    if head_rect.colliderect(food_rect):
        score += 1
        generate_food()
    else:
        snake.pop()

def generate_food():
    global food
    food = (random.randint(0, WIDTH // CELL_SIZE - 2) * CELL_SIZE, random.randint(0, HEIGHT // CELL_SIZE - 2) * CELL_SIZE)

def show_score():
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

while running:
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)
            elif event.key == pygame.K_RETURN and (game_over or welcome_screen):
                snake = [(200, 200)]
                snake_direction = (1, 0)
                score = 0
                game_over = False
                welcome_screen = False
            elif event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    if not game_over and not welcome_screen:
        move_snake()

        head_x, head_y = snake[0]
        if (
            head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= HEIGHT
            or len(snake) != len(set(snake))
        ):
            game_over = True

    if not welcome_screen:
        draw_snake()
        draw_food()
        show_score()

    if game_over:
        game_over_text = font.render('Thank you! We hope you enjoyed our mini game!', True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2.2 - 250, HEIGHT // 2))

        
    if welcome_screen:
        welcome_text = font.render('Hi Future Paulinian!', True, WHITE)
        subtitle_text = font.render('BSCS Students Present: Snake Game', True, WHITE)
        instruction1 = font.render('Press ENTER to Start', True, WHITE)
        instruction2 = font.render('Press F for Fullscreen', True, WHITE)
        controls_text = font.render('Use Arrow Keys to Move', True, WHITE)
        
        screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, HEIGHT // 3))
        screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 3 + 40))
        screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, HEIGHT // 2))
        screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, HEIGHT // 2 + 40))
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
