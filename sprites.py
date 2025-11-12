import pygame
from constants import *
import numpy as np
from animation import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("assets/image/spritesheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.sheet = pygame.image.load("assets/image/pacman.png").convert()
        self.sheet.set_colorkey((0, 0, 0))
        self.entity = entity
        self.entity.image = self.getStartImage()

        self.animations = {}
        self.defineAnimations()
        self.stopimage = (6, 0)

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((8, 0), (10, 0), (12, 0), (14, 0)))
        self.animations[RIGHT] = Animator(((0, 0), (2, 0), (4, 0), (6, 0)))
        self.animations[UP] = Animator(((16, 0), (18, 0), (20, 0), (22, 0)))
        self.animations[DOWN] = Animator(((24, 0), (26, 0), (28, 0), (30, 0)))
        self.animations[DEATH] = Animator(((0, 2), (2, 2), (4, 2), (6, 2), (8, 2), (10, 2), (12, 2), (14, 2), (16, 2), (18, 2), (20, 2), (22, 2), (24, 2)), speed=6, loop=False)

    def update(self, dt):
        if self.entity.alive == True:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (14, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (6, 0)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (22, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (30, 0)
            elif self.entity.direction == STOP:
                self.entity.image = self.getImage(*self.stopimage)
        else:
            self.entity.image = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(6, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)
    

class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        self.entity = entity
        self.entity.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def update(self, dt):
        pass

class FreightSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.sheet = pygame.image.load('assets/image/frightened.png').convert()
        self.sheet.set_colorkey(BLACK)
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.freightAnimation = Animator(((0, 0), (2, 0)))
        self.blinkAnimation = Animator(((0, 0), (2, 0), (0, 0), (2, 0), (4, 0), (6, 0), (4, 0), (6, 0)))

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def update(self, dt):
        if self.entity.mode.timer < 5:
            self.entity.image = self.getImage(*self.freightAnimation.update(dt))
        else:
            self.entity.image = self.getImage(*self.blinkAnimation.update(dt))

class SpawnSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)

        self.sheet = pygame.image.load('assets/image/ghost_eaten.png').convert()

        self.sheet.set_colorkey((0, 0, 0))
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((2, 0),))
        self.animations[RIGHT] = Animator(((0, 0),))
        self.animations[UP] = Animator(((4, 0),))
        self.animations[DOWN] = Animator(((6, 0),))

    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == UP:
            self.entity.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.direction == DOWN:
            self.entity.image = self.getImage(*self.animations[DOWN].update(dt))

class BlinkySprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)

        self.sheet = pygame.image.load("assets/image/blinky.png").convert()

        self.sheet.set_colorkey((0, 0, 0))
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def loadSpriteSheet(self):
        if self.level == 1:
            self.sheet = pygame.image.load("assets/image/blinky.png").convert()
        elif self.level == 2:
            self.sheet = pygame.image.load("assets/image/akatsuki_blinky.png").convert()
        elif self.level == 3:
            self.sheet = pygame.image.load("assets/image/squidgame_blinky.png").convert()
        elif self.level == 4:
            self.sheet = pygame.image.load("assets/image/superman.png").convert()
        elif self.level == 5:
            self.sheet = pygame.image.load("assets/image/winx_blinky.png").convert()


        self.sheet.set_colorkey(BLACK)

    def setLevel(self, level):
        self.level = level + 1
        self.loadSpriteSheet()
        self.entity.image = self.getStartImage()

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((4, 0), (6, 0)))
        self.animations[RIGHT] = Animator(((0, 0), (2, 0)))
        self.animations[UP] = Animator(((8, 0), (10, 0)))
        self.animations[DOWN] = Animator(((12, 0), (14, 0)))

    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == UP:
            self.entity.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.direction == DOWN:
            self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class PinkySprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.sheet.set_colorkey(BLACK)

        self.sheet = pygame.image.load("assets/image/pinky.png").convert()

        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def loadSpriteSheet(self):
        if self.level == 1:
            self.sheet = pygame.image.load("assets/image/pinky.png").convert()
        elif self.level == 2:
            self.sheet = pygame.image.load("assets/image/akatsuki_pinky.png").convert()
        elif self.level == 3:
            self.sheet = pygame.image.load("assets/image/squidgame_pinky.png").convert()
        elif self.level == 4:
            self.sheet = pygame.image.load("assets/image/batman.png").convert()
        elif self.level == 5:
            self.sheet = pygame.image.load("assets/image/winx_pinky.png").convert()

        self.sheet.set_colorkey(BLACK)

    def setLevel(self, level):
        self.level = level + 1
        self.loadSpriteSheet()
        self.entity.image = self.getStartImage()

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((4, 0), (6, 0)))
        self.animations[RIGHT] = Animator(((0, 0), (2, 0)))
        self.animations[UP] = Animator(((8, 0), (10, 0)))
        self.animations[DOWN] = Animator(((12, 0), (14, 0)))

    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == UP:
            self.entity.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.direction == DOWN:
            self.entity.image = self.getImage(*self.animations[DOWN].update(dt))

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class InkySprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.sheet.set_colorkey(BLACK)

        self.sheet = pygame.image.load("assets/image/inky.png").convert()

        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def loadSpriteSheet(self):
        if self.level == 1:
            self.sheet = pygame.image.load("assets/image/inky.png").convert()
        elif self.level == 2:
            self.sheet = pygame.image.load("assets/image/akatsuki_inky.png").convert()
        elif self.level == 3:
            self.sheet = pygame.image.load("assets/image/squidgame_inky.png").convert()
        elif self.level == 4:
            self.sheet = pygame.image.load("assets/image/spiderman.png")
        elif self.level == 5:
            self.sheet = pygame.image.load("assets/image/winx_inky.png")

        self.sheet.set_colorkey(BLACK)

    def setLevel(self, level):
        self.level = level + 1
        self.loadSpriteSheet()
        self.entity.image = self.getStartImage()

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((4, 0), (6, 0)))
        self.animations[RIGHT] = Animator(((0, 0), (2, 0)))
        self.animations[UP] = Animator(((8, 0), (10, 0)))
        self.animations[DOWN] = Animator(((12, 0), (14, 0)))

    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == UP:
            self.entity.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.direction == DOWN:
            self.entity.image = self.getImage(*self.animations[DOWN].update(dt))

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class ClydeSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.sheet.set_colorkey(BLACK)

        self.sheet = pygame.image.load("assets/image/clyde.png").convert()

        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def loadSpriteSheet(self):
        if self.level == 1:
            self.sheet = pygame.image.load("assets/image/clyde.png").convert()
        elif self.level == 2:
            self.sheet = pygame.image.load("assets/image/akatsuki_clyde.png").convert()
        elif self.level == 3:
            self.sheet = pygame.image.load("assets/image/squidgame_clyde.png").convert()
        elif self.level == 4:
            self.sheet = pygame.image.load("assets/image/ironman.png").convert()
        elif self.level == 5:
            self.sheet = pygame.image.load("assets/image/winx_clyde.png").convert()

        self.sheet.set_colorkey(BLACK)

    def setLevel(self, level):
        self.level = level + 1
        self.loadSpriteSheet()
        self.entity.image = self.getStartImage()

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((4, 0), (6, 0)))
        self.animations[RIGHT] = Animator(((0, 0), (2, 0)))
        self.animations[UP] = Animator(((8, 0), (10, 0)))
        self.animations[DOWN] = Animator(((12, 0), (14, 0)))

    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
        elif self.entity.direction == RIGHT:
            self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
        elif self.entity.direction == UP:
            self.entity.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.direction == DOWN:
            self.entity.image = self.getImage(*self.animations[DOWN].update(dt))

    def getStartImage(self):
        return self.getImage(0, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class FruitSprites(Spritesheet):
    def __init__(self, entity, level):
        Spritesheet.__init__(self)
        self.entity = entity
        # self.entity.image = self.getStartImage()
        self.fruits = {0: (16, 8), 1: (18, 8), 2: (20, 8), 3: (16, 10), 4: (18, 10), 5: (20, 10)}
        self.entity.image = self.getStartImage(level % len(self.fruits))


    def getStartImage(self, key):
        # return self.getImage(16, 8)
        return self.getImage(*self.fruits[key])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.sheet = pygame.image.load("assets/image/pacman.png")
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(2, 0))

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)

class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)

                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)

                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value * 90)