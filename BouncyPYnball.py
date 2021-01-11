# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:49:25 2020

@author: Pedro Silva
"""

"""
BUGS:
    -Bola passa pelos suportes laterais dos flippers em certas
    situações, penso que seja em caso de incidência
    perpendicular à superfície (rever colisões)

"""
    
import pygame
import math
import os
import getopt
import random
from socket import *
from pygame.locals import *

#ecrã e janela

ic= pygame.image.load("C:/Users/Pedro Silva/Documents/FEUP/FPRO/Projeto/pinball.jpg")
icon= pygame.display.set_icon(ic)
pygame.display.set_caption("Bouncy PYnball")

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
backtext = pygame.image.load("C:/Users/Pedro Silva/Documents/FEUP/FPRO/Projeto/backgroundtexture.png").convert()

#cenas temporárias
pygame.draw.rect(backtext, (255,0,0), (0,590,500,10))
botleft = pygame.draw.polygon(backtext, (0,0,0), [(0,450),(150,500),(140,510),(0,460)])
botright= pygame.draw.polygon(backtext, (0,0,0), [(500,450),(350,500),(360,510),(500,460)])
pygame.draw.rect(backtext, (139,69,19), (0,0,10,600))
pygame.draw.rect(backtext, (139,69,19), (490,0,10,600))
pygame.draw.rect(backtext, (139,69,19), (0,0,500,10))
#fim das cenas temporárias

class Ball(pygame.sprite.Sprite):
    def __init__(self, speed, angle):
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
        if self.rect.right >= 490 or self.rect.left <= 10:
            hit_bounds = True
            self.angle = math.pi - self.angle
        if self.rect.top <= 10:
            hit_bounds = True
            self.angle = -self.angle
        for x,y in zip(range(0,150,3),range(450,500,1)):
            if y+15 > self.rect.bottom > y and x-5 < self.rect.left < x:
                self.angle = math.radians(30) - self.angle
            #(debug colisão) pygame.draw.rect(backtext, (0,0,0), (x,y,5,20))
        for x,y in zip(range(500,350,-3),range(450,500,1)):
            if y+15 > self.rect.bottom > y and x-5 < self.rect.right < x:
                self.angle = -math.radians(30) - self.angle    
            #(debug colisão) pygame.draw.rect(backtext, (0,0,0), (x,y,5,20))
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    clock= pygame.time.Clock()
    ball = Ball(0, random.uniform(220,310))
    ball.rect.x=250
    ball.rect.y=30
    ballsprite = pygame.sprite.RenderPlain(ball)
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.speed=9
        if ball.rect.bottom >= 590:
                ball.remove()
                ball = Ball(0, random.uniform(220,310))
                ballsprite = pygame.sprite.RenderPlain(ball)
                ball.rect.x=250
                ball.rect.y=30
        screen.blit(backtext, (0,0))
        clock.tick(60)
        ballsprite.update()
        ballsprite.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()