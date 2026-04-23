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