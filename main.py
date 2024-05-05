import pygame
import os
import sys

# images
player_img = pygame.image.load(os.path.join('Assets/player.png'))

# screen
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Get To The Goal V3')

# main loop
while True:
    screen.fill('white')
    screen.blit(player_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()