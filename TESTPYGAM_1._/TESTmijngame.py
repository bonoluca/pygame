import pygame
import random
import pygame_menu
import math
import sys

pygame.init()

# =====================================
# SETTINGS
# =====================================

FPS = 60

# =====================================
# BACKGROUND
# =====================================

schaal_breedte = 1
schaal_hooghte = 2

achtergrond = pygame.image.load(
    r"TESTPYGAM_1._\achtergrond\Schermafbeelding 2026-05-28 104846.png"
)

achtergrond = pygame.transform.scale(
    achtergrond,
    (
        achtergrond.get_width() * schaal_breedte,
        achtergrond.get_height() * schaal_hooghte
    )
)

BREEDTE = achtergrond.get_width()
HOOGTE = achtergrond.get_height()

frame = pygame.display.set_mode((BREEDTE, HOOGTE))

pygame.display.set_caption("Cuphead Style Boss Fight")

# =====================================
# SOUNDS
# =====================================

HitSound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\soundscrate-slaphit.mp3'
)

GunSound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\soundscrate-classic-gun-shot-6.mp3'
)

CrashSound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\soundscrate-Rattling_Metal_Impact_3.mp3'
)

menusound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\Sarias Song - Zelda Ocarina of Time - Lost Woods - Part 42.mp3'
)

# =====================================
# BULLET CLASS
# =====================================

class Bullet:

    def __init__(self, x, y, width=15, height=15, image=None):

        self.rect = pygame.Rect(x, y, width, height)

        self.speed = 12

        self.image = image

    def update(self):

        self.rect.x += self.speed

    def draw(self, screen):

        if self.image:

            screen.blit(self.image, self.rect)

        elif self.rect.width >= 80:

            pygame.draw.ellipse(screen, (0, 200, 255), self.rect)

        else:

            pygame.draw.rect(screen, (0, 150, 255), self.rect)

# =====================================
# ENEMY BULLET
# =====================================

class EnemyBullet:

    def __init__(self, x, y, speed_x, speed_y):

        self.rect = pygame.Rect(x, y, 20, 20)

        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            self.rect
        )

# =====================================
# PLAYER
# =====================================

