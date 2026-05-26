import pygame
import time
 
# Start pygame.
pygame.init()
# Maak frame aan met bepaalde grootte.
# breed, hoog = 1000, 1000
schaal1= 3
achter = pygame.image.load(r"TESTPYGAM_1._\achtergrond.jpg")
achter= pygame.transform.scale(achter,(achter.get_width()*schaal1, achter.get_height()*schaal1))
BREEDTE,HOOGHTE = achter.get_width() , achter.get_height()
schaal = 0.15
frame = pygame.display.set_mode((BREEDTE, HOOGHTE))
 
 
# Zet alle benodigde afbeeldingen & hun startposities klaar.
doodlebobfoto= pygame.image.load(r"TESTPYGAM_1._\DoodleBob_Stock_Art.webp")
doodlebobfoto = pygame.transform.scale(doodlebobfoto,(doodlebobfoto.get_width()*schaal, doodlebobfoto.get_height()*schaal))
doodlebob = pygame.Rect(30,20, doodlebobfoto.get_width() - 5,doodlebobfoto.get_height()- 1)
 
schaal3 = 1.20
VLIEGTUIGfoto = pygame.image.load(r"TESTPYGAM_1._\skins jet\pixil-layer-Background.png")
VLIEGTUIGfoto = pygame.transform.scale(VLIEGTUIGfoto,(VLIEGTUIGfoto.get_width()*schaal3,VLIEGTUIGfoto.get_height()*schaal3))
jet  = pygame.Rect(380,400, VLIEGTUIGfoto.get_width(),VLIEGTUIGfoto.get_height())
jet_foto = VLIEGTUIGfoto
 
schaal4 = 0.5
explosie = pygame.image.load(r'TESTPYGAM_1._\explosie3.webp')
explosie = pygame.transform.scale(explosie,(explosie.get_width()*schaal4,explosie.get_height()*schaal4))

kogelfoto = pygame.image.load(r'TESTPYGAM_1._\kogel.png')
kogel =  pygame.Rect(400,420, kogelfoto.get_width(),kogelfoto.get_height())
 
schaal5 = 3
HPbar_FULL= pygame.image.load(r'TESTPYGAM_1._\HP bar\fullHP_bar.png')
HPbar_FULL = pygame.transform.scale(HPbar_FULL,(HPbar_FULL.get_width()*schaal5,HPbar_FULL.get_height()*schaal5))
 
HPbar_empty = pygame.image.load(r'TESTPYGAM_1._\HP bar\DoodleBobHealthBar.png')
HPbar_empty = pygame.transform.scale(HPbar_empty,(HPbar_empty.get_width()*schaal5,HPbar_empty.get_height()*schaal5))
 
HPbar_1e_hit = pygame.image.load(r'TESTPYGAM_1._\HP bar\HP_barr_1e_hit.png')
HPbar_1e_hit = pygame.transform.scale(HPbar_1e_hit,(HPbar_1e_hit.get_width()*schaal5,HPbar_1e_hit.get_height()*schaal5))
 
 
HPbar_2e_hit = pygame.image.load(r'TESTPYGAM_1._\HP bar\HP_bar_2e_hit.png')
HPbar_2e_hit = pygame.transform.scale(HPbar_2e_hit,(HPbar_2e_hit.get_width()*schaal5,HPbar_2e_hit.get_height()*schaal5))
 
HPbar_3e_hit = pygame.image.load(r'TESTPYGAM_1._\HP bar\HP_bar_3e_hit.png')
HPbar_3e_hit = pygame.transform.scale(HPbar_3e_hit,(HPbar_3e_hit.get_width()*schaal5,HPbar_3e_hit.get_height()*schaal5))
 
HPbar_4e_hit = pygame.image.load(r'TESTPYGAM_1._\HP bar\HP_bar_4e_hit.png')
HPbar_4e_hit = pygame.transform.scale(HPbar_4e_hit,(HPbar_4e_hit.get_width()*schaal5,HPbar_4e_hit.get_height()*schaal5))
 
wasted = pygame.image.load(r'TESTPYGAM_1._\achtergrond\GTA-Wasted-PNG-Image.png')
 
snelheid_doodlebob = 10
snelheid_jet = 6
# Maak een pygame klok om de FPS van het spel te bepalen.
klok = pygame.time.Clock()
FPS = 60
 
running =  True
geraakt = False
 
hp = 5
cooldown = 2000  # Cooldown period in milliseconds
last_hit_time = 0


while running:
   # Get the current time
   current_time = pygame.time.get_ticks()
   
   # Collision detection and health update
   if jet.colliderect(doodlebob) and current_time - last_hit_time > cooldown:
      last_hit_time = current_time
      hp -= 1
      print(f"Hit! Remaining HP: {hp}")
     
 
   if hp == 4:
      HPbar_FULL = HPbar_1e_hit
      print('eerste hit ')
   elif hp == 3:
      HPbar_FULL = HPbar_2e_hit
      print('tweede hit ')
   elif hp == 2:
      HPbar_FULL = HPbar_3e_hit
      print('derde hit ')
   elif hp == 1:
      HPbar_FULL = HPbar_4e_hit
      print('vierde hit ')
   elif hp == 0:
      jet_foto = explosie
      HPbar_FULL = HPbar_empty
      achter = wasted
      print("Spel afgelopen. Vliegtuig kapot.")
      geraakt = True 
 
  
 
   " Actie 2: spel-staat wijzigen. "  
   klok.tick(FPS) # Laat while-loop niet sneller gaan dan FPS.
 
   doodlebob.x = doodlebob.x + snelheid_doodlebob # Verhoog x-positie van vliegtuig.
   if doodlebob.x + doodlebobfoto.get_width()>= BREEDTE: # Is vliegtuig volledig van rechterrand frame?
      snelheid_doodlebob = -snelheid_doodlebob # Verplaats het links.
   elif doodlebob.x <= 0:
      snelheid_doodlebob= -snelheid_doodlebob
 
 
 
   pygame.event.pump()                # Verwerk events.
   
 
 
   toetsen = pygame.key.get_pressed() # Haal staat toetsen op.
   if toetsen[pygame.K_LEFT]:         # Als linkerpijl is ingedrukt...
      print("Linkerpijl ingedrukt")  # Dan print boodschap.
      jet.x = jet.x - snelheid_jet
 
   if toetsen[pygame.K_RIGHT]:         # Als linkerpijl is ingedrukt...
      print("rechterpijl ingedrukt")  # Dan print boodschap.
      jet.x = jet.x + snelheid_jet
   
   if toetsen[pygame.K_UP]:         # Als linkerpijl is ingedrukt...
      print("up_pijl ingedrukt")  # Dan print boodschap.
      jet.y = jet.y - snelheid_jet
     
   
   if toetsen[pygame.K_DOWN]:         # Als linkerpijl is ingedrukt...
      print("up_pijl ingedrukt")  # Dan print boodschap.
      jet.y = jet.y + snelheid_jet
   
 
 
 
 
 
 
   " Actie 3: teken & toon frame. "
   frame.blit(achter, (0,0))
   frame.blit(doodlebobfoto, (doodlebob.x,doodlebob.y)) # Teken vliegtuig.
   frame.blit(HPbar_FULL,(0,350))
   frame.blit(jet_foto,(jet.x, jet.y))
   pygame.display.flip()     # Toon frame aan gebruiker.

   if geraakt:
      time.sleep(2)
      running = False