import sys

import os

import pygame
from pygame.locals import *

colors = { 0: (0, 0, 255), 1: (255, 0, 0), 2: (128, 0, 128), 4: (0, 128, 0) }

def run(grid):
    pygame.display.init()
    display = pygame.display.set_mode((1000, 1000))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                running = False

        display.fill((255, 255, 255))

        for thePlace in grid.internal_grid:
            color = colors[thePlace.char.placeType.value]
            pygame.draw.rect(display, color, (10*thePlace.x, 10*thePlace.y, 7, 7))

        pygame.display.update()
    
    pygame.display.quit()
    
