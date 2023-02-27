# this File contains the UI elements that are owned by the pages in pages.py

import pygame
import utilities
import os.path


class Button:
    def __init__(self, font, func, pos=pygame.Vector2(0,0), size=pygame.Vector2(30,30), displayName="Button"):
        self.state = 0 # 1 = hovered over | 2 = pressed
        
        self.displayName = displayName
        self.font = font
        

        self.position = pos
        self.size = size

        self.surface = pygame.Surface(self.size).fill((0,255,0))

        self.function = func
        self.arg = None

    def checkCollision(self, mousePos, events):
        return mousePos[0] > self.position.x and mousePos[0] < self.position.x + self.size.x and mousePos[1] > self.position.y and mousePos[1] < self.position.y + self.size.y

    def render(self, pVs):
        color = pVs.cUi1
        if self.state == 1: color = pVs.cUiHighlighted1
        elif self.state == 2: color = pVs.cRed
        self.surface = pygame.Surface(self.size)
        self.surface.fill(color)

        color = pVs.cBackground
        if self.state == 1: color = pVs.cUi1
        elif self.state == 2: color = pVs.cUi1

        img = self.font.render(self.displayName, True, color)
        textRect = img.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
        self.surface.blit(img, textRect)

        self.surface = utilities.roundSurface(self.surface, 4)
        

    def update(self, pVs, mousePos, events):
        # mouse hover / clicked
        #print(self.checkCollision(mousePos, events))
        #print(mousePos)
        self.state = 1 * self.checkCollision(mousePos, events)

        if pygame.MOUSEBUTTONDOWN in [event.type for event in events] and self.state == 1: 
            self.state = 2
            self.onClick(pVs)

        self.render(pVs)

        return self.surface
    
    def onClick(self, pVs):
        if self.arg:
            self.function(pVs, self.arg)
        else:
            self.function(pVs)

class Label:
    def __init__(self, font, pos=pygame.Vector2(0,0), size=pygame.Vector2(30,30), displayName="Label"):
        
        self.font = font

        self.displayName = displayName
        self.position = pos
        self.size = size

        self.surface = pygame.Surface([self.size.x, self.size.y], pygame.SRCALPHA)

    def render(self, pVs):
        self.surface = pygame.Surface([self.size.x, self.size.y], pygame.SRCALPHA)

        color = pVs.cUi2

        img = self.font.render(self.displayName, True, color)
        textRect = img.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
        self.surface.blit(img, textRect)
        

    def update(self, pVs, mousePos, events):  
        self.render(pVs)

        return self.surface

class Image:
    def __init__(self, src, centerPos=pygame.Vector2(0,0), scaleFactor=2):

        self.centerPos = centerPos

        self.scaleFactor = scaleFactor
        
        self.image = pygame.image.load(os.path.dirname(__file__)+"/../res/"+str(src)).convert_alpha()
        self.origImgSize = self.image.get_rect()
        
        self.surface =  pygame.transform.scale(self.image,(self.origImgSize.w * scaleFactor, self.origImgSize.h * scaleFactor))

        self.position =  self.centerPos - pygame.Vector2(int(self.surface.get_rect().w/2), int(self.surface.get_rect().h/2))

    def update(self, pVs, mousePos, events):  
        return self.surface