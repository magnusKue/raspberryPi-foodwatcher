import pygame 
from pygame.locals import *
import UiElements as ui
import productGetter
import time as timelib
import string, math

class WelcomePage:
    def __init__(self, pVs):
        self.name = "welcome page"
        sx = pVs.screenSize.x
        sy = pVs.screenSize.y
        self.uiElements = [
            ui.Button(
                pygame.font.SysFont(None, 24), 
                self.BFstart, 
                pVs.screenSize - pygame.Vector2(sx/2+int(sx * .2), sy/2+int(sy * .1)), 
                pygame.Vector2(int(sx * .4), int(sy * .2)), 
                "Start"
            ),
        ]


    def render(self, pVars, mousePos, events):
        mainSurface = pygame.Surface(pVars.screenSize)
        mainSurface.fill(pVars.cBackground)
        for element in self.uiElements:
            elemSurf = element.update(pVars, mousePos, events)
            mainSurface.blit(elemSurf, element.position)


        return mainSurface


    ## Functions executed by buttons
                   
    def BFstart(self, pVs):
        pVs.currentPage = HomePage(pVs)


class HomePage:
    def __init__(self, pVs):
        self.name = "home page"
        sx = pVs.screenSize.x
        sy = pVs.screenSize.y
        buttonFontSize = 48
        self.uiElements = [
            ui.Label(
                pygame.font.SysFont(None, 90), 
                pygame.Vector2(int(sx*0.02), int((sy*0.33) - int(sy*0.05))-5),
                pygame.Vector2(int(sx*0.06), int(sy*0.1)),
                "+"
            ),
            ui.Label(
                pygame.font.SysFont(None, 90), 
                pygame.Vector2(int(sx*0.02), int((sy*0.66) - int(sy*0.05))-5),
                pygame.Vector2(int(sx*0.06), int(sy*0.1)),
                "-"
            ),
            ui.Button(
                pygame.font.SysFont(None, buttonFontSize), 
                self.BFloadAddScanPage, 
                pygame.Vector2(int(sx*0.10), int((sy*0.33) - int(sy*0.1))),
                pygame.Vector2(int(sx*0.16), int(sy*0.2)), 
                "scan"
            ),
            ui.Button(
                pygame.font.SysFont(None, buttonFontSize), 
                self.BFmanual, 
                pygame.Vector2(int(sx*0.28), int((sy*0.33) - int(sy*0.1))),
                pygame.Vector2(int(sx*0.16), int(sy*0.2)), 
                "manual"
            ),
            ui.Button(
                pygame.font.SysFont(None, buttonFontSize), 
                self.BFloadremoveScanPage, 
                pygame.Vector2(int(sx*0.10), int((sy*0.66) - int(sy*0.1))),
                pygame.Vector2(int(sx*0.16), int(sy*0.2)), 
                "scan"
            ),
            ui.Button(
                pygame.font.SysFont(None, buttonFontSize), 
                self.BFselect, 
                pygame.Vector2(int(sx*0.28), int((sy*0.66) - int(sy*0.1))),
                pygame.Vector2(int(sx*0.16), int(sy*0.2)), 
                "select"
            )
        ]


    def render(self, pVars, mousePos, events):
        mainSurface = pygame.Surface(pVars.screenSize)
        mainSurface.fill(pVars.cBackground)
        for element in self.uiElements:
            elemSurf = element.update(pVars, mousePos, events)
            mainSurface.blit(elemSurf, element.position)

        return mainSurface


    ## Functions executed by buttons

    def BFloadAddScanPage(self, pVs):
        pVs.currentPage = ScanPage(pVs)
        pVs.currentPage.mode = 1

    def BFloadremoveScanPage(self, pVs):
        pVs.currentPage = ScanPage(pVs)
        pVs.currentPage.mode = 0

    def BFmanual(self, pVs):
        pVs.currentPage = addProductPage(pVs)

    def BFselect(self, pVs):
        pVs.currentPage = removeProductPage(pVs)


