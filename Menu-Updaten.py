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
control_scheme = "AZERTY"

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
    r'TESTPYGAM_1._\sfx\peachooter.mp3'
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


# LaserWall = alleen wat een laser is (beweging + tekenen)
class LaserWall:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 200)
        self.speed = -4

    def update(self):
        self.rect.x += self.speed
    
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 255), self.rect)  # paars

class WeakLaser(LaserWall):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 1

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)  # randje

class LockRocket:

    def __init__(self, x, y, target):
        self.rect = pygame.Rect(x, y, 50, 30)

        self.target_x = target.rect.centerx
        self.target_y = target.rect.centery

        self.speed = 5

        dx = self.target_x - x
        dy = self.target_y - y
        dist = math.hypot(dx, dy)

        if dist != 0:
            self.speed_x = (dx / dist) * self.speed
            self.speed_y = (dy / dist) * self.speed
        else:
            self.speed_x = 0
            self.speed_y = 0

        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def should_destroy(self):
        return pygame.time.get_ticks() - self.spawn_time > 12000

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 80, 0), self.rect)
        pygame.draw.rect(screen, (255, 255, 0), self.rect, 3)

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
        self.shot_cooldown = 70

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

        if control_scheme == "AZERTY":

            if toetsen[pygame.K_q]:
                self.rect.x -= self.speed

            if toetsen[pygame.K_d]:
                self.rect.x += self.speed

            if toetsen[pygame.K_z]:
                self.rect.y -= self.speed

            if toetsen[pygame.K_s]:
                self.rect.y += self.speed

        else:  # QWERTY

            if toetsen[pygame.K_a]:
                self.rect.x -= self.speed

            if toetsen[pygame.K_d]:
                self.rect.x += self.speed

            if toetsen[pygame.K_w]:
                self.rect.y -= self.speed

            if toetsen[pygame.K_s]:
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
        if control_scheme == "AZERTY":

            if toetsen[pygame.K_a]:

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
        else:
            if toetsen[pygame.K_q]:

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

