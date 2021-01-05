# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:49:25 2020

@author: Pedro Silva
"""

import pygame
import sys
import random
import math
import os
import getopt
from socket import *
from pygame.locals import *

#ecrã e janela

ic= pygame.image.load("C:/Users/Pedro Silva/Documents/FEUP/FPRO/Projeto/pinball.jpg")
icon= pygame.display.set_icon(ic)
pygame.display.set_caption("PYnball")

def load_png(name):
    fullname = os.path.join('C:/Users/Pedro Silva/Documents/FEUP/FPRO/Projeto', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image: ' + fullname)
        raise SystemExit(message)
    return image, image.get_rect()

screen = pygame.display.set_mode((500, 600))

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((80, 80, 80))



class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("rsz_pinballsprite.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = speed
        self.angle = math.radians(-angle)
        
    def update(self):
        delta_x = self.speed*math.cos(self.angle)
        delta_y = self.speed*math.sin(self.angle)
        self.rect = self.rect.move(delta_x, delta_y)
        if self.rect.right >= screen.get_width() or self.rect.left <= 0:
            hit_bounds = True
            self.angle = math.pi - self.angle
        if self.rect.top <= 0 or self.rect.bottom >= screen.get_height():
            hit_bounds = True
            self.angle = -self.angle

        
def main():
    pygame.init()
    background.fill((80, 80, 80))
    screen = pygame.display.set_mode((500, 600))
    clock= pygame.time.Clock()
    speed = 9
    ball = Ball(50, 50, 7, -45)
    ballsprite = pygame.sprite.RenderPlain(ball)
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return pygame.quit()
        screen.blit(background, (0,0))
        ballsprite.update()
        ballsprite.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()