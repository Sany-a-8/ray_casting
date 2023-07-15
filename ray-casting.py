import pygame
import math

# Game settings
WIDTH = 800
HEIGHT = 600
FOV = math.pi / 3  # Field of view
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# Map representation (1 represents wall, 0 represents empty space, 2 represents the winning space)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 2, 1]
]

# Player settings
player_x = 3.0
player_y = 3.0
player_angle = 0.0
player_radius = 5
player_speed = 0.1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Color gradient for different depths
SHADES_OF_BLUE = [
    (0, 0, 128),
    (0, 0, 160),
    (0, 0, 192),
    (0, 0, 224),
    (0, 0, 255)
]
WINNING_COLOR = (0, 255, 0)
TRANSPARENT = (0, 0, 0, 0)  # Transparent color

# Game state
game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle -= 0.1
        if keys[pygame.K_RIGHT]:
            player_angle += 0.1
        if keys[pygame.K_UP]:
            new_player_x = player_x + math.sin(player_angle) * player_speed
            new_player_y = player_y + math.cos(player_angle) * player_speed

            # Check collision with walls and winning space
            if (
                MAP[int(new_player_y)][int(new_player_x)] == 0
                or MAP[int(new_player_y)][int(new_player_x)] == 2
            ):
                player_x = new_player_x
                player_y = new_player_y

        if keys[pygame.K_DOWN]:
            new_player_x = player_x - math.sin(player_angle) * player_speed
            new_player_y = player_y - math.cos(player_angle) * player_speed

            # Check collision with walls and winning space
            if (
                MAP[int(new_player_y)][int(new_player_x)] == 0
                or MAP[int(new_player_y)][int(new_player_x)] == 2
            ):
                player_x = new_player_x
                player_y = new_player_y

        # Check if the player reaches the winning space
        if MAP[int(player_y)][int(player_x)] == 2:
            game_over = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the walls
    for x in range(WIDTH):
        ray_angle = (player_angle - FOV / 2) + (x / WIDTH) * FOV
        distance_to_wall = 0
        hit_wall = False
        hit_boundary = False
        eye_x = math.sin(ray_angle)
        eye_y = math.cos(ray_angle)

        while not hit_wall and distance_to_wall < 16:
            distance_to_wall += 0.1
            test_x = int(player_x + eye_x * distance_to_wall)
            test_y = int(player_y + eye_y * distance_to_wall)

            # Check if the ray is out of bounds
            if test_x < 0 or test_x >= len(MAP[0]) or test_y < 0 or test_y >= len(MAP):
                hit_wall = True
                distance_to_wall = 16
            else:
                if MAP[test_y][test_x] == 1:
                    hit_wall = True

        # Calculate the shade of blue based on the distance
        shade_index = min(int(distance_to_wall), len(SHADES_OF_BLUE) - 1)
        wall_color = SHADES_OF_BLUE[shade_index]

        ceiling = HALF_HEIGHT - int(HEIGHT / distance_to_wall) // 2
        floor = HEIGHT - ceiling

        pygame.draw.line(screen, wall_color, (x, ceiling), (x, floor))

    # Draw the winning space as a transparent rectangle
    for y in range(len(MAP)):
        for x in range(len(MAP[0])):
            if MAP[y][x] == 2:
                pygame.draw.rect(screen, TRANSPARENT, (x * 50, y * 50, 50, 50))

    # Draw the player as a transparent circle
    pygame.draw.circle(screen, TRANSPARENT, (int(player_x * 50), int(player_y * 50)), player_radius)

    # Display the winning message
    if game_over:
        text = font.render("YOU WIN!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Quit the game
pygame.quit()
