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
BLACK  = (0,   0,   0)
GOLD   = (212, 175, 55)

# Game state constants
STATE_MENU     = "menu"
STATE_FIGHTING = "fighting"
STATE_WINNER   = "winner"

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
SAMURAI_OFFSETS = [ #AI FIXED: SAMURAI ANIMATIONS DO NOT OFFSET
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

#Win condition
WINS_NEEDED = 3

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

# index order: [attack1, attack2, dead, hurt, idle, jump, run]
KNIGHT_ANIMATION_COOLDOWNS = [150, 150, 150, 150, 150, 150, 150]
SAMURAI_ANIMATION_COOLDOWNS = [150, 110, 150, 150, 150, 50, 150]
#AI FIXED: ALLOWS TWEAKS FOR INDIVIDUAL ANIMATION SPEEDS

#font
count_font = pygame.font.Font("Assets/font/Turok.ttf", 80)
score_font = pygame.font.Font("Assets/font/Turok.ttf", 30)
title_font  = pygame.font.Font("Assets/font/Turok.ttf", 90)
menu_font   = pygame.font.Font("Assets/font/Turok.ttf", 45)
winner_font = pygame.font.Font("Assets/font/Turok.ttf", 60)
point_font  = pygame.font.Font("Assets/font/Turok.ttf", 40) 

#function for drawing drawing text
def draw_text(text, font, text_col, x, y, center=False):
    img = font.render(text, True, text_col)
    if center:
        x = x - img.get_width() // 2
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

#dims background
def draw_overlay(alpha=160):
    overlay = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    overlay.set_alpha(alpha)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

#create two instances of fighters
def reset_round():
    brawler_1 = Brawlers(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, KNIGHT_ANIMATION_COOLDOWNS, sword_fx)
    brawler_2 = Brawlers(2, 700, 310, True, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, SAMURAI_ANIMATION_COOLDOWNS, kanata_fx)
    return brawler_1, brawler_2

#Start Menu for game 
def draw_menu(play_hovered, quit_hovered):
    draw_bg()
    draw_overlay() 

    # Title
    draw_text("STEEL vs HONOR", title_font, GOLD, CANVAS_WIDTH // 2, 120, center=True)
 
    # Subtitle
    draw_text("First to 3 wins!", score_font, WHITE, CANVAS_WIDTH // 2, 230, center=True)
 
    # Play button
    play_col = GOLD if play_hovered else WHITE
    draw_text("PLAY", menu_font, play_col, CANVAS_WIDTH // 2, 320, center=True)
 
    # Quit button
    quit_col = GOLD if quit_hovered else WHITE
    draw_text("QUIT", menu_font, quit_col, CANVAS_WIDTH // 2, 400, center=True)
 
    # Controls reminder
    draw_text("Knight: WASD + R/T       Samurai: Arrows + Num1/2",
              score_font, WHITE, CANVAS_WIDTH // 2, 520, center=True)
 
 
def get_menu_rects():
#Return rects for the PLAY and QUIT buttons so we can detect hover/click
    play_img = menu_font.render("PLAY", True, WHITE)
    quit_img = menu_font.render("QUIT", True, WHITE)
    play_rect = play_img.get_rect(center=(CANVAS_WIDTH // 2, 320 + play_img.get_height() // 2))
    quit_rect = quit_img.get_rect(center=(CANVAS_WIDTH // 2, 400 + quit_img.get_height() // 2))
    return play_rect, quit_rect

#Winner screen
def draw_winner_screen(winner_name, play_hovered, quit_hovered):
    """Show who won the match and offer Play Again / Quit."""
    draw_bg()
    draw_overlay()
 
    draw_text(winner_name + " WINS!", winner_font, GOLD,  CANVAS_WIDTH // 2, 150, center=True)
    draw_text("THE MATCH!",           winner_font, WHITE, CANVAS_WIDTH // 2, 230, center=True)
 
    play_col = GOLD if play_hovered else WHITE
    quit_col = GOLD if quit_hovered else WHITE
    draw_text("PLAY AGAIN", menu_font, play_col, CANVAS_WIDTH // 2, 340, center=True)
    draw_text("QUIT",       menu_font, quit_col, CANVAS_WIDTH // 2, 420, center=True)
 
 
def get_winner_rects():
    play_img = menu_font.render("PLAY AGAIN", True, WHITE)
    quit_img = menu_font.render("QUIT",       True, WHITE)
    play_rect = play_img.get_rect(center=(CANVAS_WIDTH // 2, 340 + play_img.get_height() // 2))
    quit_rect = quit_img.get_rect(center=(CANVAS_WIDTH // 2, 420 + quit_img.get_height() // 2))
    return play_rect, quit_rect

#Game state
game_state = STATE_MENU
score = [0, 0]
intro_count = 3
last_count_update = pygame.time.get_ticks()
round_over = False
round_over_time = 0
ROUND_OVER_COOLDOWN = 3000
winner_name = ""
round_winner_name = ""
 
brawler_1, brawler_2 = reset_round()

#game loop
run = True
while run:

    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    #Handles Game Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
 
            if game_state == STATE_MENU:
                play_rect, quit_rect = get_menu_rects()
                if play_rect.collidepoint(mouse_pos):
                    # Start a fresh match
                    score = [0, 0]
                    intro_count = 3
                    last_count_update = pygame.time.get_ticks()
                    round_over = False
                    round_winner_name = ""
                    brawler_1, brawler_2 = reset_round()
                    game_state = STATE_FIGHTING
                elif quit_rect.collidepoint(mouse_pos):
                    run = False
 
            elif game_state == STATE_WINNER:
                play_rect, quit_rect = get_winner_rects()
                if play_rect.collidepoint(mouse_pos):
                    # Return to menu
                    game_state = STATE_MENU
                elif quit_rect.collidepoint(mouse_pos):
                    run = False

    #Menu
    if game_state == STATE_MENU:
        play_rect, quit_rect = get_menu_rects()
        draw_menu(
            play_hovered=play_rect.collidepoint(mouse_pos),
            quit_hovered=quit_rect.collidepoint(mouse_pos)
        )
    elif game_state == STATE_FIGHTING:
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
            draw_text(str(intro_count), count_font, RED, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 3, center=True)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update brawlers
        brawler_1.update()
        brawler_2.update()

        #draw brawlers
        brawler_1.draw(screen)
        brawler_2.draw(screen)

        # Round over check
        if not round_over:
            if not brawler_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                round_winner_name = "Samurai"
            elif not brawler_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                round_winner_name = "Knight"
        else:
            screen.blit(victory_resize, (360, 150))
            #show point notification below the victory image
            draw_text(
                round_winner_name + " scores a point!",
                point_font, GOLD,
                CANVAS_WIDTH // 2, 310, center=True
            )
 
            # Check if someone has reached WINS_NEEDED
            if score[0] >= WINS_NEEDED:
                winner_name = "KNIGHT"
                game_state  = STATE_WINNER
            elif score[1] >= WINS_NEEDED:
                winner_name = "SAMURAI"
                game_state  = STATE_WINNER
            elif pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                # No winner yet, start next round
                round_over = False
                intro_count = 3
                last_count_update = pygame.time.get_ticks()
                round_winner_name = ""
                brawler_1, brawler_2 = reset_round()
 
    #Victory Screen
    elif game_state == STATE_WINNER:
        play_rect, quit_rect = get_winner_rects()
        draw_winner_screen(
            winner_name,
            play_hovered=play_rect.collidepoint(mouse_pos),
            quit_hovered=quit_rect.collidepoint(mouse_pos)
        )
 
    pygame.display.update()
 
pygame.quit()