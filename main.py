import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump game by dissentty")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_image = pygame.image.load("image.png")
player_size = 50
player_image = pygame.transform.scale(player_image, (int(player_size*1.1), int(player_size*1.1)))

platform_image = pygame.image.load("platform.png")
platform_width, platform_height = 70, 10
platform_image = pygame.transform.scale(platform_image, (int(platform_width*1), int(platform_height*2)))

player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 100
player_velocity_y = 0
gravity = 0.25
jump_strength = -10

platform_count = 5
score = 0

def create_platforms():
    platforms = [[WIDTH // 2 - platform_width // 2, HEIGHT - 50]]
    for i in range(platform_count):
        x = random.randint(0, WIDTH - platform_width)
        y = HEIGHT - (i * 120) - 100
        platforms.append([x, y])
    return platforms

platforms = create_platforms()

def reset_game():
    global player_x, player_y, player_velocity_y, platforms
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 100
    player_velocity_y = 0
    platforms = create_platforms()


running = True
game_over = False
clock = pygame.time.Clock()

while running:
    win.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                game_over = False
                score = 0
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= 5
        if keys[pygame.K_d]:
            player_x += 5

        player_velocity_y += gravity
        player_y += player_velocity_y

        for platform in platforms:
            if (player_x + player_size > platform[0] and player_x < platform[0] + platform_width and
                player_y + player_size >= platform[1] and player_y + player_size - player_velocity_y < platform[1] and
                player_velocity_y > 0):
                player_velocity_y = jump_strength

        if player_y > HEIGHT:
            game_over = True

        if player_y < HEIGHT // 2:
            player_y = HEIGHT // 2
            for platform in platforms:
                platform[1] += int(-player_velocity_y)
                if platform[1] > HEIGHT:
                    platform[0] = random.randint(0, WIDTH - platform_width)
                    platform[1] = 0
                    score += 1

        win.blit(player_image, (player_x, player_y))
        for platform in platforms:
            win.blit(platform_image, (platform[0], platform[1]))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        win.blit(score_text, (10, 10))

    else:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Press 'R' Score: {score}", True, RED)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.update()
    clock.tick(60)

pygame.quit()


