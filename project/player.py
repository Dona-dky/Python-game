import pygame
from pygame import image

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('./textures/player/rivaille_levi___attack_on_titan__rpg_maker_vx_ace__by_iceblue007_d71hcgx.png')
        
        #position de base du joueur vers le bas
        self.image = self.get_image(0, 0)

        #retirer le fond noir du joueur
        self.image.set_colorkey([0,0,0])

        self.rect = self.image.get_rect()
        self.position = [x, y]

        #recuperer les images pour les positions du joueur
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = 1.3

        self.health = 100
        self.max_health = 100
        self.attack = 10

    #
    def save_location(self): self.old_position = self.position.copy()

    #Va rechercher l'image associé au déplacement
    def change_animation(self, name): 
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    # Modifier sa position en x
    def move_right(self): self.position[0] += self.speed
    def move_left(self): self.position[0] -= self.speed
    def move_up(self): self.position[1] -= self.speed
    def move_down(self): self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image