import pygame
file = 'C:\Users\DIEL111008\MOSA-RT\Luca Bono - TESTPYGAM_1._\sfx\Sarias Song - Zelda Ocarina of Time - Lost Woods - Part 42.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()