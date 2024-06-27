__author__ = 'sdetmer'

# Import and Initialization
import pygame
import random
from pygame.locals import *
import sqlite3

pygame.init()

# Musik einrichten
pygame.mixer.music.load('sounds/GalaxyIntruderSoundtrack.mp3')
pygame.mixer.music.play(-1)

# Display configuration
size = (450, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('GalaxyIntruders')
bg = pygame.image.load("images/GalaxyIntrudersBG.jpg")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Highscore database setup
conn = sqlite3.connect('highscores.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS highscores
             (name TEXT, score INTEGER)''')
conn.commit()

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 24)  # Kleinere Schriftgröße für Buttons

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
def setup_game():
    global player, enemies, bullets, enemy_bullets, barriers, all_sprites, score
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
    score = 0


def draw_text_centered(text, font, color, screen, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def game_over_screen():
    name_input = ''
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    input_active = False
                elif event.key == K_BACKSPACE:
                    name_input = name_input[:-1]
                else:
                    name_input += event.unicode

        screen.fill(BLACK)
        draw_text_centered('Game Over', large_font, RED, screen, pygame.Rect(0, 50, size[0], 100))
        draw_text_centered('Enter Name:', font, WHITE, screen, pygame.Rect(0, 150, size[0], 50))
        draw_text_centered(name_input, font, WHITE, screen, pygame.Rect(0, 200, size[0], 50))
        pygame.display.flip()

    c.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", (name_input, score))
    conn.commit()
    show_highscores()


def show_highscores():
    c.execute("SELECT * FROM highscores ORDER BY score DESC LIMIT 10")
    highscores = c.fetchall()
    showing_scores = True
    while showing_scores:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if new_game_button.collidepoint(mouse_pos):
                    setup_game()
                    showing_scores = False
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return

        screen.fill(BLACK)
        draw_text_centered('Highscores', large_font, RED, screen, pygame.Rect(0, 50, size[0], 100))

        y_offset = 150
        for highscore in highscores:
            highscore_text = f'{highscore[0]}: {highscore[1]}'
            draw_text_centered(highscore_text, font, WHITE, screen, pygame.Rect(0, y_offset, size[0], 50))
            y_offset += 30

        new_game_button = pygame.Rect(size[0] // 2 - 150, size[1] - 100, 100, 50)
        quit_button = pygame.Rect(size[0] // 2 + 50, size[1] - 100, 100, 50)
        pygame.draw.rect(screen, WHITE, new_game_button)
        pygame.draw.rect(screen, WHITE, quit_button)

        new_game_text = button_font.render('New Game', True, BLACK)
        quit_text = button_font.render('Quit', True, BLACK)

        # Center the text on the buttons
        screen.blit(new_game_text, (new_game_button.x + (new_game_button.width - new_game_text.get_width()) // 2,
                                    new_game_button.y + (new_game_button.height - new_game_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                                quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

        pygame.display.flip()


# Main game loop
setup_game()
running = True
clock = pygame.time.Clock()

while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)
            playerShotSound = pygame.mixer.Sound('sounds/shoot-player.mp3')
            playerShotSound.play()

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
        enemyShotSound = pygame.mixer.Sound('sounds/shoot-enemy.mp3')
        enemyShotSound.play()

    # Check for collisions
    hits = pygame.sprite.groupcollide(bullets, enemies.enemies, True, True)
    for hit in hits:
        score += 10
        hitEnemySound = pygame.mixer.Sound('sounds/hit-enemy.mp3')
        hitEnemySound.play()

    barrier_hits = pygame.sprite.groupcollide(bullets, barriers, True, False)
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    barrier_enemy_hits = pygame.sprite.groupcollide(enemy_bullets, barriers, True, False)

    for hit in player_hits:
        player.lose_life()
        hitPlayerSound = pygame.mixer.Sound('sounds/hit-player.mp3')
        hitPlayerSound.play()
        if player.lives <= 0:
            game_over_screen()
            running = False

    # Check if any enemies have reached the barriers
    enemy_collides_with_barriers = pygame.sprite.groupcollide(enemies.enemies, barriers, False, False)
    if any(enemy_collides_with_barriers.values()):
        game_over_screen()
        running = False

    # Check if all enemies are defeated
    if enemies.is_empty():
        game_over_screen()
        running = False

    # Draw the background
    screen.blit(bg, (0, 0))

    # Draw all sprites
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display lives
    lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
    screen.blit(lives_text, (size[0] - 100, 10))

    # Redisplay
    pygame.display.flip()
    clock.tick(60)

conn.close()
pygame.quit()