class Player:

    def __init__(self):

        schaal = 1.2

        self.image = pygame.image.load(
            r"TESTPYGAM_1._\skins jet\pixilart-drawing.png"
        )

        self.super_image = pygame.image.load(
            r"TESTPYGAM_1._\skin munitie\hadouken-hadoken-pixel-art-ryu-others-thumbnail.jpg"
        )

        self.mega_image = pygame.image.load(
            r"TESTPYGAM_1._\skin munitie\mega attack fireball.gif"
        )

        self.mega_image = pygame.transform.scale(
            self.mega_image,
            (250, 250)
        )

        self.super_image = pygame.transform.scale(
            self.super_image,
            (120, 120)
        )

        self.image = pygame.transform.rotate(self.image, -90)

        self.image = pygame.transform.scale(
            self.image,
            (
                self.image.get_width() * schaal,
                self.image.get_height() * schaal
            )
        )

        self.rect = pygame.Rect(
            200,
            300,
            self.image.get_width(),
            self.image.get_height()
        )

        self.speed = 6

        self.last_shot = 0
        self.shot_cooldown = 100

        # LIVES

        self.lives = 3

        # DAMAGE COOLDOWN

        self.last_hit = 0
        self.hit_cooldown = 1000

        # SUPER METER

        self.super_meter = 0
        self.max_meter = 5

        self.last_super = 0
        self.super_cooldown = 2000

        self.hit_counter = 0

    def movement(self):

        toetsen = pygame.key.get_pressed()

        if toetsen[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if toetsen[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if toetsen[pygame.K_UP]:
            self.rect.y -= self.speed

        if toetsen[pygame.K_DOWN]:
            self.rect.y += self.speed

        # SCHERM GRENZEN

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > BREEDTE:
            self.rect.right = BREEDTE

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HOOGTE:
            self.rect.bottom = HOOGTE

    def shoot(self, bullets):

        toetsen = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

        if toetsen[pygame.K_SPACE]:

            if current_time - self.last_shot > self.shot_cooldown:

                GunSound.play()

                bullet = Bullet(
                    self.rect.centerx,
                    self.rect.centery
                )

                bullets.append(bullet)

                self.last_shot = current_time

    def super_attack(self, bullets):

        toetsen = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

        if toetsen[pygame.K_x]:

            if current_time - self.last_super > self.super_cooldown:

                # MEGA MOVE

                if self.super_meter == 5:

                    mega_bullet = Bullet(
                        self.rect.centerx,
                        self.rect.centery,
                        250,
                        250,
                        self.mega_image
                    )

                    mega_bullet.speed = 20

                    mega_bullet.rect = self.mega_image.get_rect(
                        center=self.rect.center
                    )

                    bullets.append(mega_bullet)

                    self.super_meter = 0

                # NORMALE SUPER

                elif self.super_meter >= 1:

                    super_bullet = Bullet(
                        self.rect.centerx,
                        self.rect.centery,
                        120,
                        120,
                        self.super_image
                    )

                    super_bullet.speed = 18

                    super_bullet.rect = self.super_image.get_rect(
                        center=self.rect.center
                    )

                    bullets.append(super_bullet)

                    self.super_meter -= 1

                self.last_super = current_time

    def draw(self, screen):

        current_time = pygame.time.get_ticks()

        # KNIPPER EFFECT

        if current_time - self.last_hit < self.hit_cooldown:

            if current_time % 200 < 100:
                return

        screen.blit(self.image, self.rect)

# =====================================
# BOSS
# =====================================

class Boss:

    def __init__(self):

        schaal = 0.15

        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-3, 3])

        # =====================================
        # IMAGES
        # =====================================

        self.image_phase1 = pygame.image.load(
            r"TESTPYGAM_1._\DoodleBob_Stock_Art.webp"
        )

        self.image_phase1 = pygame.transform.scale(
            self.image_phase1,
            (
                int(self.image_phase1.get_width() * schaal),
                int(self.image_phase1.get_height() * schaal)
            )
        )

        self.image_phase2 = pygame.image.load(
            r"TESTPYGAM_1._\Bikini-Patrick.png"
        )

        self.image_phase2 = pygame.transform.scale(
            self.image_phase2,
            (
                self.image_phase2.get_width() // 4,
                self.image_phase2.get_height() // 4
            )
        )

        self.image = self.image_phase1

        # =====================================
        # SPAWN
        # =====================================

        self.rect = self.image.get_rect()

        self.rect.x = BREEDTE - self.rect.width - 50

        self.rect.y = random.randint(
            50,
            HOOGTE - self.rect.height - 50
        )

        # =====================================
        # GAME LOGIC
        # =====================================

        self.phase = 1
        self.hp = 10

        self.transition = False
        self.transition_timer = 0

        self.attack_timer = 0
        self.attack_cooldown = 1200

        self.direction = 1

    def update(self):

        # =====================================
        # PHASE 1
        # =====================================

        if self.phase == 1:

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            bounced = False

            if self.rect.left <= 0 or self.rect.right >= BREEDTE:

                self.speed_x *= -1

                bounced = True

            if self.rect.top <= 0 or self.rect.bottom >= HOOGTE:

                self.speed_y *= -1

                bounced = True

            if bounced:

                self.speed_x = random.choice([-5, -4, 4, 5])

                self.speed_y = random.choice([-3, -2, 2, 3])

            if self.rect.top < 0:
                self.rect.top = 0

            if self.rect.bottom > HOOGTE:
                self.rect.bottom = HOOGTE

        # =====================================
        # PHASE 2
        # =====================================

        elif self.phase == 2:

            self.rect.y += self.direction * 5

            if self.rect.top <= 0:
                self.direction = 1

            if self.rect.bottom >= HOOGTE:
                self.direction = -1

            self.rect.x = BREEDTE - self.rect.width - 50

    def attack(self, enemy_bullets):

        current_time = pygame.time.get_ticks()

        if current_time - self.attack_timer > self.attack_cooldown:

            self.attack_timer = current_time

            attack_type = random.randint(1, 3)

            # SPREAD SHOT

            if attack_type == 1:

                for i in range(-2, 3):

                    bullet = EnemyBullet(
                        self.rect.centerx,
                        self.rect.centery,
                        -8,
                        i * 2
                    )

                    enemy_bullets.append(bullet)

            # FAST SHOT

            elif attack_type == 2:

                bullet = EnemyBullet(
                    self.rect.centerx,
                    self.rect.centery,
                    -14,
                    0
                )

                enemy_bullets.append(bullet)

            # DASH ATTACK

            elif attack_type == 3:

                self.rect.x -= 150

    def take_damage(self):

        HitSound.play()

        self.hp -= 1

        print("Boss HP:", self.hp)

        if self.hp <= 0:

            # PHASE 2

            if self.phase == 1:

                self.transition = True

                self.transition_timer = pygame.time.get_ticks()

            # BOSS VERSLAGEN

            elif self.phase == 2:

                pygame.time.delay(1000)

                end_screen("YOU WIN")

    def start_phase2(self):

        self.phase = 2

        self.hp = 15

        self.image = pygame.transform.scale(
            self.image_phase2,
            (
                self.image_phase2.get_width() // 6,
                self.image_phase2.get_height() // 6
            )
        )

        self.rect = pygame.Rect(
            BREEDTE - self.image.get_width() - 50,
            200,
            self.image.get_width(),
            self.image.get_height()
        )

    def draw(self, screen):

        screen.blit(self.image, self.rect)

# =====================================
# END SCREEN
# =====================================

