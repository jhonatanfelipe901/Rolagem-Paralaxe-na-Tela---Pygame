#32091982 - Jhonatan Felipe

from os.path import dirname, join

import pygame
from pygame.locals import *

import parallax

pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
pygame.display.set_caption('Exemplo de Uso Tela com rolagem Paralaxe')
pygame.mouse.set_visible(0)

mainSurface = parallax.ParallaxSurface((640, 480), pygame.RLEACCEL)

directory = dirname(__file__)
mainSurface.add(join(directory, 'p2.png'), 5)
mainSurface.add(join(directory, 'p3.png'), 2)
mainSurface.add(join(directory, 'p1.png'), 1)

run = True
speed = 0
t_ref = 0
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN and event.key == K_RIGHT:
            speed += 2
        if event.type == KEYUP and event.key == K_RIGHT:
            speed -= 2
        if event.type == KEYDOWN and event.key == K_LEFT:
            speed -= 4
        if event.type == KEYUP and event.key == K_LEFT:
            speed += 4

    mainSurface.scroll(speed)  # Mova o fundo com a velocidade definida
    time = pygame.time.get_ticks()

    if (time - t_ref) > 60:
        mainSurface.draw(screen)
        pygame.display.flip()
