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

achtergrond_fase1 = pygame.image.load(
    r"TESTPYGAM_1._\achtergrond\ground afb.png"
)

achtergrond_fase2 = pygame.image.load(
    r"TESTPYGAM_1._\achtergrond\Schermafbeelding 2026-05-28 104846.png"                    
)




achtergrond_fase1 = pygame.transform.scale(
    achtergrond_fase1,
    (
        achtergrond_fase1.get_width() * schaal_breedte,
        achtergrond_fase1.get_height() * schaal_hooghte
    )
)

BREEDTE = achtergrond_fase1.get_width()
HOOGTE = achtergrond_fase1.get_height()

achtergrond_fase2 = pygame.transform.scale(
    achtergrond_fase2,
    (BREEDTE, HOOGTE)
)


frame = pygame.display.set_mode((BREEDTE, HOOGTE))

pygame.display.set_caption("Cuphead Style Boss Fight")

# =====================================
# SOUNDS
# =====================================

HitSound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\soundscrate-slaphit.mp3'
)

GunSound = pygame.mixer.Sound(
    r'TESTPYGAM_1._\sfx\pew sound.wav'
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
        self.rect = pygame.Rect(x, y, 40, 100)
        self.speed = -7

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
        self.target = target
        self.rect = pygame.Rect(x, y, 50, 30)

        self.speed = 3.5
        self.turn_speed = 0.08

        self.delay = 1000
        self.spawn_time = pygame.time.get_ticks()

        self.speed_x = -5
        self.speed_y = 0

    def should_destroy(self):
        return pygame.time.get_ticks() - self.spawn_time > 4000

    def update(self):

        current_time = pygame.time.get_ticks()

        # eerst recht vliegen
        if current_time - self.spawn_time < self.delay:
            self.rect.x += self.speed_x
            return

        # target volgen
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist != 0:
            target_vx = (dx / dist) * self.speed
            target_vy = (dy / dist) * self.speed

            self.speed_x += (target_vx - self.speed_x) * self.turn_speed
            self.speed_y += (target_vy - self.speed_y) * self.turn_speed

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 120, 0), self.rect)
        pygame.draw.rect(screen, (255, 255, 0), self.rect, 2)



class Spike:

    def __init__(self, x, y):
        self.x = x
        self.base_y = y

        self.max_height = 80
        self.width = 40

        self.rect = pygame.Rect(x, y, self.width, 0)

        # ⚠️ eerst warning
        self.warning_time = 600  # ms
        self.spawn_time = pygame.time.get_ticks()

        self.grow_speed = 20
        self.duration = 2500

        self.active = True
        self.growing = False

    def update(self):

        current_time = pygame.time.get_ticks()

        # ⏳ wachten
        if not self.growing:
            if current_time - self.spawn_time > self.warning_time:
                self.growing = True
            return

        # 🌱 groeien
        if self.rect.height < self.max_height:
            self.rect.y -= self.grow_speed
            self.rect.height += self.grow_speed

        # ⌛ verdwijnen
        if current_time - self.spawn_time > self.warning_time + self.duration:
            self.active = False

    def draw(self, screen):

        current_time = pygame.time.get_ticks()

        # ⚠️ warning tekenen
        if not self.growing:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.x, self.base_y - 10, self.width, 10)
            )

        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)

# =====================================
# PLAYER
# =====================================