class ScanPage:
    def __init__(self, pVs):
        self.name = "scan page"
        self.mode = 1 # 0 = remove product | 1 = add product
        self.prodGetter = productGetter.ProductGetter()
        sx = pVs.screenSize.x
        sy = pVs.screenSize.y

        self.text = ""
        self.uiElements = [
            ui.Label(
                pygame.font.SysFont(None, 64), 
                pVs.screenSize - pygame.Vector2(sx/2+int(sx * .3), sy/2+int(sy * .06)), 
                pygame.Vector2(int(sx * .6), int(sy * .12)), 
                "scan barcode"
            ),

            ui.Image(
                "barcode.png",
                pygame.Vector2(pVs.screenSize.x/2,(pVs.screenSize.y-200)/2),
                1
            ),

            ui.Button(
                pygame.font.SysFont(None, 24), 
                self.BFhome, 
                pygame.Vector2(
                    sx * (0.1), 
                    sy * 0.86
                ), 
                pygame.Vector2(
                    int(sx * .8), 
                    int(sy * .07)
                ), 
                "cancel search"
            )

        ]


    def render(self, pVars, mousePos, events):

        self.update(events, pVars)

        mainSurface = pygame.Surface(pVars.screenSize)
        mainSurface.fill(pVars.cBackground)
        for element in self.uiElements:
            elemSurf = element.update(pVars, mousePos, events)
            mainSurface.blit(elemSurf, element.position)

        return mainSurface

    def update(self, events, pVs):
        oldtext = self.text
        for event in events:
            if event.type == KEYDOWN:
                self.text += event.unicode

        if oldtext == self.text and len(self.text) > 1:
            #print("registered "+self.text)
            self.text = self.text.replace("\r", "")
            
            result = self.prodGetter.getProduct(self.text)
            if self.mode:
                pVs.currentPage = addProductPage(pVs) 

                if result != 0:
                    self.text
                    brand = result["brand"]
                    name = result["name"]
                    pVs.currentPage.code = self.text
                    pVs.currentPage.product["name"] = brand+": "+name

                    found, resName, resDays = pVs.manager.searchProductByCode(self.text)
                    if found:
                        pVs.currentPage.product["name"] = resName
                        pVs.currentPage.product["days"] = resDays % 7
                        pVs.currentPage.product["weeks"] = int(resDays/7)
                    
                else:
                    pVs.currentPage.product["name"] = "not found"
            
            else:
                if result != 0:
                    pVs.manager.removeProductFromInventoryByCode(self.text, pVs)
                else:
                    pVs.currentPage = MessagePage(pVs, "scan failed", 2, HomePage) 

    ## Functions executed by buttons

    def BFhome(self, pVs):
        pVs.currentPage = HomePage(pVs)

