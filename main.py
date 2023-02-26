# import librarys

import os, sys
import toml as tomllib
import database
# hide pygamesa buildt in welcome message
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # disable pygame welcome message

import pygame
from pygame.locals import * # dont require to use pygame namespace for often used constants

pygame.init()

from pages import *

class PVs: # general project variables
    def __init__(self):
        self.screenSize = pygame.Vector2(500,300)
        self.currentPage = None
        
        self.cBackground = pygame.Color("0x242331")

        self.cUi1 = pygame.Color("0x40531b")
        self.cUiHighlighted1 = pygame.Color("0xa6b07e")

        self.cUi2 = pygame.Color("0xc84630")
        self.cUiHighlighted2 = pygame.Color("0xf15025")
        self.cRed = pygame.Color(255,0,0)

        self.manager = database.Manager()
        self.loadTOML()

    def loadTOML(self):
        with open("config.toml", "r") as f:
            data = tomllib.load(f)
        self.screenSize = pygame.Vector2(data["screenSize"][0], data["screenSize"][1])

        self.cBackground = pygame.Color("#"+data["cBackground"].replace("#", ""))

        self.cUi1 = pygame.Color("#"+data["cUi1"].replace("#", ""))
        self.cUiHighlighted1 = pygame.Color("#"+data["cUiHighlighted1"].replace("#", ""))

        self.cUi2 = pygame.Color("#"+data["cUi2"].replace("#", ""))
        self.cUiHighlighted2 = pygame.Color("#"+data["cUiHighlighted2"].replace("#", ""))


pVs = PVs()

pVs.manager.checkFiles()

pVs.currentPage = WelcomePage(pVs)

running = True


root = pygame.display.set_mode() # main display object

while running:
    # store events so we can pass them onto the pages
    events = pygame.event.get()
    # handle quit event
    if pygame.QUIT in [event.type for event in events]:
        running = False

    # pass events onto current page and update it
    pageSurface = pVs.currentPage.render(pVs, pygame.mouse.get_pos(), events)

    root.blit(pageSurface, (0,0))

    pygame.display.flip()

pygame.quit()    
sys.exit()