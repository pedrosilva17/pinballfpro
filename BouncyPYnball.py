# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:49:25 2020

@author: Pedro Silva
"""

"""
Observações:
    -(CORRIGIDO) Bola passa pelos suportes laterais dos flippers em certas
    situações, penso que seja em caso de incidência
    perpendicular à superfície (rever colisões)
    
    -Bouncers e flippers provocam muitas colisões de uma só vez (a 
    pontuação sobe mais do que 1 a cada colisão), como limitá-las?

    
"""
    
import pygame
import math
import os
import getopt
import random
from socket import *
from pygame.locals import *

#ecrã e janela

ic= pygame.image.load("C:/Users/Public/Documents/Projeto/pinball.jpg")
icon= pygame.display.set_icon(ic)
pygame.display.set_caption("Bouncy PYnball")

def load_png(name):
    fullname = os.path.join('C:/Users/Public/Documents/Projeto', name)
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
backtext = pygame.image.load("C:/Users/Public/Documents/Projeto/backgroundtexture.png").convert()

#cenas temporárias
#esq: dx=130, dy=27, x=0, y=450
#dir: dx=130, dy=27, x=370, y=450
pygame.draw.rect(backtext, (255,0,0), (0,590,500,10))
pygame.draw.rect(backtext, (139,69,19), (0,0,10,600))
pygame.draw.rect(backtext, (139,69,19), (490,0,10,600))
pygame.draw.rect(backtext, (139,69,19), (0,0,500,10))
support1 = pygame.draw.rect(backtext, (139,69,19), (10,480,112,120))
support2 = pygame.draw.rect(backtext, (139,69,19), (383,480,112,120))
#fim das cenas temporárias

class Ball(pygame.sprite.Sprite):
    def __init__(self, speed, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("rsz_pinballsprite.png")
        screen = pygame.display.get_surface()
        surf = pygame.Surface((6,7))
        self.surf = surf
        self.area = screen.get_rect()
        self.speed = speed
        self.angle = math.radians(-angle)
        self.radius = 6
        self.mask = pygame.mask.from_surface(surf)
        
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

class Bouncer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("bumper1.png")
        surf = pygame.Surface((58,58))
        self.surf = surf
        screen = pygame.display.get_surface()
        self.radius = 29
        self.mask = pygame.mask.from_surface(surf)

class LeftFlipper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("flipper1.png")
        screen = pygame.display.get_surface()
        surf = pygame.Surface((94,27))
        self.surf = surf
        self.area = screen.get_rect()
        self.mask = pygame.mask.from_surface(surf)
        
        
class RightFlipper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("flipper2.png")
        screen = pygame.display.get_surface()
        surf = pygame.Surface((94,27))
        self.surf = surf
        self.area = screen.get_rect()
        self.mask = pygame.mask.from_surface(surf)

        
def main():
#JANELA
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    
#TEXTO
    title = pygame.font.SysFont("Comic Sans MS", 38, True)
    subtitle = pygame.font.SysFont("Comic Sans MS", 20)
    score = 0
    scoretext = pygame.font.SysFont("Comic Sans MS", 10)
    titlesurf = title.render("Bouncy PYnball", True, (255,255,255))
    subtitlesurf = subtitle.render("Press 'Spacebar' to begin!", True, (255,255,255))
    
#CLOCK
    clock = pygame.time.Clock()
    
#OBJETOS
    keys = pygame.key.get_pressed()
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
    (flipper1, flipper2) = (LeftFlipper(), RightFlipper())
    flipper1.rect.x, flipper2.rect.x = (120, 290)
    flipper1.rect.y, flipper2.rect.y = (478, 478)
    flipper1sprite = pygame.sprite.RenderPlain(flipper1)
    flipper1ogimage = flipper1.image
    flipper1ogsurf = flipper1.surf
    flipper2ogimage = flipper2.image
    flipper2ogsurf = flipper2.surf
    flipper2sprite = pygame.sprite.RenderPlain(flipper2)
    
#WHILE LOOP
    while True:
        scoretextsurf = subtitle.render("Score {0}".format(score), False, (255,255,255))
        tangent1 = math.atan2(ball.rect.centery-bouncer1.rect.centery, ball.rect.centerx-bouncer1.rect.centerx)
        tangent2 = math.atan2(ball.rect.centery-bouncer2.rect.centery, ball.rect.centerx-bouncer2.rect.centerx)
        tangent3 = math.atan2(ball.rect.centery-bouncer3.rect.centery, ball.rect.centerx-bouncer3.rect.centerx)
        colangle1 = 0.5 * math.pi + tangent1
        colangle2 = 0.5 * math.pi + tangent2
        colangle3 = 0.5 * math.pi + tangent3 
        for event in pygame.event.get():
            if event.type == QUIT:
                return pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.speed = 9
                    titlesurf = pygame.Surface((0,0))
                    subtitlesurf = pygame.Surface((0,0))
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    flipper1.image= pygame.transform.rotate(flipper1.image, 30)
                    flipper1.surf= pygame.transform.rotate(flipper1.surf, 30)
                    flipper1.mask= pygame.mask.from_surface(flipper1.surf)
                    flipper1.rect.x = 110
                    flipper1.rect.y = 430
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    flipper2.image= pygame.transform.rotate(flipper2.image, -30)
                    flipper2.surf= pygame.transform.rotate(flipper2.surf, -30)
                    flipper2.mask= pygame.mask.from_surface(flipper2.surf)
                    flipper2.rect.x = 300
                    flipper2.rect.y = 430
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    flipper1.image= flipper1ogimage
                    flipper1.surf= flipper1ogsurf
                    flipper1.mask= pygame.mask.from_surface(flipper1.surf)
                    flipper1.rect.x = 120
                    flipper1.rect.y = 478
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    flipper2.image= flipper2ogimage
                    flipper2.surf= flipper2ogsurf
                    flipper2.mask= pygame.mask.from_surface(flipper2.surf)
                    flipper2.rect.x = 290
                    flipper2.rect.y = 478
                if event.key == pygame.K_k:
                    ball.angle+= math.radians(30)
#COLISÕES
        if ball.rect.bottom >= 590:
            ball.remove()
            ball = Ball(0, random.randint(210,330))
            ballsprite = pygame.sprite.RenderPlain(ball)
            ball.rect.x=250
            ball.rect.y=30    
        if pygame.sprite.collide_mask(ball, bouncer1):
            ball.angle = 2 * tangent1 - ball.angle
            ball.rect.x += 2 * math.sin(colangle1)
            ball.rect.y -= 2 * math.cos(colangle1)
            score += 1
        if pygame.sprite.collide_mask(ball, bouncer2):
            ball.angle = 2 * tangent2 - ball.angle
            ball.rect.x += 2 * math.sin(colangle2)
            ball.rect.y -= 2 * math.cos(colangle2)
            score += 1
        if pygame.sprite.collide_mask(ball, bouncer3):
            ball.angle = 2 * tangent3 - ball.angle
            ball.rect.x += 2 * math.sin(colangle3)
            ball.rect.y -= 2 * math.cos(colangle3)
            score += 1
        if pygame.sprite.collide_mask(ball, flipper1):
            if flipper1.surf == flipper1ogsurf:
                ball.angle = math.radians(30) - ball.angle
                ball.rect.x += 2
                ball.rect.y -= 3
            else:
                ball.angle = -math.radians(30) - ball.angle
                ball.rect.x -= 2
                ball.rect.y -= 3
        if pygame.sprite.collide_mask(ball, flipper2):
            if flipper2.surf == flipper2ogsurf:
                ball.angle = -math.radians(30) - ball.angle
                ball.rect.x -= 2
                ball.rect.y -= 3
            else:
                ball.angle = math.radians(30) - ball.angle
                ball.rect.x += 2
                ball.rect.y -= 3
        if ball.rect.colliderect(support1) or ball.rect.colliderect(support2):
            ball.angle = -ball.angle

#UPDATES E BLITS
        clock.tick(60)
        screen.blit(backtext, (0,0))
        screen.blit(titlesurf, (120,100))
        screen.blit(subtitlesurf, (130, 150))
        screen.blit(scoretextsurf, (390, 530))
        ballsprite.update()
        ballsprite.draw(screen)
        bouncer1sprite.draw(screen)
        bouncer2sprite.draw(screen)
        bouncer3sprite.draw(screen)
        flipper1sprite.draw(screen)
        flipper2sprite.draw(screen)
        pygame.display.flip()

#ball = Ball(0, random.randint(220,310))
#ball.rect.x=250
#ball.rect.y=30

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
#(flipper1, flipper2) = (LeftFlipper(), RightFlipper())

if __name__ == '__main__': main()