class addProductPage:
    def __init__(self, pVs):
        self.name = "addProductPage"

        self.code = "-1"
        self.product = {
            "name" : "name",
            "weeks" : 0,
            "days" : 0
        }
        self.count = 1

        sx = pVs.screenSize.x
        sy = pVs.screenSize.y
        scaler = 0.12
        self.uiElements = [
            ui.Button(
                pygame.font.SysFont(None, 24), 
                self.BFchangeName, 
                pygame.Vector2(
                    sx * (0.1), 
                    sy * 0.08
                ), 
                pygame.Vector2(
                    int(sx * .8), 
                    int(sy * .07)
                ), 
                self.product["name"]
            ),

            ui.Label(
                pygame.font.SysFont(None, 72),
                pygame.Vector2(int((sx * 0.25 ) - sy * (0.5 * scaler) ), int(sy * (3/6))),
                pygame.Vector2(sy * scaler, sy * scaler),
                self.product["days"]
            ),

            ui.Label(
                pygame.font.SysFont(None, 72),
                pygame.Vector2(int((sx * 0.25 * 2) - sy * (0.5 * scaler) ), int(sy * (3/6))),
                pygame.Vector2(sy * scaler, sy * scaler),
                self.product["weeks"]
            ),

            ui.Label(
                pygame.font.SysFont(None, 72),
                pygame.Vector2(int((sx * 0.25 * 3) - sy * (0.5 * scaler) ), int(sy * (3/6))),
                pygame.Vector2(sy * scaler, sy * scaler),
                self.count
            ),



            ui.Label(
                pygame.font.SysFont(None, 24),
                pygame.Vector2(int((sx * 0.25 ) - sy * (0.5 * scaler) - 70), int(sy * (3/6))),
                pygame.Vector2(sy * scaler, sy * scaler),
                "Days: "
            ),

            ui.Label(
                pygame.font.SysFont(None, 24),
                pygame.Vector2(int((sx * 0.25 * 2) - sy * (0.5 * scaler) - 70), int(sy * (3/6))),
                pygame.Vector2(sy * scaler, sy * scaler),
                "Weeks: "
            ),

            ui.Label(
                pygame.font.SysFont(None, 24),
                pygame.Vector2(int((sx * 0.25 * 3) - sy * (0.5 * scaler) - 70), int(sy * (3/6))),
                pygame.Vector2(sy * scaler, sy * scaler),
                "Count: "
            ),



            ui.Button(
                pygame.font.SysFont(None, 24), 
                self.BFhome, 
                pygame.Vector2(
                    sx * (0.1), 
                    sy * 0.86
                ), 
                pygame.Vector2(
                    int(sx * .4) - 2, 
                    int(sy * .07)
                ), 
                "cancel"
            ),
            ui.Button(
                pygame.font.SysFont(None, 24), 
                self.BFadd, 
                pygame.Vector2(
                    sx * (0.1) + int(sx * .4) + 4, 
                    sy * 0.86
                ), 
                pygame.Vector2(
                    int(sx * .4) - 2, 
                    int(sy * .07)
                ), 
                "add"
            )
        ]
        functions = [
            self.BFdaysUp, 
            self.BFweeksUp, 
            self.BFcountUp, 
            
            self.BFdaysDown, 
            self.BFweeksDown, 
            self.BFcountDown
        ]

        for x in range(3):
            [self.uiElements.append(element) for element in  [
                ui.Button(
                    pygame.font.SysFont(None, 48),
                    functions[x],
                    pygame.Vector2(int((sx * 0.25 * (x+1)) - sy * (0.5 * scaler) ) ,int(sy * (2/6))),
                    pygame.Vector2(sy * scaler, sy * scaler),"+"
                ),
                
                ui.Button(
                    pygame.font.SysFont(None, 48),
                    functions[3+x],
                    pygame.Vector2(int((sx * 0.25 * (x+1)) - sy * (0.5 * scaler) ), int(sy * (4/6))),
                    pygame.Vector2(sy * scaler, sy * scaler),"-"
                )]]


    def render(self, pVars, mousePos, events):
        self.update()

        mainSurface = pygame.Surface(pVars.screenSize)
        mainSurface.fill(pVars.cBackground)
        for element in self.uiElements:
            elemSurf = element.update(pVars, mousePos, events)
            mainSurface.blit(elemSurf, element.position)

        return mainSurface

    def update(self):
        self.uiElements[0].displayName = self.product["name"] + "       |  tap to edit"
        self.uiElements[1].displayName = str(self.product["days"])
        self.uiElements[2].displayName = str(self.product["weeks"])
        self.uiElements[3].displayName = str(self.count)

    def handleKeyboard(self, text):
        self.product["name"] = text
    ## Functions executed by buttons

    def BFchangeName(self, pVs):
        pVs.currentPage = KeyboardPage(pVs, pVs.currentPage)
        pVs.currentPage.text = self.product["name"]
        pVs.currentPage.days = self.product["days"]
        pVs.currentPage.weeks = self.product["weeks"]
        pVs.currentPage.code = self.code
        pVs.currentPage.count = self.count

    def BFdaysUp(self, pVs):
        self.product["days"] += 1

    def BFdaysDown(self, pVs):
        self.product["days"] = max(0, self.product["days"]-1)

    def BFweeksUp(self, pVs):
        self.product["weeks"] += 1

    def BFweeksDown(self, pVs):
        self.product["weeks"] = max(0, self.product["weeks"]-1)

    def BFcountUp(self, pVs):
        self.count += 1

    def BFcountDown(self, pVs):
        self.count = max(1, self.count-1)

    def BFadd(self, pVs):
        for x in range(self.count):
            pVs.manager.addProductToInventory(
                str(self.product["name"]),
                int(self.product["days"]) + 7*int(self.product["weeks"]),
                str(self.code)
            )
        pVs.currentPage=MessagePage(pVs, "successfully added \" "+str(self.product["name"])+" \"", 2, HomePage)

    def BFhome(self, pVs):
        pVs.currentPage = HomePage(pVs)


