import pygame
import math
import imageio.v2 as imageio  # For saving GIF
import numpy as np

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth & Jupiter Orbit Simulation")

# Delay before starting
pygame.time.delay(5000)  # Wait for 5 seconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)  # Sun color
BLUE = (50, 100, 255)   # Earth color
ORANGE = (255, 140, 0)  # Jupiter color
GRAY = (100, 100, 100)  # Orbit path color
RED = (255, 0, 0)       # Mark closest approach

# Font setup
pygame.font.init()
font = pygame.font.SysFont(None, 24)  # Small font for numbering

# Orbital radii
EARTH_ORBIT = 150
JUPITER_ORBIT = 250

# Orbital periods
JUPITER_PERIOD = 11.86

# Time variables
angle_earth = 0
angle_jupiter = 0

# Store closest approach points
closest_points = []
prev_distance = float('inf')
found_closest = False

# List to store frames for GIF
frames = []

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Draw Sun at center
    pygame.draw.circle(screen, YELLOW, (WIDTH // 2, HEIGHT // 2), 15)

    # Draw orbit paths
    pygame.draw.circle(screen, GRAY, (WIDTH // 2, HEIGHT // 2), EARTH_ORBIT, 1)
    pygame.draw.circle(screen, GRAY, (WIDTH // 2, HEIGHT // 2), JUPITER_ORBIT, 1)

    # Calculate positions using circular motion formula
    earth_x = WIDTH // 2 + EARTH_ORBIT * math.cos(math.radians(angle_earth))
    earth_y = HEIGHT // 2 + EARTH_ORBIT * math.sin(math.radians(angle_earth))

    jupiter_x = WIDTH // 2 + JUPITER_ORBIT * math.cos(math.radians(angle_jupiter))
    jupiter_y = HEIGHT // 2 + JUPITER_ORBIT * math.sin(math.radians(angle_jupiter))

    # Calculate distance between Earth and Jupiter
    distance = math.sqrt((earth_x - jupiter_x) ** 2 + (earth_y - jupiter_y) ** 2)

    # Detect exact closest approach and mark only once
    if distance < prev_distance:
        found_closest = True
    elif found_closest:
        closest_points.append((jupiter_x, jupiter_y))
        found_closest = False

    prev_distance = distance

    # Draw planets
    pygame.draw.circle(screen, BLUE, (int(earth_x), int(earth_y)), 8)
    pygame.draw.circle(screen, ORANGE, (int(jupiter_x), int(jupiter_y)), 10)

    # Draw closest approach points
    for index, (cx, cy) in enumerate(closest_points, start=1):
        pygame.draw.circle(screen, RED, (int(cx), int(cy)), 5)
        text_surface = font.render(str(index), True, WHITE)
        screen.blit(text_surface, (int(cx) + 10, int(cy) - 10))

    # Update angles
    angle_earth += 10
    angle_jupiter += 10 / JUPITER_PERIOD

    # Capture frame for GIF
    frame = pygame.surfarray.array3d(screen)  # Convert to array
    frame = np.rot90(frame)  # Rotate for proper orientation
    frame = np.fliplr(frame)  # Flip to match the display
    frames.append(frame)

    # Stop after 12 revolutions of Earth
    if angle_earth >= 360 * 12:
        running = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

# Save frames as a GIF
imageio.mimsave("orbit_simulation.gif", frames, fps=30)

print("GIF saved as orbit_simulation.gif ✅")