class MiniDoodle:

    def __init__(self, x, y, target):

        schaal = 0.08

        self.image = pygame.image.load(
            r"TESTPYGAM_1._\DoodleBob_Stock_Art.webp"
        )

        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * schaal),
                int(self.image.get_height() * schaal)
            )
        )

        self.rect = self.image.get_rect(topleft=(x, y))

        self.target = target

        self.moving = False

        self.wait_time = random.randint(2000, 8000)
        self.spawn_time = pygame.time.get_ticks()

        self.speed_x = 0
        self.speed_y = 0
        self.speed = 4

        self.last_shot = 0
        self.shot_cooldown = 1200

        # ✅ voor despawn
        self.alive = True

        self.hp = 3  # aantal hits nodig

    def update(self, enemy_bullets):

        current_time = pygame.time.get_ticks()

        # ✅ start bewegen na delay
        if not self.moving and current_time - self.spawn_time > self.wait_time:

            self.moving = True

            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)

            if dist != 0:
                self.speed_x = (dx / dist) * self.speed
                self.speed_y = (dy / dist) * self.speed

        # ✅ bewegen
        if self.moving:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

        # ✅ schieten
        if current_time - self.last_shot > self.shot_cooldown:

            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)

            if dist != 0:
                speed_x = (dx / dist) * 6
                speed_y = (dy / dist) * 6
            else:
                speed_x = -6
                speed_y = 0

            bullet = EnemyBullet(
                self.rect.centerx,
                self.rect.centery,
                speed_x,
                speed_y
            )

            enemy_bullets.append(bullet)
            self.last_shot = current_time

        # ✅ verwijderen als buiten scherm
        if self.rect.right < 0 or self.rect.left > BREEDTE or self.rect.bottom < 0 or self.rect.top > HOOGTE:
            self.alive = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

        self.phase2_stage = 0
        self.big_mode = False

    def update(self):

        # =====================================
        # PHASE 1
        # =====================================

        if self.phase == 1:
            # Alleen horizontaal bewegen
            self.rect.x += self.speed_x

            # Botsen links/rechts
            if self.rect.left <= 0 or self.rect.right >= BREEDTE:
                self.speed_x *= -1  # richting omdraaien

            # Binnen scherm houden
            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > BREEDTE:
                self.rect.right = BREEDTE


        # =====================================
        # PHASE 2
        # =====================================

        elif self.phase == 2:

            if self.big_mode:
                # ✅ blijft stil in het midden rechts
                self.rect.x = BREEDTE - self.rect.width - 50
                self.rect.y = HOOGTE // 2 - self.rect.height // 2

            else:
                # oude beweging
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

            if self.phase == 2 and self.hp <= 60:
                attack_type = 1  # ✅ ALTIJD multishot
            else:
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

                if self.phase == 2 and self.hp <= 80 and self.hp > 60:

                    amount = 3
                    gap = HOOGTE // amount  # ✅ verdeelt perfect over scherm

                    weak_index = random.randint(0, amount - 1)

                    for i in range(amount):

                        y_pos = i * gap + 10   # kleine offset zodat het niet tegen de rand zit

                        if i == weak_index:
                            laser = WeakLaser(self.rect.left, y_pos)
                        else:
                            laser = LaserWall(self.rect.left, y_pos)

                        enemy_bullets.append(laser)





    def take_damage(self):

        HitSound.play()

        self.hp -= 1
        if self.phase == 2:
            new_stage = (100 - self.hp) // 20
            if new_stage > self.phase2_stage:
                self.phase2_stage = new_stage
                self.phase2_event()


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

        self.hp = 100

        self.image = pygame.transform.scale(
            self.image_phase2,
            (
                self.image_phase2.get_width() // 3,
                self.image_phase2.get_height() // 3
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
    
    def phase2_event(self):
        print("Phase 2 event:", self.phase2_stage)

        if self.phase2_stage == 1:
            print("Boss wordt sneller!")
            self.attack_cooldown = 900

        elif self.phase2_stage == 2:

            print("STAGE 2: BOSS WORDT GROOT EN STIL")

            self.attack_cooldown = 700
            self.big_mode = True


        elif self.phase2_stage == 3:
            print("Chaos mode!")
            self.attack_cooldown = 500

        elif self.phase2_stage == 4:
            print("Rage mode!")
            self.attack_cooldown = 300

        elif self.phase2_stage == 5:
            print("FINAL MODE!!!")
            self.attack_cooldown = 200

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

        self.lasers = []
        self.rockets = []

        self.god_mode = False
        self.debug_damage = False

        self.spawned_75 = False
        self.spawned_70 = False
        self.spawned_65 = False

        self.minis = []
        self.spawned_doodles = False
        self.last_doodle_spawn = 0
        self.doodle_delay = 4000  # 4 seconden

    

    def update(self):

        self.player.movement()
        self.player.shoot(self.bullets)
        self.player.super_attack(self.bullets)

        self.boss.update()
        self.boss.attack(self.enemy_bullets)

        # =====================================
        # PLAYER BULLETS
        # =====================================

        for bullet in self.bullets[:]:


            bullet.update()

            # =====================================
            # ✅ HIT OP BOSS
            # =====================================
            if bullet.rect.colliderect(self.boss.rect):

                damage = 5 if self.debug_damage else 1

                for _ in range(damage):
                    self.boss.take_damage()

                self.player.hit_counter += 1

                if self.player.hit_counter >= 3:
                    self.player.super_meter += 1
                    self.player.hit_counter = 0

                if self.player.super_meter > 5:
                    self.player.super_meter = 5

                self.bullets.remove(bullet)
                continue


            # =====================================
            # ✅ HIT OP DOODLEBOBS
            # =====================================
            hit_mini = False

            for mini in self.minis[:]:
                if bullet.rect.colliderect(mini.rect):

                    mini.hp -= 1

                    if mini.hp <= 0:
                        print("Mini doodlebob destroyed 💥")
                        self.minis.remove(mini)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    hit_mini = True
                    break

            if hit_mini:
                continue


            # =====================================
            # ✅ HIT OP WEAK LASER
            # =====================================
            for enemy in self.enemy_bullets[:]:
                if isinstance(enemy, WeakLaser) and bullet.rect.colliderect(enemy.rect):

                    enemy.hp -= 1

                    if enemy.hp <= 0:
                        self.enemy_bullets.remove(enemy)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    break




            # ✅ UIT SCHERM
            if bullet.rect.left > BREEDTE:
                self.bullets.remove(bullet)

        # =====================================
        # ROCKET SPAWN ✅ (NA DAMAGE!)
        # =====================================

        if self.boss.phase == 2:

            # ✅ 75 HP → 1 rocket
            if self.boss.hp <= 75 and not self.spawned_75:

                rocket = LockRocket(
                    self.boss.rect.centerx,
                    self.boss.rect.centery,
                    self.player
                )

                self.rockets.append(rocket)
                self.spawned_75 = True
                print("Rocket 1 spawned")

            # ✅ 70 HP → 2e rocket
            if self.boss.hp <= 70 and not self.spawned_70:

                rocket = LockRocket(
                    self.boss.rect.centerx,
                    self.boss.rect.centery,
                    self.player
                )

                self.rockets.append(rocket)
                self.spawned_70 = True
                print("Rocket 2 spawned")

            # ✅ 65 HP → 3e rocket
            if self.boss.hp <= 65 and not self.spawned_65:

                rocket = LockRocket(
                    self.boss.rect.centerx,
                    self.boss.rect.centery,
                    self.player
                )

                self.rockets.append(rocket)
                self.spawned_65 = True
                print("Rocket 3 spawned")

        
        # =====================================
        # DOODLEBOB SPAWN (STAGE 2)
        # =====================================

        if self.boss.phase == 2 and self.boss.hp <= 60 and not self.spawned_doodles:

            print("DoodleBobs spawned 😈")

            # boven boss
            top = MiniDoodle(
                self.boss.rect.left,
                self.boss.rect.top - 60,
                self.player
            )

            # onder boss
            bottom = MiniDoodle(
                self.boss.rect.left,
                self.boss.rect.bottom + 60,
                self.player
            )

            self.minis.append(top)
            self.minis.append(bottom)

            self.spawned_doodles = True
        
        # =====================================
        # DOODLEBOB RESPAWN SYSTEM
        # =====================================

        current_time = pygame.time.get_ticks()

        if self.boss.phase == 2 and self.boss.hp <= 60:

            # check hoeveel er nog leven
            alive_minis = [m for m in self.minis if m.alive]

            # als geen meer over → respawn na delay
            if len(alive_minis) == 0 and current_time - self.last_doodle_spawn > self.doodle_delay:

                print("Respawning doodlebobs 😈")

                top = MiniDoodle(
                    self.boss.rect.left,
                    self.boss.rect.top - 60,
                    self.player
                )

                bottom = MiniDoodle(
                    self.boss.rect.left,
                    self.boss.rect.bottom + 60,
                    self.player
                )

                self.minis.append(top)
                self.minis.append(bottom)

                self.last_doodle_spawn = current_time

        # =====================================
        # ROCKETS UPDATE
        # =====================================

        current_time = pygame.time.get_ticks()

        for rocket in self.rockets[:]:

            rocket.update()

            if rocket.rect.colliderect(self.player.rect):

                if current_time - self.player.last_hit > self.player.hit_cooldown:
                    if not self.god_mode:
                        self.player.lives -= 1

                    self.player.last_hit = current_time
                    CrashSound.play()

                self.rockets.remove(rocket)

            elif rocket.should_destroy():
                self.rockets.remove(rocket)

        
        # =====================================
        # DOODLEBOBS UPDATE
        # =====================================

        for mini in self.minis[:]:

            mini.update(self.enemy_bullets)

            if mini.rect.colliderect(self.player.rect):

                if current_time - self.player.last_hit > self.player.hit_cooldown:
                    if not self.god_mode:
                        self.player.lives -= 1

                    self.player.last_hit = current_time
                    CrashSound.play()

            # ✅ verwijderen als dood
            if not mini.alive:
                self.minis.remove(mini)


        # =====================================
        # ENEMY BULLETS
        # =====================================

        for bullet in self.enemy_bullets[:]:

            bullet.update()

            if bullet.rect.colliderect(self.player.rect):

                if current_time - self.player.last_hit > self.player.hit_cooldown:
                    if not self.god_mode:
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

        # =====================================
        # PLAYER CRASH (boss aanraken)
        # =====================================

        if self.player.rect.colliderect(self.boss.rect):

            if current_time - self.player.last_hit > self.player.hit_cooldown:
                if not self.god_mode:
                    self.player.lives -= 1

                self.player.last_hit = current_time
                CrashSound.play()

        # =====================================
        # GAME OVER
        # =====================================

        if self.player.lives <= 0:
            self.running = False
            end_screen("GAME OVER")

        # =====================================
        # PHASE 2 SCROLL
        # =====================================

        if self.boss.phase == 2:

            self.bg_x -= self.scroll_speed

            if self.bg_x <= -BREEDTE:
                self.bg_x = 0


    def draw_ui(self):

        if self.god_mode:
            txt = self.font.render("GOD MODE", True, (255, 255, 0))
            frame.blit(txt, (BREEDTE - 250, 20))

        if self.debug_damage:
            txt = self.font.render("DMG x5", True, (255, 100, 100))
            frame.blit(txt, (BREEDTE - 250, 80))


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
        
        # ✅ NIEUW: rockets tekenen
        for rocket in self.rockets:
            rocket.draw(frame)
        
        for mini in self.minis:
            mini.draw(frame)


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
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    self.god_mode = not self.god_mode
                    print("God mode:", self.god_mode)

                if event.key == pygame.K_o:
                    self.debug_damage = not self.debug_damage
                    print("Debug damage:", self.debug_damage)


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



def quit_game():

    pygame.quit()

    sys.exit()




def set_controls(value, scheme):
    global control_scheme
    control_scheme = scheme
    print("Controls ingesteld op:", control_scheme)






class MainMenu:

    def __init__(self):

        # 🎨 achtergrond
        self.background = pygame.image.load(
            r"TESTPYGAM_1._\achtergrond\Background_Menu\cuphead_00.png"
        )
        self.background = pygame.transform.scale(
            self.background,
            (BREEDTE, HOOGTE)
        )

        # animatie
        self.anim_time = 0

        # 🎬 film grain
        self.grain_surface = pygame.Surface((BREEDTE, HOOGTE))
        self.grain_surface.set_alpha(25)

        # ➤ selectie pijltje
        self.arrow_font = pygame.font.SysFont(None, 60)

        # 🎨 THEME
        self.theme = pygame_menu.themes.THEME_SOLARIZED.copy()

        self.theme.background_color = (0, 0, 0, 0)
        self.theme.title_background_color = (0, 0, 0, 0)
        self.theme.title_font_color = (0, 0, 0, 0)

        # 🎨 betere kleuren (minder “clean”)
        self.theme.widget_background_color = (240, 240, 240)
        self.theme.widget_font_color = (0, 0, 0)
        self.theme.widget_background_color_hover = (255, 220, 100)
        self.theme.widget_font_color_hover = (200, 0, 0)

        self.theme.widget_border_color = (0, 0, 0)
        self.theme.widget_border_width = 3
        self.theme.widget_border_radius = 15
        self.theme.widget_padding = 20
        self.theme.widget_font_size = 45

        self.theme.widget_width = 380
        self.theme.widget_alignment = pygame_menu.locals.ALIGN_RIGHT
        self.theme.widget_margin = (-10, 30)

        # 🎮 MENU
        self.menu = pygame_menu.Menu('', BREEDTE, HOOGTE, theme=self.theme)

        # ⚙️ SETTINGS MENU
        self.settings_menu = pygame_menu.Menu(
            'Settings',
            BREEDTE,
            HOOGTE,
            theme=self.theme
        )

        self.settings_menu.add.selector(
            'Controls: ',
            [('AZERTY (Default)', "AZERTY"), ('QWERTY', "QWERTY")],
            onchange=set_controls
        )

        self.settings_menu.add.button('BACK', pygame_menu.events.BACK)

        # ✅ KNOPPEN
        self.menu.add.vertical_margin(100)

        self.menu.add.button('START', start_game)
        self.menu.add.button('SETTINGS', self.settings_menu)
        self.menu.add.button('QUIT', quit_game)

    # 🎬 film grain
    def draw_grain(self):

        self.grain_surface.fill((0, 0, 0))

        for _ in range(250):  # lager = subtieler
            x = random.randint(0, BREEDTE - 1)
            y = random.randint(0, HOOGTE - 1)

            shade = random.randint(160, 255)
            self.grain_surface.set_at((x, y), (shade, shade, shade))

    # 🎮 DRAW
    def draw_background(self):

        self.anim_time += 0.03

        # 🎬 zachte beweging
        bounce = math.sin(self.anim_time) * 3
        shake_x = math.sin(self.anim_time * 2) * 1.2
        shake_y = math.cos(self.anim_time * 2) * 1.2

        frame.fill((0, 0, 0))

        # 🎨 achtergrond
        frame.blit(
            self.background,
            (int(shake_x), int(bounce + shake_y))
        )

        # 🌑 subtiele shadow (depth)
        shadow = pygame.Surface((BREEDTE, HOOGTE))
        shadow.set_alpha(30)
        shadow.fill((0, 0, 0))
        frame.blit(shadow, (2, 2))

        # 🎬 film grain
        self.draw_grain()
        frame.blit(self.grain_surface, (0, 0))

        # 🎯 selectie pijltje
        selected = self.menu.get_current().get_selected_widget()

        if selected:
            rect = selected.get_rect()

            arrow = self.arrow_font.render("->", True, (255, 255, 255))

            frame.blit(
                arrow,
                (rect.x - 40, rect.y + 10)
            )

    def run(self):

        if not pygame.mixer.get_busy():
            menusound.play(-1)

        self.menu.mainloop(frame, bgfun=self.draw_background)


# START
menu = MainMenu()
menu.run()