import pygame
import os
import sys

pygame.init()

# images
player_img = pygame.image.load(os.path.join('Assets/player.png'))
spike_man_img = pygame.image.load(os.path.join('Assets/spike.png'))
moving_spike_man_img = pygame.image.load(os.path.join('Assets/moving spike.png'))
moving_spike_man_handle_img = pygame.image.load(os.path.join('Assets/moving spike handle.png'))
flag_img = pygame.image.load(os.path.join('Assets/flag.png'))

# screen
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Get To The Goal V3')

# font?
font = pygame.font.SysFont("Arial", 50, bold=True, italic=False)
font2 = pygame.font.SysFont("Arial", 20, bold=False, italic=False)
font3 = pygame.font.SysFont("Arial", 45, bold=False, italic=False)

# some variables or smth
completed_level = False
current_level = 1
winning_text = font3.render("Level Complete! Press ENTER to go to the next level", True, (255, 255, 255))

# movement
class Player():
    def __init__(self, x, y, vel, img, spikes, moving_spikes, flag):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.spikes = spikes
        self.moving_spikes = moving_spikes
        self.flag = flag
        
    def draw(self):
        global completed_level
        global current_level
        keys = pygame.key.get_pressed()
        
        if completed_level == False:
            
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if self.x > self.vel:
                    self.x -= self.vel

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if self.x < 900 - self.vel - 100:
                    self.x += self.vel
                
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if self.y > self.vel:
                    self.y -= self.vel

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if self.y < 500 - 100 - self.vel:
                    self.y += self.vel
            
        for spike in self.spikes:
            if self.check_collision_spike(spike):
                self.x = 20
                self.y = 200
                break
            
        for moving_spike in self.moving_spikes:
            if self.check_collision_moving_spike(moving_spike):
                self.x = 20
                self.y = 200
                break
        
        if self.check_collision_flag(self.flag):
            completed_level = True
        
        screen.blit(self.img, (self.x, self.y))
    
    def check_collision_spike(self, spike):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        spike_rect = spike.img.get_rect(topleft=(spike.x + 15, spike.y + 15), width=70, height=70)
        return player_rect.colliderect(spike_rect)
    
    def check_collision_moving_spike(self, moving_spike):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        moving_spike_rect = moving_spike.img.get_rect(topleft=(moving_spike.x + 15, moving_spike.y + 15), width=70, height=70)
        return player_rect.colliderect(moving_spike_rect)
    
    def check_collision_flag(self, flag):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        flag_rect = flag.img.get_rect(topleft=(flag.x + 50, flag.y + 50), width=1, height=100)
        return player_rect.colliderect(flag_rect)
    
    def check(self):
        global completed_level
        global current_level
        keys = pygame.key.get_pressed()
        if completed_level:
            screen.blit(winning_text, (15, 200))
            if keys[pygame.K_RETURN]:
                self.x = 20
                self.y = 200
                current_level += 1
                completed_level = False

class Spike():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
class Moving_Spike():
    def __init__(self, x, y, img, speed):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.go_up = False
        self.go_down = False
        
    def draw(self):
        
        if self.go_down == False:
            self.go_up = True
        if self.go_up == False:
            self.go_down = True
        if self.y <= 0:
            self.go_up = False
            self.go_down = True
        if self.y >= 400:
            self.go_up = True
            self.go_down = False
        
        # go down or up
        if self.go_up:
            self.y -= self.speed
        elif self.go_down:
            self.y += self.speed
        
        screen.blit(moving_spike_man_handle_img, (self.x + 45, 0))
        screen.blit(self.img, (self.x, self.y))
        
class Flag():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
class Level():
    def __init__(self, level, flag):
        self.level = level
        self.flag = flag
    
    def run(self):
        if self.level == 1:
            # text
            level_1_text = font.render("Level 1", True, (0, 0, 0))
            level_1_description_1 = font2.render("Welcome to Gttg v3", True, (0, 0, 0))
            level_1_description_2 = font2.render("You move with WASD or arrow keys", True, (0, 0, 0))
            level_1_description_3 = font2.render("Go to the flag to win", True, (0, 0, 0))
            screen.blit(level_1_text, (400, 0))
            screen.blit(level_1_description_1, (50, 50))
            screen.blit(level_1_description_2, (50, 75))
            screen.blit(level_1_description_3, (50, 100))
            
            # the level
            player_thing.draw()
            self.flag.draw()
            
            player_thing.check()

        if self.level == 2:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            spikes = [Spike(400, 200, spike_man_img)]
            player_thing.spikes = spikes
            for spike in spikes:
                spike.draw()
                
            player_thing.check()
            
            # text
            level_2_text = font.render("Level 2", True, (0, 0, 0))
            level_2_description_1 = font2.render("Don't touch the spike", True, (0, 0, 0))
            level_2_description_2 = font2.render("I think it kills you", True, (0, 0, 0))
            screen.blit(level_2_text, (400, 0))
            screen.blit(level_2_description_1, (50, 50))
            screen.blit(level_2_description_2, (50, 75))
            
        if self.level == 3:
            # the player flag
            player_thing.draw()
            self.flag.draw()
            
            # spikes
            spikes = [Spike(350, 200, spike_man_img), Spike(450, 200, spike_man_img)]
            player_thing.spikes = spikes
            for spike in spikes:
                spike.draw()
                
            player_thing.check()
            
            # text
            level_3_text = font.render("Level 3", True, (0, 0, 0))
            level_3_description = font2.render("More spikes", True, (0, 0, 0))
            screen.blit(level_3_text, (400, 0))
            screen.blit(level_3_description, (50, 50))
        
flag = Flag(775, 300, flag_img)
player_thing = Player(20, 200, 5, player_img, [], [], flag)
#moving_spikes = [Moving_Spike(700, 200, moving_spike_man_img, 4), Moving_Spike(800, 200, moving_spike_man_img, 100)]
#player_thing.moving_spikes = moving_spikes

# level stuff
level_1 = Level(1, flag)
level_2 = Level(2, flag)
level_3 = Level(3, flag)

# main loop
while True:
    clock = pygame.time.Clock()
    clock.tick(60)
    screen.fill((0, 128, 255))
    #for moving_spike in moving_spikes:
        #moving_spike.draw()
    if current_level == 1:
        level_1.run()
    elif current_level == 2:
        level_2.run()
    elif current_level == 3:
        level_3.run()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
