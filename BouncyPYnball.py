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
    -Bouncers prendem muito a bola, colisão não é suave (rever colisões)

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
        self.radius = 6
        
    def update(self):
        delta_x = self.speed*math.cos(self.angle)
        delta_y = self.speed*math.sin(self.angle)
        self.rect = self.rect.move(delta_x, delta_y)
        self.x = self.rect.x
        self.y = self.rect.y
        if self.rect.right >= 490 or self.rect.left <= 10:
            self.angle = math.pi - self.angle
        if self.rect.top <= 10:
            self.angle = -self.angle
        for x,y in zip(range(0,150,3),range(450,500,1)):
            if y+15 > self.rect.bottom > y and x-5 < self.rect.left < x:
                self.angle = math.radians(30) - self.angle
            #(debug colisão) pygame.draw.rect(backtext, (0,0,0), (x,y,5,20))
        for x,y in zip(range(500,350,-3),range(450,500,1)):
            if y+15 > self.rect.bottom > y and x-5 < self.rect.right < x:
                self.angle = -math.radians(30) - self.angle    
            #(debug colisão) pygame.draw.rect(backtext, (0,0,0), (x,y,5,20))

class Bouncer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("bumper1.png")
        screen = pygame.display.get_surface()
        self.radius = 29


        
def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    title = pygame.font.SysFont("Comic Sans MS", 38, True)
    subtitle = pygame.font.SysFont("Comic Sans MS", 20)
    titlesurf = title.render("Bouncy PYnball", True, (255,255,255))
    subtitlesurf = subtitle.render("Press 'Spacebar' to begin!", True, (255,255,255))
    clock = pygame.time.Clock()
    ball = Ball(0, random.randint(210,330))
    ball.rect.x=250
    ball.rect.y=30
    ballsprite = pygame.sprite.RenderPlain(ball)
    (bouncer1, bouncer1.rect.x, bouncer1.rect.y) = (Bouncer(), 230, 170) 
    (bouncer2, bouncer2.rect.x, bouncer2.rect.y) = (Bouncer(), 100, 300)
    (bouncer3, bouncer3.rect.x, bouncer3.rect.y) = (Bouncer(), 360, 300)
    bouncer1sprite = pygame.sprite.RenderPlain(bouncer1)
    bouncer2sprite = pygame.sprite.RenderPlain(bouncer2)
    bouncer3sprite = pygame.sprite.RenderPlain(bouncer3)
    while True:
        distance1 = math.hypot(ball.rect.centerx - bouncer1.rect.centerx, ball.rect.centery - bouncer1.rect.centery)
        distance2 = math.hypot(ball.rect.centerx - bouncer2.rect.centerx, ball.rect.centery - bouncer2.rect.centery)
        distance3 = math.hypot(ball.rect.centerx - bouncer3.rect.centerx, ball.rect.centery - bouncer3.rect.centery)
        tangent1 = math.atan2(ball.rect.centery-bouncer1.rect.centery, ball.rect.centerx-bouncer1.rect.centerx)
        tangent2 = math.atan2(ball.rect.centery-bouncer2.rect.centery, ball.rect.centerx-bouncer2.rect.centerx)
        tangent3 = math.atan2(ball.rect.centery-bouncer3.rect.centery, ball.rect.centerx-bouncer3.rect.centerx)
        for event in pygame.event.get():
            if event.type == QUIT:
                return pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.speed = 6
                    titlesurf = pygame.Surface((0,0))
                    subtitlesurf = pygame.Surface((0,0))
        if ball.rect.bottom >= 590:
            ball.remove()
            ball = Ball(0, random.randint(210,330))
            ballsprite = pygame.sprite.RenderPlain(ball)
            ball.rect.x=250
            ball.rect.y=30
        if ball.radius + bouncer1.radius >= distance1:
            ball.angle = 2 * tangent1 - ball.angle
        if ball.radius + bouncer2.radius >= distance2:
            ball.angle = 2 * tangent2 - ball.angle
        if ball.radius + bouncer3.radius >= distance3:
            ball.angle = 2 * tangent3 - ball.angle
        clock.tick(60)
        screen.blit(backtext, (0,0))
        screen.blit(titlesurf, (120,100))
        screen.blit(subtitlesurf, (130, 150))
        ballsprite.update()
        ballsprite.draw(screen)
        bouncer1sprite.draw(screen)
        bouncer2sprite.draw(screen)
        bouncer3sprite.draw(screen)
        pygame.display.flip()

ball = Ball(0, random.randint(220,310))
ball.rect.x=250
ball.rect.y=30
#print(ball.rect.center)
#centro da bola: (6,7) em relação ao c.sup.esq
#raio: 6

#bouncer = Bouncer()
#bouncer.rect.x = 230
#bouncer.rect.y = 170
#print(bouncer.rect.center)
#centro do bouncer: (29,29) em relação ao c.sup.esq
#raio: 29

#distance = math.hypot(ball.rect.centerx - bouncer.rect.centerx, ball.rect.centery - bouncer.rect.centery)
#print(distance)

if __name__ == '__main__': main()