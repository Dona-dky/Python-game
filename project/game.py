import pygame
import pytmx
import pyscroll

from player import Player

class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((630,450))
        #self.screen = pygame.display.set_mode((500,300))
        #self.screen = pygame.display.set_mode((1000,800))

        pygame.display.set_caption("LABYRINTHE - SNK")

        # Son du jeu
        song = pygame.mixer.Sound("./sound/SNK.mp3")
        song.play()

        # Charger la carte du jeu
        tmx_data = pytmx.util_pygame.load_pygame('./textures/background/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Définir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)


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


    def run(self):

        clock = pygame.time.Clock()

        #Boucle du jeu
        launched = True

        while launched:
            self.player.save_location()

            # Afficher la touche dans la console si print("x") 
            self.handle_input()

            # Mettre à jour le déplacement du joueur
            self.update()

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

            clock.tick(60)

        pygame.quit()