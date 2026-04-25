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

#Color for Health Bar
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define fighter variables
KNIGHT_SIZE = 128
KNIGHT_SCALE = 3
KNIGHT_OFFSET = [20, 67]
KNIGHT_DATA = [KNIGHT_SIZE, KNIGHT_SCALE, KNIGHT_OFFSET]
SAMURAI_SIZE = 128
SAMURAI_OFFSET = [80, 67]
SAMURAI_SCALE = 3
SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET]

#Background/Setting
bg_image = pygame.image.load("download35.png").convert_alpha()

#spritesheets
knight_sheet = pygame.image.load("Assets\Brawlers\knight.png").convert_alpha()
samurai_sheet = pygame.image.load("Assets\Brawlers\Samurai.png").convert_alpha()

#Steps of animation in each animation
KNIGHT_ANIMATION_STEPS = [4, 4, 6, 2, 4, 6, 7]
SAMURAI_ANIMATION_STEPS = [4, 5, 6, 3, 6, 9, 8]

#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (CANVAS_WIDTH, CANVAS_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#creating health bars. also I want to add assest to the bars to make them look cool
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#create two instances of fighters
brawler_1 = Brawlers(200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS)
brawler_2 = Brawlers(700, 310, True, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS)

#game loop
run = True
while run:

    clock.tick(FPS)

    #drawing the background
    draw_bg()

    #Display of Health Bar
    draw_health_bar(brawler_1.health, 20, 20)
    draw_health_bar(brawler_2.health, 580, 20)

    #calling the movement method from fighters
    brawler_1.move(CANVAS_WIDTH, CANVAS_HEIGHT, screen, brawler_2)

    #update brawlers
    brawler_1.update()
    brawler_2.update()

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