<<<<<<< HEAD
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

=======
from tkinter import Image

import pygame
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
pygame.quit()
>>>>>>> 3e9ab39400fb68785b813c87393e48a58c96993e
