__author__ = 'sdetmer'

# Import and Initialization
import pygame
from pygame.locals import *

pygame.init() #initialisiert alle Pygame-Module.

# Display configuration
size = (640, 480)
screen = pygame.display.set_mode(size) #erstellt ein Fenster mit der angegebenen Größe.
screen.fill((255, 255, 255)) #füllt den Bildschirm mit weißer Farbe.
pygame.display.set_caption('Paint Brush') #setzt den Fenstertitel.

# Entities
brush = pygame.image.load('images/black_brush.gif') #lädt das Bild des Pinsels.
brush = pygame.transform.scale(brush, (64, 64)) #skaliert das Bild auf die gewünschte Größe.

# Action --> ALTER
# Assign Variables
keepGoing = True #ist eine Kontrollvariable für die Hauptschleife.
paint = False
clock = pygame.time.Clock() #wird verwendet, um die Bildrate zu kontrollieren.

# Loop
while keepGoing: #Die Schleife läuft, solange keepGoing True ist.
    # Timer
    clock.tick(30) #beschränkt die Schleife auf 30 Frames pro Sekunde.

    # Event Handling
    for event in pygame.event.get(): #sammelt alle Ereignisse, wie das Schließen des Fensters (QUIT).
        if event.type == QUIT:
            keepGoing = False

    # Redisplay
    # Get the state of the mouse buttons
    mouse_pressed = pygame.mouse.get_pressed() #überprüft den Zustand der Maustasten.

    if mouse_pressed[0]:  # Check if the left mouse button is pressed
        x, y = pygame.mouse.get_pos() #holt die aktuelle Mausposition.
        screen.blit(brush, (x-32, y-32)) #zeichnet den Pinsel an der Mausposition.

    pygame.display.update()  #aktualisiert den Bildschirm, um die Änderungen anzuzeigen.

pygame.quit()
