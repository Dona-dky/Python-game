import pygame

class Attack(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./textures/player/rivaille_levi___attack_on_titan__rpg_maker_vx_ace__by_iceblue007_d71hcgx.png')
        self.velocity = 5
        self.rect = self.image.get_rect()