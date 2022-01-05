import pygame
from pygame import image

from animation import Animation

class Player(Animation):

    def __init__(self, x, y):
        super().__init__()
        
        #position de base du joueur vers le bas
        self.image = self.get_image(0, 0)

        #retirer le fond noir du joueur
        self.image.set_colorkey([0,0,0])

        self.rect = self.image.get_rect()
        self.position = [x, y]

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

        self.health = 100
        self.max_health = 100
        self.attack = 10

    #
    def save_location(self): self.old_position = self.position.copy()

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