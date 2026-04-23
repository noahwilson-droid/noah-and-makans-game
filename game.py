import pygame
from sys import exit

#game variable
GAME_WIDTH = 512
GAME_HEIGHT = 512

#Game Window
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Game of WIP") #title in window
clock = pygame.time.Clock() #frame rate

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        pygame.display.update()
        clock.tick(60) #60 FPS


