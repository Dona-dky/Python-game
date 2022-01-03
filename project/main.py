import pygame

pygame.init()



screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Pygamon - WOW")


launched = True

#Chargement et collage du fond
background = pygame.image.load("background.jpg").convert()
screen.blit(background, (0,0))

#Rafraîchissement de l'écran
pygame.display.flip()

while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False