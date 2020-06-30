#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:06:17 2020

@author: katemao
"""

import pygame, sys
from pygame.locals import *

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

class GradualAppearance:
    def __init__(self,string):
        
        self.string = string
        text = ''
        for i in range(len(string)):
            DISPLAYSURF.fill(WHITE)
            text += string[i]
            pygame.font.init()
            font = pygame.font.SysFont("myresources/fonts/Papyrus.ttf", 30) #Assign it to a variable font
            text_surface = font.render(text, True, (0, 128, 0)) 
        
            text_rect = text_surface.get_rect()
            text_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
            DISPLAYSURF.blit(text_surface, text_rect)
            pygame.display.update()
            pygame.time.wait(100)
    
    #def display_text_animation(self,string):
        

    def quitGame(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


a = GradualAppearance('YOUR QUANTUM EXPERIENCE STARTS HERE!')
#a.display_text_animation('no')
a.quitGame()

#display_text_animation('YOUR QUANTUM JOURNEY STARTS HERE!')
#main()