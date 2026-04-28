import pygame

class Brawlers():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, animation_cooldowns, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 4 #Checks animation type #0:attack1 #1:attack2 #2:dead #3:hurt #4:idle #5:jump #6:run
        self.frame_index = 0
        self.animation_cooldowns = animation_cooldowns #AI FIXED: Helps with individual animation cooldowns
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, canvas_width, canvas_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #Keypresses/Inputs
        key = pygame.key.get_pressed()

            #can only perform attacks if not attacking
        if self.attacking == False and self.alive  == True and round_over == False:
            #checks Player 1 controls
            if self.player  == 1:
            #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
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
                        self.attack_type = 2

            #checks Player 2 controls
            if self.player  == 2:
            #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #Jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #attacks
                if key[pygame.K_KP1] or key [pygame.K_KP2]:
                    self.attack(surface, target)

                    #Attack type
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

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

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        

        #updates player position
        self.rect.x += dx
        self.rect.y += dy       


    #animations
    def update(self):
        #check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(2) #2:death
        elif self.hit == True:
            self.update_action(3) #3:Hurt
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(0) #0:Attack1
            elif self.attack_type == 2:
                self.update_action(1) #1:Attack2
        elif self.jump == True:
            self.update_action(5) #5:Jump
        elif self.running == True:
            self.update_action(6) #6:Run
        else:
            self.update_action(4) #4:idle

        animation_cooldown = self.animation_cooldowns[self.action]
        #updates images
        self.image = self.animation_list[self.action][self.frame_index]
        #Checks if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #check if player died then end animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #checks if attack happened
                if self.action == 0 or self.action == 1:
                    self.attacking = False
                    self.attack_cooldown = 30
                #Checking for damage taken
                if self.action == 3:
                    self.hit = False
                    #Cancels attack if hit, No hyperarmor
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            #execute atack
            self.attacking = True
            self.attack_sound.play()
            if self.flip:
                attacking_rect = pygame.Rect(self.rect.centerx - 2.5 * self.rect.width, self.rect.y, 2.5 * self.rect.width, self.rect.height)
            else:
                attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2.5 * self.rect.width, self.rect.height)
            #attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def update_action(self, new_action):
        #checks if action changes
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)

    # Support per-animation offsets or a single shared offset
        if isinstance(self.offset[0], list):
            offset = self.offset[self.action]
        else:
            offset = self.offset

        if self.flip:
        # When flipped, offset goes in the opposite x direction
            draw_x = self.rect.x - (self.image.get_width() - (offset[0] * self.image_scale) - self.rect.width)
        else:
            draw_x = self.rect.x - (offset[0] * self.image_scale)
    
        draw_y = self.rect.y - (offset[1] * self.image_scale)
        surface.blit(img, (draw_x, draw_y))
        #surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))