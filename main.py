import pygame
import os
import sys

# images
player_img = pygame.image.load(os.path.join('Assets/player.png'))
spike_man_img = pygame.image.load(os.path.join('Assets/spike.png'))
moving_spike_man_img = pygame.image.load(os.path.join('Assets/moving spike.png'))

# screen
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Get To The Goal V3')

# movement
class Player():
    def __init__(self, x, y, vel, img, spikes, moving_spikes):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.spikes = spikes
        self.moving_spikes = moving_spikes
        
    def draw(self):
        keys = pygame.key.get_pressed()
        
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
        
        screen.blit(self.img, (self.x, self.y))
    
    def check_collision_spike(self, spike):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        spike_rect = spike.img.get_rect(topleft=(spike.x + 15, spike.y + 15), width=70, height=70)
        return player_rect.colliderect(spike_rect)
    
    def check_collision_moving_spike(self, moving_spike):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        moving_spike_rect = moving_spike.img.get_rect(topleft=(moving_spike.x + 15, moving_spike.y + 15), width=70, height=70)
        return player_rect.colliderect(moving_spike_rect)

class Spike():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
class Moving_Spike():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
player_thing = Player(20, 200, 5, player_img, [], [])
spikes = [Spike(400, 200, spike_man_img)]
moving_spikes = [Moving_Spike(700, 200, moving_spike_man_img)]
player_thing.spikes = spikes
player_thing.moving_spikes = moving_spikes

# main loop
while True:
    clock = pygame.time.Clock()
    clock.tick(60)
    screen.fill('cyan')
    player_thing.draw()
    for spike in spikes:
        spike.draw()
    for moving_spike in moving_spikes:
        moving_spike.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
