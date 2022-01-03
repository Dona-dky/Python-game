import pygame
import pytmx
import pyscroll

class Game:

    def __init__(self):

        #self.screen = pygame.display.set_mode((640,480))
        self.screen = pygame.display.set_mode((800,600))

        pygame.display.set_caption("Pygamon - WOW")

        #Chargement et collage du fond
        #background = pygame.image.load("./textures/background/foot.jpg").convert()
        #self.screen.blit(background, (0,0))

        #Rafraîchissement de l'écran
        pygame.display.flip()

        #Son du jeu
        song = pygame.mixer.Sound("./sound/SNK.mp3")
        song.play()

        #Charger la carte du jeu
        tmx_data = pytmx.util_pygame.load_pygame('./textures/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        #dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def run(self):

        #Boucle du jeu
        launched = True

        while launched:

            self.group.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = False

            pygame.quit()