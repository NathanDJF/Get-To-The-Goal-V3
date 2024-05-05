import pygame
import os
import sys

screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Test')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()