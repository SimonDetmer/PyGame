
#ToDO
# - Highscoreeingabe und anschließende Highscore-Tabelle mit New Game Button im Screen

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
        self.images = {
            3: pygame.image.load("images/player.png"),
            2: pygame.image.load("images/player-2Lives.png"),
            1: pygame.image.load("images/player-1Live.png")
        }
        self.image = pygame.transform.scale(self.images[3], (50, 30))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (size[0] // 2, size[1] - 10)
        self.speed = 5
        self.lives = 3

    def update(self, keys):
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < size[0]:
            self.rect.x += self.speed

    def lose_life(self):
        self.lives -= 1
        if self.lives > 0:
            self.image = pygame.transform.scale(self.images[self.lives], (50, 30))
        else:
            self.kill()


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1

    def update(self, direction):
        self.rect.x += self.speed * direction


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


# EnemyGroup class
class EnemyGroup:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.direction = 1

    def add(self, enemy):
        self.enemies.add(enemy)

    def update(self):
        for enemy in self.enemies:
            enemy.update(self.direction)

        # Check if any enemy hits the screen boundary
        change_direction = False
        for enemy in self.enemies:
            if enemy.rect.right >= size[0] or enemy.rect.left <= 0:
                change_direction = True
                break

        # Change direction if needed and move enemies down
        if change_direction:
            self.direction *= -1
            for enemy in self.enemies:
                enemy.rect.y += 10

    def is_empty(self):
        return len(self.enemies) == 0


# Setup
player = Player()
enemies = EnemyGroup()
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

all_sprites = pygame.sprite.Group(player, *barriers)
all_sprites.add(*enemies.enemies)

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
        enemy = random.choice(enemies.enemies.sprites())
        enemy_bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
        enemy_bullets.add(enemy_bullet)
        all_sprites.add(enemy_bullet)

    # Check for collisions
    hits = pygame.sprite.groupcollide(bullets, enemies.enemies, True, True)
    for hit in hits:
        score += 10

    barrier_hits = pygame.sprite.groupcollide(bullets, barriers, True, False)
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    barrier_enemy_hits = pygame.sprite.groupcollide(enemy_bullets, barriers, True, False)

    for hit in player_hits:
        player.lose_life()
        if player.lives <= 0:
            running = False

    # Check if any enemies have reached the barriers
    enemy_collides_with_barriers = pygame.sprite.groupcollide(enemies.enemies, barriers, False, False)
    if any(enemy_collides_with_barriers.values()):
        running = False

    # Check if all enemies are defeated
    if enemies.is_empty():
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

# Save Highscore
if score > 0:  # Nur Highscore speichern, wenn Punktzahl größer als 0 ist
    name = input("Gib deinen Namen ein: ")
    c.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

# Display highscores
c.execute("SELECT * FROM highscores ORDER BY score DESC LIMIT 10")
highscores = c.fetchall()
print("Highscores:")
for highscore in highscores:
    print(f"{highscore[0]}: {highscore[1]}")

conn.close()
pygame.quit()

