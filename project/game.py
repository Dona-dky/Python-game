import pygame
import pytmx
import pyscroll

from player import Player

class Game:

    def __init__(self):

        #self.screen = pygame.display.set_mode((500,300))
        self.screen = pygame.display.set_mode((1000,800))

        pygame.display.set_caption("Pygamon - WOW")

        # Son du jeu
        song = pygame.mixer.Sound("./sound/SNK.mp3")
        song.play()

        # Charger la carte du jeu
        tmx_data = pytmx.util_pygame.load_pygame('./textures/background/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            # Afficher la touche dans la console  
            # print("up")
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def run(self):

        #Boucle du jeu
        launched = True

        while launched:
            # Afficher la touche dans la console si print("x") 
            self.handle_input()

            # Mettre à jour le déplacement du joueur
            self.group.update()

            # Centrer la caméra sur le joueur
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)

            # Chargement et collage du fond
            #background = pygame.image.load("./textures/background/foot.jpg").convert()
            #self.screen.blit(background, (0,0))

            # Rafraîchissement de l'écran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = False

        pygame.quit()