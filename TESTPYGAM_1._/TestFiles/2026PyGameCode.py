import pygame
import random
import pygame_menu

pygame.init()

# =========================================================
# SETTINGS
# =========================================================

schaal1 = 3
schaal = 0.15

# =========================================================
# ACHTERGROND
# =========================================================

achter2 = pygame.image.load(r"TESTPYGAM_1._\achtergrond\Man_Ray_Returns_001.webp")

achter1 = pygame.image.load(
    r"TESTPYGAM_1._\achtergrond\achtergrond.jpg"
)

achter1 = pygame.transform.scale(
    achter1,
    (
        achter1.get_width() * schaal1,
        achter1.get_height() * schaal1
    )
)

achtergrond = random.choice((achter1, achter2))

BREEDTE = achtergrond.get_width()
HOOGHTE = achtergrond.get_height()

frame = pygame.display.set_mode((BREEDTE, HOOGHTE))

pygame.display.set_caption("OOP Shooter Game")

# =========================================================
# SOUNDS
# =========================================================

HitSound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\soundscrate-slaphit.mp3'
)

GunSound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\soundscrate-classic-gun-shot-6.mp3'
)

JetcrashSFX = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\soundscrate-Rattling_Metal_Impact_3.mp3'
)

menusound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\Sarias Song - Zelda Ocarina of Time - Lost Woods - Part 42.mp3'
)

# =========================================================
# PLAYER CLASS
# =========================================================

