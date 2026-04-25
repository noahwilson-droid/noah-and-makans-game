import pygame

class Brawlers():
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    def move(self, canvas_width, canvas_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        #Keypresses/Inputs
        key = pygame.key.get_pressed()

            #Preventing Spam Attacks
        if self.attacking == False:
            #movement
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
            #Jump
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            #attacks
            if key[pygame.K_r] or key [pygame.K_t]:
                self.attack(surface, target)

                #Attack type
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 1

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

        #Makes characters always face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #updates player position
        self.rect.x += dx
        self.rect.y += dy       

    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)