class Player:

    def __init__(self):

        
        self.hitbox = pygame.Rect(0, 0, 25, 35)

        # SPRITE SHEET LADEN
        self.sprite_sheet = pygame.image.load(
            r"TESTPYGAM_1._\skins jet\llama.png"
        ).convert_alpha()

        self.frames = []

        # bereken grootte per frame
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()

        frame_width = sheet_width // 2
        frame_height = sheet_height // 3

        # frames eruit knippen
        for row in range(3):
            for col in range(2):

                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(
                        col * frame_width,
                        row * frame_height,
                        frame_width,
                        frame_height
                    )
                )

                frame = pygame.transform.scale(frame, (100, 100))



                self.frames.append(frame)

        # =====================================
        # JET SPRITE (phase 2)
        # =====================================

        self.jet_sheet = pygame.image.load(
            r"TESTPYGAM_1._\skins jet\llama rocket boots.png"
        ).convert_alpha()

        self.jet_frames = []

        sheet_width = self.jet_sheet.get_width()
        sheet_height = self.jet_sheet.get_height()

        frame_width = sheet_width // 2
        frame_height = sheet_height // 3

        for row in range(3):
            for col in range(2):

                frame = self.jet_sheet.subsurface(
                    pygame.Rect(
                        col * frame_width,
                        row * frame_height,
                        frame_width,
                        frame_height
                    )
                )

                frame = pygame.transform.scale(frame, (100, 100))



                self.jet_frames.append(frame)


        # animatie
        self.current_frame = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]

        self.current_frame_jet = 0


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

        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False

        self.direction = 1  # 1 = rechts, -1 = links



    def movement(self, phase):

        toetsen = pygame.key.get_pressed()
        moving = False

        # =====================================
        # PHASE 1 → LOPEN + SPRINGEN
        # =====================================
        if phase == 1:

            if toetsen[pygame.K_q]:
                self.rect.x -= self.speed
                self.direction = -1
                moving = True

            if toetsen[pygame.K_d]:
                self.rect.x += self.speed
                self.direction = 1
                moving = True


            # springen
            if toetsen[pygame.K_z] and self.on_ground:
                self.velocity_y = self.jump_power
                self.on_ground = False

            # gravity
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            ground_level = HOOGTE - 120

            if self.rect.bottom >= ground_level:
                self.rect.bottom = ground_level
                self.velocity_y = 0
                self.on_ground = True

        # =====================================
        # PHASE 2 → VLIEGEN (JET)
        # =====================================
        else:

            if toetsen[pygame.K_q]:
                self.rect.x -= self.speed
                self.direction = -1
                moving = True

            if toetsen[pygame.K_d]:
                self.rect.x += self.speed
                self.direction = 1
                moving = True


            if toetsen[pygame.K_z]:
                self.rect.y -= self.speed
                moving = True

            if toetsen[pygame.K_s]:
                self.rect.y += self.speed
                moving = True

        # =====================================
        # ANIMATIE SYSTEM
        # =====================================
        if phase == 1:

            if moving:
                self.current_frame += self.animation_speed

                if self.current_frame >= len(self.frames):
                    self.current_frame = 0

                self.image = self.frames[int(self.current_frame)]
            else:
                self.current_frame = 0
                self.image = self.frames[0]

        else:

            if moving:
                self.current_frame_jet += self.animation_speed

                if self.current_frame_jet >= len(self.jet_frames):
                    self.current_frame_jet = 0

                self.image = self.jet_frames[int(self.current_frame_jet)]
            else:
                self.current_frame_jet = 0
                self.image = self.jet_frames[0]

        # =====================================
        # SCHERM GRENZEN
        # =====================================
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > BREEDTE:
            self.rect.right = BREEDTE

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HOOGTE:
            self.rect.bottom = HOOGTE
        
        # hitbox centreren in player
        self.hitbox.center = self.rect.center


        


    def shoot(self, bullets):

        toetsen = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

        if toetsen[pygame.K_SPACE]:

            if current_time - self.last_shot > self.shot_cooldown:

                GunSound.play()

                if self.direction == 1:
                    x = self.rect.right
                else:
                    x = self.rect.left

                bullet = Bullet(
                    x,
                    self.rect.centery
                )

                bullet.speed = 12 * self.direction


                bullets.append(bullet)

                self.last_shot = current_time

    def super_attack(self, bullets):

        toetsen = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

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

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        current_time = pygame.time.get_ticks()

        # KNIPPER EFFECT

        if current_time - self.last_hit < self.hit_cooldown:

            if current_time % 200 < 100:
                return

        image = self.image

        if self.direction == -1:
            image = pygame.transform.flip(self.image, True, False)

        screen.blit(image, self.rect)


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

        # spawn rechts buiten scherm
        spawn_x = BREEDTE + 50
        self.rect = self.image.get_rect(topleft=(spawn_x, y))

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

        self.boss_mode = False

        self.entering = False   # ✅ nog niet in beeld

        self.mode = "normal"

        # FINAL MODE
        self.attack_done = False
        self.wait_timer = 0


    def update(self, enemy_bullets):

        # =========================
        # FINAL MODE BEHAVIOR
        # =========================
        if self.mode == "final":

            current_time = pygame.time.get_ticks()

            # ====================
            # FASE 1 → inkomen
            # ====================
            target_x = BREEDTE - 500

            if not self.attack_done:

                if self.rect.x > target_x:
                    self.rect.x -= 6
                    return None

                # eenmaal op positie → rocket
                self.attack_done = True
                self.wait_timer = current_time
                return "shoot_rocket"

            # ====================
            # FASE 2 → korte pause
            # ====================
            if current_time - self.wait_timer < 1200:
                return None

            # ====================
            # FASE 3 → weg dashen ✅
            # ====================
            self.rect.x += 12
            self.rect.y += math.sin(current_time * 0.01) * 3

            if self.rect.left > BREEDTE:
                self.alive = False

            return None


       

        current_time = pygame.time.get_ticks()

        # ✅ ENTRY MOVEMENT (alleen als geactiveerd)
        if self.entering:
            self.rect.x -= 6

            if self.rect.x <= BREEDTE - 250:
                self.moving = True
                self.entering = False

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
        if self.moving and current_time - self.last_shot > self.shot_cooldown:

            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery

            dist = math.hypot(dx, dy)

            if dist != 0:
                speed = 6
                speed_x = (dx / dist) * speed
                speed_y = (dy / dist) * speed
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
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > HOOGTE:
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
                    self.image_phase2.get_width() // 5,
                    self.image_phase2.get_height() // 5
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
            self.hp = 100

            self.transition = False
            self.transition_timer = 0

            self.attack_timer = 0
            self.attack_cooldown = 1200

            self.direction = 1

            self.phase2_stage = 0
            self.big_mode = False

            self.laser_timer = 0
            self.laser_cooldown = 1500  # 3000 ms = 3 seconden

            self.rocket_timer = 0
            self.rocket_cooldown = 2500

            self.final_form = False
            self.game = None
            
            # ✅ TRANSFORM VARS (hier toevoegen!)
            self.transforming = False
            self.transform_phase = 0
            self.transform_y_target = HOOGTE + 20


    def update(self):

        # =========================
        # 🛑 TRANSFORM OVERRIDE (SUPER BELANGRIJK)
        # =========================
        if self.transforming:

            # ⬇️ FASE 1 → naar beneden
            if self.transform_phase == 1:

                self.rect.y += 8

                if self.rect.top > HOOGTE:
                    self.transform_phase = 2

                    # ✅ image veranderen HIER
                    self.image = pygame.image.load(
                        r"TESTPYGAM_1._\boss skin\patrick boos.png"
                    ).convert_alpha()

                    scale = 0.6
                    self.image = pygame.transform.scale(
                        self.image,
                        (
                            int(self.image.get_width() * scale),
                            int(self.image.get_height() * scale)
                        )
                    )

                    self.rect = self.image.get_rect(
                        center=(BREEDTE - 200, HOOGTE + 200)
                    )

            # ⬆️ FASE 2 → omhoog
            elif self.transform_phase == 2:

                target_y = HOOGTE // 2

                self.rect.y -= 6

                if self.rect.centery <= target_y:

                    self.transforming = False
                    self.final_form = True

                    # kleine pause voor attacks
                    self.attack_timer = pygame.time.get_ticks() + 700

                    print("FINAL FORM READY")

            return  # ⛔ STOP ALLES ANDERS

        # =====================================
        # PHASE 1
        # =====================================
        if self.phase == 1:
            self.rect.x = BREEDTE - self.rect.width - 50
            self.rect.y = HOOGTE - self.rect.height - 120

        # =====================================
        # PHASE 2
        # =====================================
        elif self.phase == 2:

            if self.big_mode:
                self.rect.x = BREEDTE - self.rect.width - 50
                self.rect.y = HOOGTE // 2 - self.rect.height // 2

            else:
                self.rect.y += self.direction * 5

                if self.rect.top <= 0:
                    self.direction = 1

                if self.rect.bottom >= HOOGTE:
                    self.direction = -1

                self.rect.x = BREEDTE - self.rect.width - 50

        # =========================
        # START TRANSFORM (ONDERAAN!)
        # =========================
        if self.phase == 2 and self.hp <= 40 and not self.final_form:

            print("START TRANSFORM")

            self.game.minis.clear()

            self.transforming = True
            self.transform_phase = 1




    def attack(self, enemy_bullets, minis, player, rockets):

        # ❌ GEEN ATTACKS tijdens transform
        if self.transforming:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.attack_timer <= self.attack_cooldown:
            return

        self.attack_timer = current_time

        # =====================================
        # ✅ PHASE 1
        # =====================================
        if self.phase == 1:

            attack_type = random.choice(["seed", "spike", "burst"])

            if attack_type == "seed":

                bullet = EnemyBullet(
                    self.rect.left,
                    self.rect.centery,
                    -8,
                    random.randint(-2, 2)
                )
                enemy_bullets.append(bullet)

            elif attack_type == "spike":

                x_pos = random.randint(100, BREEDTE - 200)
                spike = Spike(x_pos, HOOGTE - 120)
                enemy_bullets.append(spike)

            elif attack_type == "burst":

                for angle in range(-3, 4):
                    bullet = EnemyBullet(
                        self.rect.left,
                        self.rect.centery,
                        -6,
                        angle * 2
                    )
                    enemy_bullets.append(bullet)

        # =====================================
        # ✅ PHASE 2
        # =====================================
        else:

            # =============================
            # 🟡 HP > 80 → spread
            # =============================
            if self.hp > 80:

                for angle in range(-3, 4):
                    bullet = EnemyBullet(
                        self.rect.centerx,
                        self.rect.centery,
                        -6,
                        angle * 2
                    )
                    enemy_bullets.append(bullet)

            # =============================
            # 🟠 80 → 60 → laser + single
            # =============================
            elif self.hp > 60:

                # single shot
                bullet = EnemyBullet(
                    self.rect.centerx,
                    self.rect.centery,
                    -10,
                    0
                )
                enemy_bullets.append(bullet)

                # lasers
                if current_time - self.laser_timer > self.laser_cooldown:

                    self.laser_timer = current_time

                    lanes = 4
                    lane_height = HOOGTE // lanes
                    weak_index = random.randint(0, lanes - 1)

                    for i in range(lanes):

                        y_pos = i * lane_height

                        if i == weak_index:
                            laser = WeakLaser(self.rect.left, y_pos)
                        else:
                            laser = LaserWall(self.rect.left, y_pos)

                        laser.rect.height = lane_height
                        enemy_bullets.append(laser)

            # =============================
            # 🔴 60 → 40 → (OPTIONEEL leeg of lichte attack)
            # =============================
            elif self.hp > 40:

                # lichte pattern (rust moment)
                if current_time % 2 == 0:
                    return

                for angle in [-10, 0, 10]:

                    bullet = EnemyBullet(
                        self.rect.centerx,
                        self.rect.centery,
                        -5,
                        angle * 2
                    )

                    enemy_bullets.append(bullet)


            # =============================
            # 🟠 40 → 20 → LASER + DOUBLE SPREAD ✅
            # =============================
            elif self.hp > 20:

                # ✅ laser walls elke 4 sec
                if current_time - self.laser_timer > 4000:

                    self.laser_timer = current_time

                    lanes = 4
                    lane_height = HOOGTE // lanes
                    weak_index = random.randint(0, lanes - 1)

                    for i in range(lanes):

                        y_pos = i * lane_height

                        if i == weak_index:
                            laser = WeakLaser(self.rect.left, y_pos)
                        else:
                            laser = LaserWall(self.rect.left, y_pos)

                        laser.rect.height = lane_height
                        enemy_bullets.append(laser)

                # ✅ dubbel spread
                for angle in [-15, -8, 8, 15]:

                    speed_x = -7
                    speed_y = math.sin(math.radians(angle)) * 6

                    bullet = EnemyBullet(
                        self.rect.centerx,
                        self.rect.centery,
                        speed_x,
                        speed_y
                    )

                    enemy_bullets.append(bullet)

            # =============================
            # 🟣 ≤ 20 → GEEN ATTACKS ✅
            # =============================
            else:
                return
    
    def take_damage(self):

        # ❗ GEEN DAMAGE TIJDENS TRANSFORM
        if self.transforming:
            return

        HitSound.play()

        self.hp -= 1

        # ✅ trigger exact op 40 (extra zekerheid)
        if self.phase == 2 and self.hp == 40 and not self.final_form:
            print("TRANSFORM TRIGGER EXACT")

        # ✅ PHASE 1 → DIRECT VERDWIJNEN
        if self.phase == 1 and self.hp <= 0:

            self.rect.x = -1000
            self.rect.y = -1000

            self.transition = True
            self.transition_timer = pygame.time.get_ticks()

            return

        # ✅ PHASE 2 EVENTS
        if self.phase == 2:

            new_stage = (100 - self.hp) // 20

            if new_stage > self.phase2_stage:
                self.phase2_stage = new_stage
                self.phase2_event()

        print("Boss HP:", self.hp)

        # ✅ WIN
        if self.phase == 2 and self.hp <= 0:
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

            self.attack_cooldown = 1100
            self.big_mode = True


        elif self.phase2_stage == 3:
            print("Chaos mode!")
            self.attack_cooldown = 500

        elif self.phase2_stage == 4:
            print("Rage mode!")
            self.attack_cooldown = 300

        elif self.phase2_stage == 5:
            print("FINAL MODE!!!")
            self.attack_cooldown = 500

