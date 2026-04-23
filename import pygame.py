import pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Characters")

clock = pygame.time.Clock()

# Player 1
p1_x, p1_y = 100, 300
p1_speed = 5

# Player 2
p2_x, p2_y = 600, 300
p2_speed = 5

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Player 1 controls (WASD)
    if keys[pygame.K_a]:
        p1_x -= p1_speed
    if keys[pygame.K_d]:
        p1_x += p1_speed
    if keys[pygame.K_w]:
        p1_y -= p1_speed
    if keys[pygame.K_s]:
        p1_y += p1_speed

    # Player 2 controls (Arrow keys)
    if keys[pygame.K_LEFT]:
        p2_x -= p2_speed
    if keys[pygame.K_RIGHT]:
        p2_x += p2_speed
    if keys[pygame.K_UP]:
        p2_y -= p2_speed
    if keys[pygame.K_DOWN]:
        p2_y += p2_speed

    # Draw players
    pygame.draw.rect(screen, (0, 0, 255), (p1_x, p1_y, 50, 50))  # Blue player
    pygame.draw.rect(screen, (255, 0, 0), (p2_x, p2_y, 50, 50))  # Red player

    pygame.display.update()

pygame.quit()