import pygame
from pygame import image, transform
import sys
import random

pygame.init()

# GameSprite class
class GameSprite:
    def __init__(self, player_image, x, y, speed):
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Player class
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - 65:
            self.rect.x += self.speed


# Enemy class
class Enemy(GameSprite):
    def update(self):
        global missed

        self.rect.y += self.speed

        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH - 65)
            missed += 1


# Asteroid class
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-100, 0)
            self.rect.x = random.randint(0, WIDTH - 65)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = transform.scale(image.load("bullet.png"), (20, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()


# Window setup
WIDTH = 700
HEIGHT = 500

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

background = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))

# Sounds
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound("fire.ogg")

# Clock
clock = pygame.time.Clock()
FPS = 60

# FONT FIX
font = pygame.font.SysFont('Arial', 36)

# Game variables
missed = 0
score = 0
game_over = False
win = False

# Reload system
shots_fired = 0
max_shots = 5

reload_time = 3000  # milliseconds
last_reload = 0
reloading = False

# Create player
player = Player("rocket.png", 300, 400, 5)

# Create enemies
enemies = []

for i in range(5):
    enemy = Enemy(
        "ufo.png",
        random.randint(0, WIDTH - 65),
        random.randint(-100, 0),
        random.randint(1, 3)
    )

    enemies.append(enemy)

# Create asteroids
asteroids = []

for i in range(3):
    asteroid = Asteroid(
        "asteroid.png",
        random.randint(0, WIDTH - 65),
        random.randint(-150, 0),
        random.randint(1, 2)
    )

    asteroids.append(asteroid)

# Bullet group
bullets = pygame.sprite.Group()

# Game loop
running = True

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:

                current_time = pygame.time.get_ticks()

                if not reloading:

                    bullet = Bullet(player.rect.centerx, player.rect.top)

                    bullets.add(bullet)

                    shoot_sound.play()

                    shots_fired += 1

                    if shots_fired >= max_shots:
                        reloading = True
                        last_reload = current_time

    # Game logic
    if not game_over:

        current_time = pygame.time.get_ticks()

        # Reload timer
        if reloading:

            if current_time - last_reload >= reload_time:
                reloading = False
                shots_fired = 0

        # Update player
        player.update()

        # Update enemies
        for enemy in enemies:
            enemy.update()

        # Update asteroids
        for asteroid in asteroids:
            asteroid.update()

        # Update bullets
        bullets.update()

        # Bullet collisions
        for bullet in bullets:

            for enemy in enemies:

                if bullet.rect.colliderect(enemy.rect):

                    bullet.kill()

                    enemy.rect.y = 0
                    enemy.rect.x = random.randint(0, WIDTH - 65)

                    score += 1

        # Collision with enemies
        for enemy in enemies:

            if player.rect.colliderect(enemy.rect):
                game_over = True

        # Collision with asteroids
        for asteroid in asteroids:

            if player.rect.colliderect(asteroid.rect):
                game_over = True

        # Lose condition
        if missed >= 10:
            game_over = True

        # Win condition
        if score >= 15:
            win = True
            game_over = True

    # Drawing
    window.blit(background, (0, 0))

    if not game_over:

        player.draw()

        for enemy in enemies:
            enemy.draw()

        for asteroid in asteroids:
            asteroid.draw()

        bullets.draw(window)

        # Text
        text_missed = font.render(
            f"Missed: {missed}",
            True,
            (255, 255, 255)
        )

        text_score = font.render(
            f"Hits: {score}",
            True,
            (255, 255, 255)
        )

        window.blit(text_missed, (10, 10))
        window.blit(text_score, (10, 50))

        # Reload message
        if reloading:

            reload_text = font.render(
                "Wait, reload...",
                True,
                (255, 255, 0)
            )

            window.blit(
                reload_text,
                (WIDTH // 2 - 120, HEIGHT - 50)
            )

    else:

        if win:

            text = font.render(
                "YOU WIN!",
                True,
                (0, 255, 0)
            )

        else:

            text = font.render(
                "YOU LOSE!",
                True,
                (255, 0, 0)
            )

        window.blit(
            text,
            (WIDTH // 2 - 100, HEIGHT // 2)
        )

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()