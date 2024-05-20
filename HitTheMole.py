__author__ = 'sdetmer'

# IMPORT AND INITIALIZATION
import pygame
import random
from pygame.locals import *


pygame.init()

# DISPLAY CONFIGURATION
size = (700, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('HitTheMole')
bg = pygame.image.load("images/grass02.png")
counter = int()
# showCounter

# ENTITIES
# Load custom cursor image (shovel)
shovel = pygame.image.load("images/shovel.png")
shovel = pygame.transform.scale(shovel, (32, 32))

# Load mole image
mole = pygame.image.load("images/mole.png")
mole = pygame.transform.scale(mole, (64, 64))

# Hide the default mouse cursor
pygame.mouse.set_visible(False)

# Initial mole position
mole_rect = mole.get_rect()
mole_rect.topleft = (random.randint(0, size[0] - mole_rect.width), random.randint(0, size[1] - mole_rect.height))

# ACTION --> ALTER
# ASSIGN VARIABLES
show_mole = False
mole_timer = pygame.time.get_ticks()
mole_show_duration = 500  # Mole visible duration in milliseconds
mole_hide_duration = 400  # Mole hidden duration in milliseconds

# LOOP
running = True
clock = pygame.time.Clock()
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:  # Allow quitting with ESC key
            running = False

    # TIMER
    current_time = pygame.time.get_ticks()

    # Check if it's time to show or hide the mole
    if show_mole:
        if current_time - mole_timer > mole_show_duration:
            show_mole = False
            mole_timer = current_time
    else:
        if current_time - mole_timer > mole_hide_duration:
            show_mole = True
            mole_timer = current_time
            mole_rect.topleft = (random.randint(0, size[0] - mole_rect.width), random.randint(0, size[1] - mole_rect.height))

    # Draw the background
    screen.blit(bg, (0, 0))

    # Draw the mole if it's visible
    if show_mole:
        screen.blit(mole, mole_rect)

    # Get mouse position and draw the custom cursor (shovel)
    mouse_pos = pygame.mouse.get_pos()
    shovel_rect = shovel.get_rect(topleft=(mouse_pos[0] - 16, mouse_pos[1] - 16))  # Center the shovel on the mouse
    screen.blit(shovel, shovel_rect)

    # Event when hitting the mole
    # check if mouse pressed
    # Get current position of the mole_rect
    # get current position of shovel_rect
    # if intersection -- > Hit Animation and Sound and add 10Points to Counter
    # else --> Sound (miss)

    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  # Check if the left mouse button is pressed
        x, y = pygame.mouse.get_pos()
       # screen.blit(brush, (x-32, y-32))



    # REDISPLAY
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
