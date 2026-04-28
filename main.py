import pygame
from pygame import mixer
from brawlers import Brawlers

mixer.init()
pygame.init()

#Game's Window
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600

screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("Steel vs Honor")

#Implementing Framerate
clock = pygame.time.Clock()
FPS = 60

#Color for Health Bar
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] # score count
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
KNIGHT_SIZE = 128
KNIGHT_SCALE = 3
KNIGHT_OFFSET = [20, 67]
KNIGHT_DATA = [KNIGHT_SIZE, KNIGHT_SCALE, KNIGHT_OFFSET]
SAMURAI_SIZE = 128
SAMURAI_OFFSETS = [
    [40, 67], #attack1
    [45, 67], #attack2
    [50, 67], #dead
    [60, 67], #hurt
    [20, 67], #idle
    [55, 67], #jump
    [30, 67], #run
]
SAMURAI_SCALE = 3
SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSETS]

#Music and sounds
pygame.mixer.music.load("Assets\Sounds\piano-action-combat.ogg")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("Assets\Sounds\sword-attack.wav")
sword_fx.set_volume(0.2)
kanata_fx = pygame.mixer.Sound("Assets\Sounds\swing-the-katana.mp3")
kanata_fx.set_volume(0.9)

#Background/Setting
bg_image = pygame.image.load("Assets/background/vecteezy_illustration-of-landscape-with-bushes-trees_6081344.jpg").convert_alpha()

#spritesheets
knight_sheet = pygame.image.load("Assets\Brawlers\knight.png").convert_alpha()
samurai_sheet = pygame.image.load("Assets\Brawlers\Samurai.png").convert_alpha()

#load victory image and size change
victory_img = pygame.image.load("Assets/icon/victory.png").convert_alpha()
victory_resize = pygame.transform.scale_by(victory_img, 0.2)

#Steps of animation in each animation
KNIGHT_ANIMATION_STEPS = [4, 4, 6, 2, 4, 6, 7]
SAMURAI_ANIMATION_STEPS = [4, 5, 6, 3, 4, 9, 8]

#font
count_font = pygame.font.Font("Assets/font/Turok.ttf", 80)
score_font = pygame.font.Font("Assets/font/Turok.ttf", 30)

#function for drawing drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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
brawler_1 = Brawlers(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, sword_fx)
brawler_2 = Brawlers(2, 700, 310, True, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, kanata_fx)

#game loop
run = True
while run:

    clock.tick(FPS)

    #drawing the background
    draw_bg()

    #Display of Health Bar and Wins
    draw_health_bar(brawler_1.health, 20, 20)
    draw_health_bar(brawler_2.health, 580, 20)
    draw_text("Knight: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("Samurai: " + str(score[1]), score_font, RED, 580, 60)

    if intro_count <= 0:
        #calling the movement method from fighters
        brawler_1.move(CANVAS_WIDTH, CANVAS_HEIGHT, screen, brawler_2, round_over)
        brawler_2.move(CANVAS_WIDTH, CANVAS_HEIGHT, screen, brawler_1, round_over)
    else:
        #updates the countdown and display of countdown
        draw_text(str(intro_count), count_font, RED, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count)

    #update brawlers
    brawler_1.update()
    brawler_2.update()

    #draw brawlers
    brawler_1.draw(screen)
    brawler_2.draw(screen)

    #check for player defeat
    if round_over == False:
        if brawler_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        if brawler_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_resize, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            brawler_1 = Brawlers(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, sword_fx)
            brawler_2 = Brawlers(2, 700, 310, True, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, kanata_fx)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

pygame.quit()