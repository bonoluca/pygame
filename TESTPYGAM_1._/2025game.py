import pygame
import time
import random
import pygame_menu

# Start pygame.
pygame.init()

# zelda = pygame.image.load(r'achtergrond\download (1).jpeg')

# Maak frame aan met bepaalde grootte.
schaal1= 3
achter2 = pygame.image.load(r"TESTPYGAM_1._\achtergrond\Man_Ray_Returns_001.webp")

achter1 = pygame.image.load(r"TESTPYGAM_1._\achtergrond\achtergrond.jpg")
achter1= pygame.transform.scale(achter1,(achter1.get_width()*schaal1, achter1.get_height()*schaal1))
BREEDTE,HOOGHTE = achter1.get_width() , achter1.get_height()
schaal = 0.15



achtergrond = random.choice( (achter1,achter2) )
BREEDTE, HOOGHTE = achtergrond.get_width(), achtergrond.get_height()
frame = pygame.display.set_mode((BREEDTE, HOOGHTE))

# SFX laden
HitSound = pygame.mixer.Sound('TESTPYGAM_1._\sfx\soundscrate-slaphit.mp3')
GunSound = pygame.mixer.Sound('TESTPYGAM_1._\sfx\soundscrate-classic-gun-shot-6.mp3')
JetcrashSFX = pygame.mixer.Sound('TESTPYGAM_1._\sfx\soundscrate-Rattling_Metal_Impact_3.mp3')

menusound = pygame.mixer.Sound('TESTPYGAM_1._\sfx\Sarias Song - Zelda Ocarina of Time - Lost Woods - Part 42.mp3')

# bossound =  pygame.mixer.Sound('')

# Maak een pygame klok om de FPS van het spel te bepalen.
  