def end_screen(text):

    waiting = True

    big_font = pygame.font.SysFont(None, 100)

    small_font = pygame.font.SysFont(None, 50)

    while waiting:

        frame.blit(achtergrond, (0, 0))

        title = big_font.render(
            text,
            True,
            (255, 0, 0)
        )

        info = small_font.render(
            "Press R to Restart or ESC to Quit",
            True,
            (255, 255, 255)
        )

        frame.blit(
            title,
            (
                BREEDTE // 2 - title.get_width() // 2,
                HOOGTE // 2 - 100
            )
        )

        frame.blit(
            info,
            (
                BREEDTE // 2 - info.get_width() // 2,
                HOOGTE // 2
            )
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    start_game()
                    return

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

# =====================================
# GAME CLASS
# =====================================

class Game:

    def __init__(self):

        self.clock = pygame.time.Clock()

        self.running = True

        self.player = Player()

        self.boss = Boss()

        self.bullets = []

        self.enemy_bullets = []

        self.font = pygame.font.SysFont(None, 80)

        self.bg_x = 0

        self.scroll_speed = 2

    def update(self):

        self.player.movement()

        self.player.shoot(self.bullets)

        self.player.super_attack(self.bullets)

        self.boss.update()

        self.boss.attack(self.enemy_bullets)

        # PLAYER BULLETS

        for bullet in self.bullets[:]:

            bullet.update()

            if bullet.rect.colliderect(self.boss.rect):

                self.boss.take_damage()

                self.player.hit_counter += 1

                if self.player.hit_counter >= 3:

                    self.player.super_meter += 1

                    self.player.hit_counter = 0

                if self.player.super_meter > 5:

                    self.player.super_meter = 5

                self.bullets.remove(bullet)

            elif bullet.rect.left > BREEDTE:

                self.bullets.remove(bullet)

        # ENEMY BULLETS

        for bullet in self.enemy_bullets[:]:

            bullet.update()

            current_time = pygame.time.get_ticks()

            if bullet.rect.colliderect(self.player.rect):

                if (
                    current_time - self.player.last_hit
                    > self.player.hit_cooldown
                ):

                    self.player.lives -= 1

                    self.player.last_hit = current_time

                    CrashSound.play()

                self.enemy_bullets.remove(bullet)

            elif (
                bullet.rect.right < 0
                or bullet.rect.top > HOOGTE
                or bullet.rect.bottom < 0
            ):

                self.enemy_bullets.remove(bullet)

        # PLAYER CRASH

        current_time = pygame.time.get_ticks()

        if self.player.rect.colliderect(self.boss.rect):

            if (
                current_time - self.player.last_hit
                > self.player.hit_cooldown
            ):

                self.player.lives -= 1

                self.player.last_hit = current_time

                CrashSound.play()

        # GAME OVER

        if self.player.lives <= 0:

            self.running = False

            end_screen("GAME OVER")

        # PHASE 2 SCROLL

        if self.boss.phase == 2:

            self.bg_x -= self.scroll_speed

            if self.bg_x <= -BREEDTE:

                self.bg_x = 0

    def draw_ui(self):

        # HARTJES

        for i in range(self.player.lives):

            pygame.draw.rect(
                frame,
                (255, 0, 0),
                (20 + i * 50, 20, 35, 35),
                border_radius=10
            )

        # SUPER METER

        for i in range(self.player.max_meter):

            kleur = (50, 50, 50)

            if i < self.player.super_meter:

                kleur = (0, 100, 255)

            pygame.draw.rect(
                frame,
                kleur,
                (20 + i * 60, 70, 45, 25)
            )

    def draw(self):

        # BACKGROUND

        if self.boss.phase == 1:

            frame.blit(achtergrond, (0, 0))

        else:

            frame.blit(achtergrond, (self.bg_x, 0))

            frame.blit(
                achtergrond,
                (self.bg_x + BREEDTE, 0)
            )

        # DRAW OBJECTS

        self.player.draw(frame)

        self.boss.draw(frame)

        for bullet in self.bullets:

            bullet.draw(frame)

        for bullet in self.enemy_bullets:

            bullet.draw(frame)

        self.draw_ui()

        # PHASE TRANSITION

        if self.boss.transition:

            tekst = self.font.render(
                "NEXT PHASE",
                True,
                (255, 0, 0)
            )

            frame.blit(
                tekst,
                (
                    BREEDTE // 2 - 220,
                    HOOGTE // 2
                )
            )

            if (
                pygame.time.get_ticks()
                - self.boss.transition_timer
                > 3000
            ):

                self.boss.transition = False

                self.boss.start_phase2()

        pygame.display.flip()

    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.events()

            self.update()

            self.draw()

# =====================================
# START GAME
# =====================================

def start_game():

    menusound.stop()

    game = Game()

    game.run()

# =====================================
# QUIT GAME
# =====================================

def quit_game():

    pygame.quit()

    sys.exit()

# =====================================
# MENU
# =====================================

menu = pygame_menu.Menu(
    'Cuphead Boss Fight',
    BREEDTE,
    HOOGTE,
    theme=pygame_menu.themes.THEME_SOLARIZED
)

menusound.play(-1)

menu.add.button('Start', start_game)

menu.add.button('Quit', quit_game)

menu.mainloop(frame)