import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏹 Archery Game")
clock = pygame.time.Clock()

# Load and scale background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load and scale target
target_img = pygame.image.load("target.png")
target_img = pygame.transform.scale(target_img, (100, 100))
target_rect = target_img.get_rect()
target_rect.x = WIDTH - 200
target_rect.y = HEIGHT // 2 - 50

# Load and scale bow
bow_img = pygame.image.load("bow.png")
bow_img = pygame.transform.scale(bow_img, (50, 80))

# Load and scale arrow
arrow_img = pygame.image.load("arrow.png")
arrow_img = pygame.transform.scale(arrow_img, (60, 20))

# Initial position for bow and arrow
bow_x, bow_y = 100, HEIGHT // 2 - 40
arrow_x, arrow_y = bow_x + 50, bow_y + 30  # Offset from bow
arrow_speed = 15
arrow_fired = False

# Load sounds
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound("shoot.wav")

# Fonts
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Game state
score = 0
chances = 5
game_over = False

# Target movement
target_speed_y = 3
target_direction = 1

def show_score():
    text = font.render(f"Score: {score}   Chances Left: {chances}", True, (0, 0, 0))
    screen.blit(text, (20, 20))

def show_game_over():
    text = game_over_font.render("Game Over!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(target_img, target_rect)
    screen.blit(bow_img, (bow_x, bow_y))
    screen.blit(arrow_img, (arrow_x, arrow_y))
    show_score()

    if game_over:
        show_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot
        if event.type == pygame.KEYDOWN and not arrow_fired and not game_over:
            if event.key == pygame.K_SPACE:
                arrow_fired = True
                shoot_sound.play()

    # Control bow and arrow movement before firing
    keys = pygame.key.get_pressed()
    if not arrow_fired and not game_over:
        if keys[pygame.K_UP]:
            bow_y -= 5
            arrow_y -= 5
        if keys[pygame.K_DOWN]:
            bow_y += 5
            arrow_y += 5
        if keys[pygame.K_LEFT]:
            bow_x -= 5
            arrow_x -= 5
        if keys[pygame.K_RIGHT]:
            bow_x += 5
            arrow_x += 5

        # Keep within bounds
        bow_y = max(0, min(HEIGHT - 80, bow_y))
        bow_x = max(0, min(WIDTH - 110, bow_x))
        arrow_y = bow_y + 30
        arrow_x = bow_x + 50

    # Zigzag target movement
    if not game_over:
        target_rect.y += target_speed_y * target_direction
        if target_rect.y <= 0 or target_rect.y >= HEIGHT - target_rect.height:
            target_direction *= -1

        # Scoring zones
        bullseye = pygame.Rect(target_rect.x + 35, target_rect.y + 35, 30, 30)
        inner_ring = pygame.Rect(target_rect.x + 20, target_rect.y + 20, 60, 60)
        outer_ring = target_rect

    # Arrow flight
    if arrow_fired and not game_over:
        arrow_x += arrow_speed

        arrow_rect = pygame.Rect(arrow_x, arrow_y, 60, 20)

        if arrow_rect.colliderect(bullseye):
            score += 100
            arrow_fired = False
        elif arrow_rect.colliderect(inner_ring):
            score += 75
            arrow_fired = False
        elif arrow_rect.colliderect(outer_ring):
            score += 50
            arrow_fired = False
        elif arrow_x > WIDTH:
            chances -= 1
            arrow_fired = False
            if chances == 0:
                game_over = True

        if not arrow_fired:
            # Reset to bow
            arrow_x = bow_x + 50
            arrow_y = bow_y + 30

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
