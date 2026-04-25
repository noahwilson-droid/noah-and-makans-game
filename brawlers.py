import pygame

class Brawlers():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False

    def move(self, canvas_width, canvas_height):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        #Keypresses/Inputs
        key = pygame.key.get_pressed()

        #movement
        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED
        #Jump
        if key[pygame.K_w] and self.jump == False:
            self.vel_y = -30
            self.jump = True

        #Inventing Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #boundaries/barrier
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > canvas_width:
            dx = canvas_width - self.rect.right
        if self.rect.bottom + dy > canvas_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = canvas_height - 110 - self.rect.bottom

        #updates player position
        self.rect.x += dx
        self.rect.y += dy       


    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)