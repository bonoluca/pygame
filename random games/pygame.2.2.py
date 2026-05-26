import pygame  # Importeer de pygame bibliotheek
import pygame_menu  # Importeer pygame-menu voor het maken van het menu

# Pygame initialiseren
pygame.init()

# Scherminstellingen
WIDTH, HEIGHT = 800, 600  # Breedte en hoogte van het scherm instellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Maak een venster met de opgegeven afmetingen
pygame.display.set_caption("Eenvoudig Menu")  # Stel de titel van het venster in

# Kleuren\WHITE = (255, 255, 255)  # Witte kleur gedefinieerd in RGB
BLACK = (0, 0, 0)  # Zwarte kleur gedefinieerd in RGB

# Functie die het spel start
def start_game():
    while True:
        
        
        print("Spel start...")  # Print bericht dat het spel start

# Menu aanmaken
menu = pygame_menu.Menu('Eenvoudig Menu', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)
menu.add.button('Start', start_game)  # Voeg een knop toe die het spel start
menu.add.button('Quit', pygame.quit)  # Voeg een knop toe om het programma af te sluiten
menu.mainloop(screen)  # Start de menu-lus en toon het menu