# =====================================
# END SCREEN
# =====================================

def end_screen(text):

    waiting = True

    big_font = pygame.font.SysFont(None, 100)

    small_font = pygame.font.SysFont(None, 50)

    while waiting:

        frame.blit(achtergrond_fase1, (0, 0))

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
        self.boss.game = self  # ✅ KOPPELING VOOR DAMAGE LOCK

        self.bullets = []
        self.enemy_bullets = []

        self.font = pygame.font.SysFont(None, 80)

        self.bg_x = 0
        self.scroll_speed = 2

        self.lasers = []
        self.rockets = []

        self.god_mode = False
        self.debug_damage = False

        # ✅ OUDE ROCKET FLAGS (mag blijven)
        self.spawned_75 = False
        self.spawned_70 = False
        self.spawned_65 = False

        # ✅ DOODLEBOBS
        self.minis = []
        self.spawned_doodles = False
        self.last_doodle_spawn = 0
        self.doodle_delay = 4000

        # ✅ NIEUW → TWEEDE BOSS
        self.second_boss = None

        # ✅ NIEUW → LOCK SYSTEM (optioneel voor debug)
        self.doodlebob_alive = False

        self.second_rocket_timer = 0


    def update(self):

        # ⏱️ tijd
        self.current_time = pygame.time.get_ticks()
        current_time = self.current_time

        self.doodlebob_alive = len(self.minis) > 0

        # ================================
        # PLAYER + BOSS
        # ================================
        self.player.movement(self.boss.phase)
        self.player.shoot(self.bullets)
        self.player.super_attack(self.bullets)

        self.boss.update()
        self.boss.attack(self.enemy_bullets, self.minis, self.player, self.rockets)

        # ================================
        # PLAYER BULLETS
        # ================================
        for bullet in self.bullets[:]:

            bullet.update()

            # HIT BOSS
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

            # HIT MINIS
            for mini in self.minis[:]:
                if bullet.rect.colliderect(mini.rect):

                    mini.hp -= 1
                    if mini.hp <= 0:
                        self.minis.remove(mini)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    break

            # HIT WEAK LASER
            for enemy in self.enemy_bullets[:]:
                if isinstance(enemy, WeakLaser) and bullet.rect.colliderect(enemy.rect):

                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        self.enemy_bullets.remove(enemy)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    break

            if bullet.rect.left > BREEDTE:
                self.bullets.remove(bullet)

        
        if self.boss.phase == 2 and 60 >= self.boss.hp > 40 and not self.spawned_doodles:

            print("DoodleBobs spawned 😈")

            top_rect_y = self.boss.rect.top - 60
            bottom_rect_y = self.boss.rect.bottom + 60

            top = MiniDoodle(
                self.boss.rect.left,
                top_rect_y,
                self.player
            )

            bottom = MiniDoodle(
                self.boss.rect.left,
                bottom_rect_y,
                self.player
            )

            top.entering = True
            bottom.entering = True

            self.minis.append(top)
            self.minis.append(bottom)


            self.spawned_doodles = True

        # ================================
        # ✅ DOODLEBOB RESPAWN (FIX)
        # ================================
        alive_minis = [m for m in self.minis if m.alive]

        if self.boss.phase == 2 and 60 >= self.boss.hp > 40:

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
        
        # ================================
        # FINAL DOODLEBOS (HP ≤ 10)
        # ================================
        if self.boss.phase == 2 and self.boss.hp <= 20:

            if len(self.minis) == 0:

                top = MiniDoodle(
                    BREEDTE + 50,
                    HOOGTE // 4,
                    self.player
                )

                bottom = MiniDoodle(
                    BREEDTE + 50,
                    HOOGTE * 3 // 4,
                    self.player
                )

                top.mode = "final"
                bottom.mode = "final"

                self.minis.append(top)
                self.minis.append(bottom)


        # ================================
        # ROCKETS
        # ================================
        for rocket in self.rockets[:]:

            rocket.update()

            if rocket.rect.colliderect(self.player.hitbox):

                if current_time - self.player.last_hit > self.player.hit_cooldown:
                    if not self.god_mode:
                        self.player.lives -= 1

                    self.player.last_hit = current_time
                    CrashSound.play()

                self.rockets.remove(rocket)

            elif rocket.should_destroy():
                self.rockets.remove(rocket)

            elif (
                rocket.rect.right < 0
                or rocket.rect.left > BREEDTE
                or rocket.rect.top < 0
                or rocket.rect.bottom > HOOGTE
            ):
                self.rockets.remove(rocket)

        # ================================
        # DOODLEBOS UPDATE
        # ================================
        for mini in self.minis[:]:

            result = mini.update(self.enemy_bullets)

            if result == "shoot_rocket":
                rocket = LockRocket(
                    mini.rect.centerx,
                    mini.rect.centery,
                    self.player
                )
                self.rockets.append(rocket)


            if mini.rect.colliderect(self.player.hitbox):

                if current_time - self.player.last_hit > self.player.hit_cooldown:
                    if not self.god_mode:
                        self.player.lives -= 1

                    self.player.last_hit = current_time
                    CrashSound.play()

            if not mini.alive:
                self.minis.remove(mini)

        # ================================
        # ENEMY BULLETS
        # ================================
        for bullet in self.enemy_bullets[:]:

            bullet.update()

            if isinstance(bullet, Spike):
                if not bullet.active:
                    self.enemy_bullets.remove(bullet)
                    continue

            if bullet.rect.colliderect(self.player.hitbox):

                if current_time - self.player.last_hit > self.player.hit_cooldown:
                    if not self.god_mode:
                        self.player.lives -= 1

                    self.player.last_hit = current_time
                    CrashSound.play()

                self.enemy_bullets.remove(bullet)

        # ================================
        # PLAYER vs BOSS
        # ================================
        if self.player.hitbox.colliderect(self.boss.rect):

            if current_time - self.player.last_hit > self.player.hit_cooldown:
                if not self.god_mode:
                    self.player.lives -= 1

                self.player.last_hit = current_time
                CrashSound.play()

        # ================================
        # GAME OVER
        # ================================
        if self.player.lives <= 0:
            self.running = False
            end_screen("GAME OVER")

        # ================================
        # BACKGROUND SCROLL
        # ================================
        self.bg_x -= self.scroll_speed

        if self.bg_x <= -BREEDTE:
            self.bg_x = 0

        if self.boss.phase == 1:
            self.scroll_speed = 2
        else:
            self.scroll_speed = 5





    

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

            frame.blit(achtergrond_fase1, (self.bg_x, 0))
            frame.blit(achtergrond_fase1, (self.bg_x + BREEDTE, 0))

        else:

            frame.blit(achtergrond_fase2, (self.bg_x, 0))
            frame.blit(achtergrond_fase2, (self.bg_x + BREEDTE, 0))

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
        
        if self.second_boss:
            self.second_boss.draw(frame)


        
        
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


def fade(screen, width, height, speed=5):

    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))

    for alpha in range(0, 255, speed):

        fade_surface.set_alpha(alpha)

        screen.blit(fade_surface, (0, 0))
        pygame.display.update()

        pygame.time.delay(10)

# =====================================
# START GAME
# =====================================

def start_game():

    menusound.stop()

    game = Game()

    game.run()


def start_with_fade():

    fade(frame, BREEDTE, HOOGTE)  # 🎬 fade eerst

    start_game()  # start daarna game

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

        self.menu.add.button('START', start_with_fade)
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