def start_game(): 

   menusound.stop()
   


   lastGunShotTime = 0  # Tijdstip van het laatste schot
   lastHitTime = 0 # tijdstip van de laatste keer gebotst
   cooldownGunShotTime = 500 # cooldown voor 500ms
   cooldownHitTime = 1000 # cooldown voor 1sec

   # Zet alle benodigde afbeeldingen & hun startposities klaar.
   doodlebot_foto = pygame.image.load(r"TESTPYGAM_1._\DoodleBob_Stock_Art.webp")
   doodlebot_foto = pygame.transform.scale(doodlebot_foto,(doodlebot_foto.get_width()*schaal, doodlebot_foto.get_height()*schaal))
   
   vijand_foto = doodlebot_foto 
   vijand = pygame.Rect(30,20, vijand_foto.get_width() - 5,vijand_foto.get_height()- 1)
   vijand_type = "Doodlebob"
   
   patrick_foto = pygame.image.load(r'TESTPYGAM_1._\Bikini-Patrick.png')
   patrick_foto = pygame.transform.scale(patrick_foto,(patrick_foto.get_width()//4, patrick_foto.get_height()//4))

   monaca = pygame.image.load(r"TESTPYGAM_1._\Monaca-DBZ.png")
   monaca =  pygame.transform.scale(monaca,(monaca.get_width()*schaal, monaca.get_height()*schaal))

   #---------------------------------------------------------------------------------------------------------------------------

   schaal3 = 1.20
   VLIEGTUIGfoto = pygame.image.load(r"TESTPYGAM_1._\skins jet\pixilart-drawing.png")
   VLIEGTUIGfoto = pygame.transform.scale(VLIEGTUIGfoto,(VLIEGTUIGfoto.get_width()*schaal3,VLIEGTUIGfoto.get_height()*schaal3))
   jet  = pygame.Rect(380,400, VLIEGTUIGfoto.get_width(),VLIEGTUIGfoto.get_height())
   jet_foto = VLIEGTUIGfoto

   #---------------------------------------------------------------------------------------------------------------------------

   schaal4 = 0.5
   explosie = pygame.image.load(r'TESTPYGAM_1._\explosie3.webp')
   explosie = pygame.transform.scale(explosie,(explosie.get_width()*schaal4,explosie.get_height()*schaal4))

   #---------------------------------------------------------------------------------------------------------------------------

   bullet_foto = pygame.image.load(r'TESTPYGAM_1._\kogel.png')
   bullet_foto = pygame.transform.rotate(bullet_foto,90 )
   bullets = []

   #---------------------------------------------------------------------------------------------------------------------------
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

   #-----------------------------------------------------------------------------------------------------------------------------
   hp = 5
   cooldown = 0  # Cooldown period in milliseconds
   cooldown2 = 1000
   last_hit_time = 0 
   LAST_shoot_time = 2000
   running =  True
   geraakt = False
   snelheid_vijand = 5
   snelheid_jet = 3
   klok = pygame.time.Clock()
   FPS = 60


   while running:

      # print("Spel start...")  # Print bericht dat het spel start
           # Get the current time
      current_time = pygame.time.get_ticks() 
      
      # Collision detection and health update
      if jet.colliderect(vijand) and (pygame.time.get_ticks() - lastHitTime > cooldownHitTime):
         JetcrashSFX.play()
         lastHitTime = pygame.time.get_ticks()  # Update de laatst geregistreerde hit-tijd
         hp -= 1
         # print(f"Hit! Remaining HP: {hp}")
      
      bullet_geraakt = vijand.collidelist(bullets)
      if bullet_geraakt != -1 and current_time - last_hit_time > cooldown:
         HitSound.play()
         bullets.pop(bullet_geraakt)
         last_hit_time = current_time
         hp -= 1
         # print(f"Hit! Remaining HP: {hp}")
      if hp == 5:
         HPbar_FULL = HPbar_FULL
         # print('geen hit ')
      elif hp ==4:
         HPbar_FULL = HPbar_1e_hit
         # print('eerste hit ')
      elif hp == 3:
         HPbar_FULL = HPbar_2e_hit
         # print('tweede hit ')
      elif hp == 2:
         HPbar_FULL = HPbar_3e_hit
         # print('derde hit ')
      elif hp == 1:
         HPbar_FULL = HPbar_4e_hit
         # print('vierde hit ')
      elif hp == 0:
         HPbar_FULL = HPbar_empty
         vijand_foto = patrick_foto
         vijand = pygame.Rect(30,20, vijand_foto.get_width() - 5,vijand_foto.get_height()- 1)
         
         vijand_type = "Patrick"
         hp = 5

                 

   
      " Actie 2: spel-staat wijzigen. "  
      klok.tick(FPS) # Laat while-loop niet sneller gaan dan FPS.
      if vijand_type == "Doodlebob":

         vijand.x = vijand.x + snelheid_vijand # Verhoog x-positie van vijand.
         if vijand.x + vijand_foto.get_width()>= BREEDTE: # Is vliegtuig volledig van rechterrand frame?
            snelheid_vijand = -snelheid_vijand # Verplaats het links.
         elif vijand.x <= 0:
            snelheid_vijand= -snelheid_vijand
     
      # elif vijand_type == "Patrick":
      #    vijand.x = vijand.x + snelheid_vijand
      #    vijand.y = vijand.y - snelheid_vijand
      #    if vijand.x + patrick_foto.get_width()>= BREEDTE:
      #       snelheid_vijand = -snelheid_vijand # Verplaats het links.
      #    # if vijand.colliderect(achtergrond): print("Raak!")      
      elif vijand_type == "Patrick":
        vijand.x += snelheid_vijand_x
        vijand.y += snelheid_vijand_y

    # Controleer of hij de rechter- of linkerkant van het scherm raakt
      if vijand.x + patrick_foto.get_width() >= BREEDTE or vijand.x <= 0:
        snelheid_vijand_x = random.choice([-3, -2, -1, 1, 2, 3])  # Nieuwe willekeurige X-snelheid

    # Controleer of hij de boven- of onderkant van het scherm raakt
      if vijand.y + patrick_foto.get_height() >= 800 or vijand.y <= 0:
        snelheid_vijand_y = random.choice([-3, -2, -1, 1, 2, 3])  # Nieuwe willekeurige Y-snelheid

         
      # Verplaats ELKE kogel naar rechts met 1.     
      for index, bullet in enumerate(bullets): 
        bullets[index].y = bullets[index].y - 5
                                                  
   
      pygame.event.pump()                # Verwerk events.

   
      toetsen = pygame.key.get_pressed() # Haal staat toetsen op.
      if toetsen[pygame.K_LEFT]:         # Als linkerpijl is ingedrukt...
         # print("Linkerpijl ingedrukt")  # Dan print boodschap.
         jet.x = jet.x - snelheid_jet
   
      if toetsen[pygame.K_RIGHT]:         # Als linkerpijl is ingedrukt...
         # print("rechterpijl ingedrukt")  # Dan print boodschap.
         jet.x = jet.x + snelheid_jet
      
      if toetsen[pygame.K_UP]:         # Als linkerpijl is ingedrukt...
         # print("up_pijl ingedrukt")  # Dan print boodschap.
         jet.y = jet.y - snelheid_jet
         
      if toetsen[pygame.K_DOWN]:         # Als linkerpijl is ingedrukt...
         # print("up_pijl ingedrukt")  # Dan print boodschap.
         jet.y = jet.y + snelheid_jet

      if toetsen[pygame.K_SPACE] and (pygame.time.get_ticks() - lastGunShotTime > cooldownGunShotTime):
      # Spatie is ingedrukt en cooldown is voorbij
         GunSound.play()
         y_kogel_temp = jet.y - bullet_foto.get_height()
         x_kogel_temp = jet.x + VLIEGTUIGfoto.get_width() // 2 - bullet_foto.get_width() // 2
         bullets.append(pygame.Rect(x_kogel_temp, y_kogel_temp, bullet_foto.get_width(), bullet_foto.get_height()))

         #  Update lastGunShotTime alleen als er een schot is afgevuurd
         lastGunShotTime = pygame.time.get_ticks()


      if jet.x > BREEDTE:
         jet.x = -100
      elif jet.x < -100:
         jet.x = BREEDTE
         

      "Actie 3: teken & toon frame. "
      print(vijand.x, vijand.y)

      frame.blit(achtergrond, (0,0))
      frame.blit(vijand_foto, (vijand.x,vijand.y)) # Teken vliegtuig.
      frame.blit(HPbar_FULL,(0,350))
      frame.blit(jet_foto,(jet.x, jet.y))
      for bullet in bullets: # Teken ELKE kogel in de lijst kogels.
        frame.blit(bullet_foto,bullet)

   
      pygame.display.flip()     # Toon frame aan gebruiker.


# Menu aanmaken
menu = pygame_menu.Menu('Eenvoudig Menu', BREEDTE, HOOGHTE, theme=pygame_menu.themes.THEME_SOLARIZED)
menusound.play()
menu.add.button('Start', start_game)  # Voeg een knop toe die het spel start
menu.add.button('Quit', pygame.quit)  # Voeg een knop toe om het programma af te sluiten
menu.mainloop(frame)  # Start de menu-lus en toon het menu