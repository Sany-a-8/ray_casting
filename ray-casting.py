import pygame
import math

# Game settings
WIDTH = 800
HEIGHT = 600
FOV = math.pi / 3  # Field of view
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# Map representation (1 represents wall, 0 represents empty space)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
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

# Color gradient for different depths
SHADES_OF_BLUE = [
    (0, 0, 128),
    (0, 0, 160),
    (0, 0, 192),
    (0, 0, 224),
    (0, 0, 255)
]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= 0.1
    if keys[pygame.K_RIGHT]:
        player_angle += 0.1
    if keys[pygame.K_UP]:
        new_player_x = player_x + math.sin(player_angle) * player_speed
        new_player_y = player_y + math.cos(player_angle) * player_speed

        # Check collision with walls
        if MAP[int(new_player_y)][int(new_player_x)] == 0:
            player_x = new_player_x
            player_y = new_player_y
        else:
            # Slide along the wall
            for i in range(10):
                temp_x = player_x + math.sin(player_angle) * player_speed * i / 10
                temp_y = player_y + math.cos(player_angle) * player_speed * i / 10
                if MAP[int(temp_y)][int(temp_x)] == 0:
                    player_x = temp_x
                    player_y = temp_y
                    break

    if keys[pygame.K_DOWN]:
        new_player_x = player_x - math.sin(player_angle) * player_speed
        new_player_y = player_y - math.cos(player_angle) * player_speed

        # Check collision with walls
        if MAP[int(new_player_y)][int(new_player_x)] == 0:
            player_x = new_player_x
            player_y = new_player_y
        else:
            # Slide along the wall
            for i in range(10):
                temp_x = player_x - math.sin(player_angle) * player_speed * i / 10
                temp_y = player_y - math.cos(player_angle) * player_speed * i / 10
                if MAP[int(temp_y)][int(temp_x)] == 0:
                    player_x = temp_x
                    player_y = temp_y
                    break

    # Clear the screen
    screen.fill((0, 0, 0))

    # Ray casting
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

        # Draw the walls
        pygame.draw.line(screen, wall_color, (x, ceiling), (x, floor))

    # Draw the player
    pygame.draw.circle(screen, (255, 0, 0), (int(player_x * 50), int(player_y * 50)), player_radius)

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Quit the game
pygame.quit()
