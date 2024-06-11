__author__ = 'sdetmer'

# Import and Initialization
import pygame
import random
from pygame.locals import *
import sqlite3

pygame.init()

# Display configuration
size = (450, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('GalaxyIntruders')
bg = pygame.image.load("images/GalaxyIntrudersBG.jpg")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Highscore database setup
conn = sqlite3.connect('highscores.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS highscores
             (name TEXT, score INTEGER)''')
conn.commit()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("images/player.png")
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (size[0] // 2, size[1] - 10)
        self.speed = 5
        self.lives = 3

    def update(self, keys):
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < size[0]:
            self.rect.x += self.speed


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= size[0] or self.rect.left <= 0:
            self.speed = -self.speed
            self.rect.y += 30


# Different types of enemies
class RedEnemy(Enemy):
    def __init__(self, x, y):
        super(RedEnemy, self).__init__(x, y, "images/enemy-red.png")

class YellowEnemy(Enemy):
    def __init__(self, x, y):
        super(YellowEnemy, self).__init__(x, y, "images/enemy-yellow.png")


class WhiteEnemy(Enemy):
    def __init__(self, x, y):
        super(WhiteEnemy, self).__init__(x, y, "images/enemy-white.png")


class PurpleEnemy(Enemy):
    def __init__(self, x, y):
        super(PurpleEnemy, self).__init__(x, y, "images/enemy-purple.png")


class GreenEnemy(Enemy):
    def __init__(self, x, y):
        super(GreenEnemy, self).__init__(x, y, "images/enemy-green.png")


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = -5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# EnemyBullet class
class EnemyBullet(Bullet):
    def __init__(self, x, y):
        super(EnemyBullet, self).__init__(x, y)
        self.image = pygame.Surface((2, 8))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = 5  # Enemy bullets move downwards

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > size[1]:  # Destroy bullet when it goes off the bottom
            self.kill()


# Barrier class
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Barrier, self).__init__()
        self.image = pygame.Surface((50, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)


# Setup
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
barriers = pygame.sprite.Group()

# Create enemies with different types
enemy_classes = [RedEnemy, GreenEnemy, WhiteEnemy, PurpleEnemy, YellowEnemy]

for row in range(5):
    for col in range(10):
        enemy_class = enemy_classes[row % len(enemy_classes)]
        enemy = enemy_class(40 * col + 20, 30 * row + 20)
        enemies.add(enemy)

# Create barriers
barrier_positions = [(75, size[1] - 100), (175, size[1] - 100), (275, size[1] - 100), (375, size[1] - 100)]
for pos in barrier_positions:
    barrier = Barrier(pos[0], pos[1])
    barriers.add(barrier)

all_sprites = pygame.sprite.Group(player, *enemies, *barriers)

# Loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)

    # Timer
    keys = pygame.key.get_pressed()

    # Update
    player.update(keys)
    enemies.update()
    bullets.update()
    enemy_bullets.update()

    # Randomly shoot enemy bullets
    if random.random() < 0.01:
        enemy = random.choice(enemies.sprites())
        enemy_bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
        enemy_bullets.add(enemy_bullet)
        all_sprites.add(enemy_bullet)

    # Check for collisions
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        score += 10

    barrier_hits = pygame.sprite.groupcollide(bullets, barriers, True, False)
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    barrier_enemy_hits = pygame.sprite.groupcollide(enemy_bullets, barriers, True, False)

    for hit in player_hits:
        player.lives -= 1
        if player.lives <= 0:
            running = False

    # Draw the background
    screen.blit(bg, (0, 0))

    # Draw all sprites
    all_sprites.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display lives
    lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
    screen.blit(lives_text, (size[0] - 100, 10))

    # Redisplay
    pygame.display.flip()
    clock.tick(60)

# Save highscore
name = input("Enter your name: ")
c.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", (name, score))
conn.commit()

# Display highscores
c.execute("SELECT * FROM highscores ORDER BY score DESC LIMIT 10")
print("Highscores:")
for row in c.fetchall():
    print(f'{row[0]}: {row[1]}')

conn.close()
pygame.quit()
