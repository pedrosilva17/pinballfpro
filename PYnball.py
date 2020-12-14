# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:49:25 2020

@author: Pedro Silva
"""

import pygame 
pygame.init()

window = pygame.display.set_mode((500, 600))

pygame.display.set_caption("PYnball")

def redrawWindow():
    window.fill((60,60,60))
    pinBall.draw(window)
    pygame.display.update()
    
x = 50
y = 50
width = 30
height = 50
vel = 5

class ball(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def draw(self, window):
        pygame.draw.circle(window, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius-1)
        

pinBall = ball(450, 550, 5, (255,255,255))
run = True
while run:
    pygame.time.delay(80)
    redrawWindow()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

pygame.quit()