class MessagePage:
    def __init__(self, pVs, message, time, link):
        self.name = "message"
        
        self.time = time
        self.startTime = timelib.time()

        self.link = link

        sx = pVs.screenSize.x
        sy = pVs.screenSize.y
        self.uiElements = [
            ui.Label(
                pygame.font.SysFont(None, 48), 
                pygame.Vector2(0, int(sy/2 - (sx*.05))), 
                pygame.Vector2(int(sx), int(sy*.1)), 
                message
            )
        ]

    def render(self, pVars, mousePos, events):
        self.update(pVars)

        mainSurface = pygame.Surface(pVars.screenSize)
        mainSurface.fill(pVars.cBackground)
        for element in self.uiElements:
            elemSurf = element.update(pVars, mousePos, events)
            mainSurface.blit(elemSurf, element.position)

        return mainSurface
    
    def update(self, pVs):
        if timelib.time() > self.startTime + self.time:
            pVs.currentPage = self.link(pVs)


class KeyboardPage:
    def __init__(self, pVs, link):
        self.name = "keyboard page"

        self.link = link
        self.text = ""
        self.keys = list(string.ascii_uppercase)
        sx = pVs.screenSize.x
        sy = pVs.screenSize.y
        self.uiElements = [
            ui.Label(
                pygame.font.Font(None, 48),
                pygame.Vector2(0,0),
                pygame.Vector2(sx,100),
                "text"

            )
        ]

        columns = 8
        buttonSize = 100
        keyboardSize = pygame.Vector2((columns * buttonSize) + ((columns-1) * 4), 100)
        offs = pygame.Vector2(int(sy*0.1), int((sx - keyboardSize.x) / 2))
        for x, item in enumerate(self.keys):
            button = ui.Button(
                pygame.font.Font(None, 48),
                self.BFaddChar,
                pygame.Vector2(offs.x + x%columns * (buttonSize+4), offs.y + (int(x/columns) * (buttonSize+4))),
                pygame.Vector2(buttonSize, buttonSize),
                item
            )
            button.arg = item
            self.uiElements.append(button)

        x += 1
        button = ui.Button(
                    pygame.font.Font(None, 48),
                    self.BFaddChar,
                    pygame.Vector2(offs.x + x%columns * (buttonSize+4), offs.y + (int(x/columns) * (buttonSize+4))),
                    pygame.Vector2(buttonSize*3+8, buttonSize),
                    " "
                )
        button.arg = " "
        self.uiElements.append(button)


        x += 3
        self.uiElements.append(
                ui.Button(
                    pygame.font.Font(None, 48),
                    self.BFremoveChar,
                    pygame.Vector2(offs.x + x%columns * (buttonSize+4), offs.y + (int(x/columns) * (buttonSize+4))),
                    pygame.Vector2(buttonSize*2 + 4, buttonSize),
                    "del"
                )
            )
        
        x+=2
        self.uiElements.append(
                ui.Button(
                    pygame.font.Font(None, 48),
                    self.BFdone,
                    pygame.Vector2(offs.x + x%columns * (buttonSize+4), offs.y + (int(x/columns) * (buttonSize+4))),
                    pygame.Vector2(buttonSize, buttonSize),
                    "ok"
                )
            )
        #self.uiElements.append(
        #        ui.Button(
        #            pygame.font.Font(None, 48),
        #            self.BFaddChar,
        #            pygame.Vector2(x+1%columns * (buttonSize+4), 120 + (int(x+1/columns) * (buttonSize+4))),
        #            pygame.Vector2(buttonSize, buttonSize),
        #            " "
        #        )
        #    )
        


    def render(self, pVars, mousePos, events):
        self.update(pVars)
        mainSurface = pygame.Surface(pVars.screenSize)
        mainSurface.fill(pVars.cBackground)
        for element in self.uiElements:
            elemSurf = element.update(pVars, mousePos, events)
            mainSurface.blit(elemSurf, element.position)


        return mainSurface

    def update(self, pVars):
        c = ""
        if timelib.time() % 1 > 0.5: c ="|"
        self.uiElements[0].displayName = self.text + c
    ## Functions executed by buttons
                   
    def BFaddChar(self, pVs, arg):
        self.text += arg

    def BFremoveChar(self, pVs):
        if len(self.text) >= 1:
            self.text = self.text[:-1]

    def BFdone(self, pVs):
        self.link.handleKeyboard(self.text.strip())
        pVs.currentPage = self.link

