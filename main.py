import pygame
import os
import sys

# images
player_img = pygame.image.load(os.path.join('Assets/player.png'))
spike_man_img = pygame.image.load(os.path.join('Assets/spike.png'))

# screen
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Get To The Goal V3')

# movement
class Player():
    def __init__(self, x, y, vel, img, spikes):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.spikes = spikes
        
    def draw(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a] and self.x > self.vel: 
            self.x -= self.vel

        if keys[pygame.K_d] and self.x < 900 - self.vel - 100:  
            self.x += self.vel
            
        if keys[pygame.K_w] and self.y > self.vel:
            self.y -= self.vel

        if keys[pygame.K_s] and self.y < 500 - 100 - self.vel:
            self.y += self.vel
            
        for spike in self.spikes:
            if self.check_collision(spike):
                self.x = 20
                self.y = 200
                break
        
        screen.blit(self.img, (self.x, self.y))
    
    def check_collision(self, spike):
        player_rect = self.img.get_rect(topleft=(self.x, self.y))
        spike_rect = spike.img.get_rect(topleft=(spike.x, spike.y))
        return player_rect.colliderect(spike_rect)
        
class Spike():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
player_thing = Player(20, 200, 5, player_img, [])
spikes = [Spike(400, 200, spike_man_img), Spike(400, 300, spike_man_img)]
player_thing.spikes = spikes

# main loop
while True:
    clock = pygame.time.Clock()
    clock.tick(60)
    screen.fill('white')
    player_thing.draw()
    for spike in spikes:
        spike.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
