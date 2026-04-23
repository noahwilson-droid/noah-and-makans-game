import pygame
from sys import exit
pygame.init()


size = [1500, 800]
window = pygame.display.set_mode(size)
Image = pygame.image.load("download35.png")
Image = pygame.transform.scale(Image, (1500, 800))
done = False
while not done:
    pygame.display.flip()
    window.blit(Image, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

clock = pygame.time.Clock() #frame rate
while True: #game loop
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        pygame.display.update()
        clock.tick(60)