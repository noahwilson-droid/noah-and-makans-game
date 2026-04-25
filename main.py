import pygame
from brawlers import Brawlers

pygame.init()

#Game's Window
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600

screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("Battle of Lungunica")

#Implementing Framerate
clock = pygame.time.Clock()
FPS = 60

#Background/Setting
bg_image = pygame.image.load("download35.png").convert_alpha()

#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (CANVAS_WIDTH, CANVAS_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#create two instances of fighters
brawler_1 = Brawlers(200, 310)
brawler_2 = Brawlers(700, 310)

#game loop
run = True
while run:

    clock.tick(FPS)

    #drawing the background
    draw_bg()

    #calling the movement method from fighters
    brawler_1.move(CANVAS_WIDTH, CANVAS_HEIGHT)
    #brawler_2.move()

    #draw brawlers
    brawler_1.draw(screen)
    brawler_2.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

pygame.quit()