import pygame
import pygame_menu

# Start pygame
pygame.init()

# Schaal en instellingen
schaal1 = 3
achter2 = pygame.image.load(r"achtergrond\Man_Ray_Returns_001.webp")
achter1 = pygame.image.load(r"achtergrond\achtergrond.jpg")
achter1 = pygame.transform.scale(achter1, (achter1.get_width() * schaal1, achter1.get_height() * schaal1))

BREEDTE, HOOGHTE = achter1.get_width(), achter1.get_height()
frame = pygame.display.set_mode((BREEDTE, HOOGHTE))

# Zelda achtergrond voor het menu
zelda_background = pygame.image.load('achtergrond\download (1).jpeg')  # Vervang dit met je daadwerkelijke Zelda-afbeelding
zelda_background = pygame.transform.scale(zelda_background, (BREEDTE, HOOGHTE))  # Schaal de afbeelding naar het scherm

# SFX laden
menusound = pygame.mixer.Sound('sfx\Sarias Song - Zelda Ocarina of Time - Lost Woods - Part 42.mp3')

# Functie om het spel te starten
def start_game(): 
    menusound.stop()

    # Start game code (je bestaande logica volgt hier)
    # ...

# Menu aanmaken
menu = pygame_menu.Menu('Eenvoudig Menu', BREEDTE, HOOGHTE, theme=pygame_menu.themes.THEME_SOLARIZED)

# Pas achtergrond toe in menu
menu.get_widget('background_color').set_background(zelda_background)

menusound.play()

menu.add_button('Start', start_game)  # Voeg een knop toe die het spel start
menu.add_button('Quit', pygame.quit)  # Voeg een knop toe om het programma af te sluiten

# Start de menu-lus en toon het menu
menu.mainloop(frame)
import pygame
import pygame_menu
import pygame_menu.events
import random

# Init pygame
pygame.init()

# Maak frame aan met bepaalde grootte.

schaal = 3

doodlebot_foto = pygame.image.load(r"DoodleBob_Stock_Art.webp")
doodlebot_foto = pygame.transform.scale(doodlebot_foto,(doodlebot_foto.get_width()*schaal, doodlebot_foto.get_height()*schaal))

# SFX laden
HitSound = pygame.mixer.Sound(r'sfx/soundscrate-slaphit.mp3')
GunSound = pygame.mixer.Sound(r'sfx/soundscrate-classic-gun-shot-6.mp3')
JetcrashSFX = pygame.mixer.Sound(r'sfx\soundscrate-Rattling_Metal_Impact_3.mp3')

menusound = pygame.mixer.Sound(r'sfx\Sarias Song - Zelda Ocarina of Time - Lost Woods - Part 42.mp3')

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zelda Menu")

# Laad de Zelda achtergrondafbeelding
background_image = pygame.image.load("achtergrond\download (1).jpeg")  # Vervang met je Zelda afbeelding
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def draw_background(surface):
    """Tekent de Zelda achtergrondafbeelding."""
    surface.blit(background_image, (0, 0))
    menusound.play()

# Maak een Zelda-stijl menu
zelda_theme = pygame_menu.themes.THEME_DARK.copy()
zelda_theme.title_font = pygame_menu.font.FONT_FRANCHISE  # Zelda-achtige stijl
zelda_theme.widget_font = pygame_menu.font.FONT_NEVIS
zelda_theme.background_color = (0, 0, 0, 0)  # Transparant zodat we de achtergrond zien

menu = pygame_menu.Menu('Zelda Adventure', WIDTH, HEIGHT, theme=zelda_theme)

# Voeg opties toe
menu.add.label("Welkom, avonturier!", font_size=30)
startknop = menu.add.button("Start Quest", lambda: print("Start Zelda Quest"), font_color=(0, 255, 0))  # Groene tekst
if startknop == True:
    surface = doodlebot_foto

menu.add.button("Instellingen", lambda: print("instellingen "), font_color=(0, 255, 0))  # Groene tekst
menu.add.button("Afsluiten", pygame_menu.events.EXIT)



# Game loop
while True:
    screen.fill((0, 0, 0))  # Zwart scherm
    draw_background(screen)  # Zelda achtergrond tekenen
    events = pygame.event.get()
    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)
    pygame.display.update()