class Jet:

    def __init__(self, x, y):

        schaal3 = 1.20

        self.image = pygame.image.load(
            r"TESTPYGAM_1._\skins jet\pixilart-drawing.png"
        )

        self.image = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() * schaal3,
                self.image.get_height() * schaal3
            )
        )

        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 5

    def move(self, toetsen):

        if toetsen[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if toetsen[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if toetsen[pygame.K_UP]:
            self.rect.y -= self.speed

        if toetsen[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Wrap around screen
        if self.rect.x > BREEDTE:
            self.rect.x = -100

        elif self.rect.x < -100:
            self.rect.x = BREEDTE

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# =========================================================
# BULLET CLASS
# =========================================================

class Bullet:

    def __init__(self, x, y):

        self.image = pygame.image.load(
            r'TESTPYGAM_1._\kogel.png'
        )

        self.image = pygame.transform.rotate(
            self.image,
            90
        )

        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# =========================================================
# ENEMY CLASS
# =========================================================

class Enemy:

    def __init__(self):

        self.doodlebob_image = pygame.image.load(
            r"TESTPYGAM_1._\DoodleBob_Stock_Art.webp"
        )

        self.doodlebob_image = pygame.transform.scale(
            self.doodlebob_image,
            (
                self.doodlebob_image.get_width() * schaal,
                self.doodlebob_image.get_height() * schaal
            )
        )

        self.patrick_image = pygame.image.load(
            r'TESTPYGAM_1._\Bikini-Patrick.png'
        )

        self.patrick_image = pygame.transform.scale(
            self.patrick_image,
            (
                self.patrick_image.get_width() // 4,
                self.patrick_image.get_height() // 4
            )
        )

        self.image = self.doodlebob_image

        self.rect = self.image.get_rect(topleft=(30, 20))

        self.hp = 5

        self.type = "Doodlebob"

        self.speed_x = 5
        self.speed_y = 3

    def move(self):

        # Doodlebob movement
        if self.type == "Doodlebob":

            self.rect.x += self.speed_x

            if self.rect.right >= BREEDTE:
                self.speed_x *= -1

            if self.rect.left <= 0:
                self.speed_x *= -1

        # Patrick movement
        elif self.type == "Patrick":

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.right >= BREEDTE or self.rect.left <= 0:
                self.speed_x = random.choice(
                    [-5, -4, -3, 3, 4, 5]
                )

            if self.rect.bottom >= HOOGHTE or self.rect.top <= 0:
                self.speed_y = random.choice(
                    [-5, -4, -3, 3, 4, 5]
                )

    def hit(self):

        self.hp -= 1

        if self.hp <= 0:

            self.image = self.patrick_image

            self.rect = self.image.get_rect(
                topleft=(30, 20)
            )

            self.type = "Patrick"

            self.hp = 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# =========================================================
# HP BAR CLASS
# =========================================================

class HPBar:

    def __init__(self):

        schaal5 = 3

        self.full = pygame.image.load(
            r'TESTPYGAM_1._\HP bar\fullHP_bar.png'
        )

        self.full = pygame.transform.scale(
            self.full,
            (
                self.full.get_width() * schaal5,
                self.full.get_height() * schaal5
            )
        )

        self.hit1 = pygame.image.load(
            r'TESTPYGAM_1._\HP bar\HP_barr_1e_hit.png'
        )

        self.hit1 = pygame.transform.scale(
            self.hit1,
            (
                self.hit1.get_width() * schaal5,
                self.hit1.get_height() * schaal5
            )
        )

        self.hit2 = pygame.image.load(
            r'TESTPYGAM_1._\HP bar\HP_bar_2e_hit.png'
        )

        self.hit2 = pygame.transform.scale(
            self.hit2,
            (
                self.hit2.get_width() * schaal5,
                self.hit2.get_height() * schaal5
            )
        )

        self.hit3 = pygame.image.load(
            r'TESTPYGAM_1._\HP bar\HP_bar_3e_hit.png'
        )

        self.hit3 = pygame.transform.scale(
            self.hit3,
            (
                self.hit3.get_width() * schaal5,
                self.hit3.get_height() * schaal5
            )
        )

        self.hit4 = pygame.image.load(
            r'TESTPYGAM_1._\HP bar\HP_bar_4e_hit.png'
        )

        self.hit4 = pygame.transform.scale(
            self.hit4,
            (
                self.hit4.get_width() * schaal5,
                self.hit4.get_height() * schaal5
            )
        )

        self.empty = pygame.image.load(
            r'TESTPYGAM_1._\HP bar\DoodleBobHealthBar.png'
        )

        self.empty = pygame.transform.scale(
            self.empty,
            (
                self.empty.get_width() * schaal5,
                self.empty.get_height() * schaal5
            )
        )

    def get_bar(self, hp):

        if hp == 5:
            return self.full

        elif hp == 4:
            return self.hit1

        elif hp == 3:
            return self.hit2

        elif hp == 2:
            return self.hit3

        elif hp == 1:
            return self.hit4

        else:
            return self.empty

# =========================================================
# GAME CLASS
# =========================================================

class Game:

    def __init__(self):

        self.clock = pygame.time.Clock()

        self.FPS = 60

        self.running = True

        self.player = Jet(380, 400)

        self.enemy = Enemy()

        self.hpbar = HPBar()

        self.bullets = []

        self.lastGunShotTime = 0

        self.lastHitTime = 0

        self.cooldownGunShotTime = 500

        self.cooldownHitTime = 1000

    def shoot(self):

        current_time = pygame.time.get_ticks()

        if current_time - self.lastGunShotTime > self.cooldownGunShotTime:

            GunSound.play()

            bullet = Bullet(
                self.player.rect.centerx,
                self.player.rect.top
            )

            self.bullets.append(bullet)

            self.lastGunShotTime = current_time

    def collisions(self):

        current_time = pygame.time.get_ticks()

        # Jet hit enemy
        if self.player.rect.colliderect(self.enemy.rect):

            if current_time - self.lastHitTime > self.cooldownHitTime:

                JetcrashSFX.play()

                self.enemy.hit()

                self.lastHitTime = current_time

        # Bullet hit enemy
        for bullet in self.bullets[:]:

            if self.enemy.rect.colliderect(bullet.rect):

                HitSound.play()

                self.enemy.hit()

                self.bullets.remove(bullet)

    def update(self):

        toetsen = pygame.key.get_pressed()

        self.player.move(toetsen)

        self.enemy.move()

        for bullet in self.bullets:
            bullet.move()

        self.collisions()

    def draw(self):

        frame.blit(achtergrond, (0, 0))

        self.enemy.draw(frame)

        self.player.draw(frame)

        for bullet in self.bullets:
            bullet.draw(frame)

        frame.blit(
            self.hpbar.get_bar(self.enemy.hp),
            (0, 350)
        )

        pygame.display.flip()

    def run(self):

        while self.running:

            self.clock.tick(self.FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        self.shoot()

            self.update()

            self.draw()

# =========================================================
# START GAME
# =========================================================

def start_game():

    menusound.stop()

    game = Game()

    game.run()

# =========================================================
# MENU
# =========================================================

menu = pygame_menu.Menu(
    'Eenvoudig Menu',
    BREEDTE,
    HOOGHTE,
    theme=pygame_menu.themes.THEME_SOLARIZED
)

menusound.play(-1)

menu.add.button('Start', start_game)

menu.add.button('Quit', pygame.quit)

menu.mainloop(frame)