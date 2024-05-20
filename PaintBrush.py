__author__ = 'sdetmer'

# Import and Initialization
import pygame
from pygame.locals import *

pygame.init()

# Display configuration
size = (640, 480)
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.set_caption('Paint Brush')

# Entities
brush = pygame.image.load('images/black_brush.gif')
brush = pygame.transform.scale(brush, (64, 64))

# Action --> ALTER
# Assign Variables
keepGoing = True
paint = False
clock = pygame.time.Clock()

# Loop
while keepGoing:
    # Timer
    clock.tick(30)

    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            keepGoing = False

    # Redisplay
    # Get the state of the mouse buttons
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  # Check if the left mouse button is pressed
        x, y = pygame.mouse.get_pos()
        screen.blit(brush, (x-32, y-32))

    pygame.display.update()  # Correct the update call

pygame.quit()
