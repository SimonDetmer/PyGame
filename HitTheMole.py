__author__ = 'sdetmer'

# Import and Initialization
import pygame
from pygame.locals import *

pygame.init()

# Display configuration
size = (640, 480)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('HitTheMole')
bg = pygame.image.load("images/rasen01.jpg")

# Entities

# Action --> ALTER
# Assign Variables

# Loop
running = True
while running:
    # Timer

    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Draw the background
    screen.blit(bg, (0, 0))

    # Redisplay
    pygame.display.flip()

pygame.quit()