class removeProductPage:
    def __init__(self, pVs):
        self.name = "remove product page"
        sx = pVs.screenSize.x
        sy = pVs.screenSize.y

        self.inventory = pVs.manager.getInventory()
        self.maxElementsPerPage = 7
        self.currentPage = 0
        self.uiElements = []


    def render(self, pVars, mousePos, events):
        self.update(pVars)

        mainSurface = pygame.Surface(pVars.screenSize)
        mainSurface.fill(pVars.cBackground)
        for element in self.uiElements:
            elemSurf = element.update(pVars, mousePos, events)
            mainSurface.blit(elemSurf, element.position)

        return mainSurface

    def update(self, pVs):
        self.inventory = pVs.manager.getInventory() # update in case items got removed
        self.uiElements = []
        sx = pVs.screenSize.x
        sy = pVs.screenSize.y
        size = 0.07

        self.uiElements.append( 
            ui.Button(
                pygame.font.Font(None, 24),
                self.BFhome,
                pygame.Vector2(8,  int(sy * .9 - (0.5*(sx*size)))),
                pygame.Vector2(int(sx*size*1.5), sx*size),
                "cancel"
            )
        )
        
        if self.currentPage > 0:
            self.uiElements.append (
                    ui.Button(pygame.font.Font(None, 24),
                    self.BFlast,
                    pygame.Vector2(int(sx * .333 - (0.5*(sx*size))),  int(sy * .9 - (0.5*(sx*size)))),
                    pygame.Vector2(sx*size, sx*size),
                    "previous"
                )
            )

        self.uiElements.append (
                ui.Label(
                pygame.font.Font(None, 48),
                pygame.Vector2(int(sx * .5 - (0.5*(sx*size))),  int(sy * .9 - (0.5*(sx*size)))),
                pygame.Vector2(sx*size, sx*size),
                str(self.currentPage+1) + " / " + str(max(1, math.ceil( len(list(self.inventory.keys())) / self.maxElementsPerPage)))
            )
        )

        if len(list(self.inventory.keys())) == 0:
            self.uiElements.append( 
                ui.Label(pygame.font.Font(None, 48),
                    pygame.Vector2(0,0),
                    pygame.Vector2(sx, sy),
                    "no items in inventoy"
                )
            )

        if len(list(self.inventory.keys())) > (self.currentPage+1) * self.maxElementsPerPage:
            self.uiElements.append( 
                ui.Button(pygame.font.Font(None, 24),
                    self.BFnext,
                    pygame.Vector2(int(sx * .666 - (0.5*(sx*size))),  int(sy * .9 - (0.5*(sx*size)))),
                    pygame.Vector2(sx*size, sx*size),
                    "next"
                )
            )

        for i in range(min(self.maxElementsPerPage, len( list(self.inventory.keys())[0+(self.currentPage * self.maxElementsPerPage):]  ))):
            x = i+(self.currentPage * self.maxElementsPerPage)
            #x=i
            name = list(self.inventory.keys())[x]
            count = self.inventory[list(self.inventory.keys())[x]]
            ySize = (sy * 0.7) / self.maxElementsPerPage
            button = ui.Button(
                pygame.font.Font(None, 24),
                self.BFremove,
                pygame.Vector2(4,8 + ((x%self.maxElementsPerPage)*ySize + (((x%self.maxElementsPerPage)-1)*4))),
                pygame.Vector2(sx - 8, ySize),
                name + "  ( "+str(count)+" )"
                )
            button.arg = name
            self.uiElements.append(button)

    ## Functions executed by buttons

    def BFremove(self, pVs, name):
        print("removing "+str(name))
        pVs.manager.removeProductFromInventoryByName(pVs, name)

    def BFlast(self, pVs):
        self.currentPage = max(0, self.currentPage-1)

    def BFnext(self, pVs):
        if len(list(self.inventory.keys())) > (self.currentPage+1) * self.maxElementsPerPage:
            self.currentPage += 1

    def BFhome(self, pVs):
        pVs.currentPage = HomePage(pVs)