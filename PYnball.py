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

def redrawWindow():
    window.fill((60,60,60))
    pygame.display.update()

    
x = 50
y = 50
width = 30
height = 50
vel = 5

class Ball(pygame.sprite.Sprite):
    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("pinballsprite.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        
    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)
        
def main():
    pygame.init()
    window = pygame.display.set_mode((500, 600))
    ic= pygame.image.load("C:/Users/Pedro Silva/Documents/FEUP/FPRO/Projeto/pinball.jpg")
    icon= pygame.display.set_icon(ic)
    pygame.display.set_caption("PYnball")
    
    clock= pygame.time.Clock()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                if event.key == K_RIGHT:
            
    
        
    

if __name__ == '__main__': main()