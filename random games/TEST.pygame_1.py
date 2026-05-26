import pygame

pygame.init()
# BREEDTE,HOOGHTE = 500,500

achter = pygame.image.load(r"TESTPYGAM_1._\achtergrond.jpg") 
BREEDTE,HOOGHTE = achter.get_width() , achter.get_height()

frame = pygame.display.set_mode((BREEDTE,HOOGHTE))
# frame.fill((250, 0, 0))   # kies de achtergrond kleur 
"-------------------------------------------------------"
klok = pygame.time.Clock()

while True:
    klok.tick(FPS) # Laat while-loop niet sneller gaan dan FPS.
    y_vliegtuig = y_vliegtuig + snelheid_vliegtuig # Verhoog x-positie van vliegtuig.
    if y_vliegtuig + afb_vliegtuig.get_height()>= hoog: # Is vliegtuig volledig van rechterrand frame?
      snelheid_vliegtuig = -snelheid_vliegtuig # Verplaats het links.
    elif y_vliegtuig <= 0:
       snelheid_vliegtuig = -snelheid_vliegtuig


    VLIEGTUIGfoto = pygame.image.load(r"TESTPYGAM_1._\fotovliegtuig.png")
    
    schaal = 0.15

    x_doodlebob , y_doodlebob = 30, 20 
    doodlebobfoto= pygame.image.load(r"TESTPYGAM_1._\DoodleBob_Stock_Art.webp")
    doodlebobfoto = pygame.transform.scale(doodlebobfoto,(doodlebobfoto.get_width()*schaal, doodlebobfoto.get_height()*schaal))
    frame.blit(achter, (0,0))
    frame.blit(doodlebobfoto,(BREEDTE// 2 - doodlebobfoto.get_width()//2, HOOGHTE// 2 - doodlebobfoto.get_height()//2 ))
    frame.blit(VLIEGTUIGfoto, (50, 50))
    pygame.display.flip()



  
  

    
    
