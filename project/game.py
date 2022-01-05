import pygame
from pygame.constants import MOUSEBUTTONDOWN
import pytmx
import pyscroll

from player import Player

class Game:

    def __init__(self):

        #definir si le jeu a commencé ou pas
        self.is_playing = False

        #self.screen = pygame.display.set_mode((630,450))
        self.screen = pygame.display.set_mode((800,450))
        #self.screen = pygame.display.set_mode((1000,800))

        self.icone = pygame.image.load("./textures/btn/smile.png").convert()
        pygame.display.set_icon(self.icone)
        # Chargement et collage du fond
        self.background = pygame.image.load("./textures/background/background.jpg")

        self.banner = pygame.image.load("./textures/Logo_game.png")
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = self.screen.get_width() / 10.5

        self.play_button = pygame.image.load("./textures/btn/start.png")
        #self.play_button = pygame.transform.scale(self.play_button, (120, 50))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = self.screen.get_width() / 2.5
        self.play_button_rect.y = self.screen.get_height() / 1.8

        self.quit_button = pygame.image.load("./textures/btn/quit.png")


        pygame.display.set_caption("LABYRINTHE - SNK")

        # Son du jeu
        self.song = pygame.mixer.Sound("./sound/SNK.mp3")
        self.song.play()

        # Charger la carte du jeu
        self.tmx_data = pytmx.util_pygame.load_pygame('./textures/background/map.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Generer un joueur
        player_position = self.tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Définir une liste qui va stocker les rectangles de collision
        self.walls = []

        self.wayout = []

        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "out":
                self.wayout.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)

        self.timer_font = pygame.font.Font("FrescoStamp.ttf", 38)
        self.timer_sec = 60
        self.timer_text = self.timer_font.render("01:00", True, (240, 0, 32))

        self.timer = pygame.USEREVENT + 1                                                
        pygame.time.set_timer(self.timer, 1000)



    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            # Afficher la touche dans la console  
            # print("up")
            self.player.move_up()
            self.player.change_animation('up')

        if pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')

        if pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def update(self):
        self.group.update()

        #Vérification de collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def start(self):
        self.screen.blit(self.background, (0,0))

        self.screen.blit(self.banner, self.banner_rect)
                #self.screen.blit(self.banner, (0,0))
        self.screen.blit(self.play_button, self.play_button_rect)

        for event in pygame.event.get():         
                
            # verification pour savoir si la souris est en collision avec le bouton
            if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):                    
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.play_button = pygame.image.load("./textures/btn/start_select.png")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_playing = True
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.play_button = pygame.image.load("./textures/btn/start.png")

    def win(self):
        self.group.update()

        #Vérification de collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.wayout) > -1:
                #self.is_playing = False

                player_position = self.tmx_data.get_object_by_name("player")
                self.player = Player(player_position.x, player_position.y)

                # Centrer la caméra sur le joueur
                self.group.center(self.player.rect.center)
                self.group.draw(self.screen)


                #self.song.stop()
        pygame.display.flip()


    def run(self):

        clock = pygame.time.Clock()

        #Boucle du jeu
        launched = True

        

        while launched:

            self.screen.blit(self.background, (0,0))

            if self.is_playing:

                self.player.save_location()

                # Afficher la touche dans la console si print("x") 
                self.handle_input()

                # Mettre à jour le déplacement du joueur
                self.update()

                # Centrer la caméra sur le joueur
                self.group.center(self.player.rect.center)
                self.group.draw(self.screen)

                # Si le joueur gagne
                self.win()

            else:
                
                self.start()

            # Rafraîchissement de l'écran
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = False

            clock.tick(60)

        pygame.quit()