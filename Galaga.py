import os
import sys
import pygame as pg
from pygame.locals import *

class Ship(object):
    def __init__(self, image, x, y):
        self.image = image
        self.xCoord = x
        self.yCoord = y
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.bulletHeight = int(self.height / 10)
        if self.bulletHeight < 2:
            self.bulletHeight = 2
        else:
            pass
        self.bulletWidth = int(self.bulletHeight / 2)
        self.bullets = []
        self.hasFired = False

    def fire(self):
        self.hasFired = True       

    def update(self, screen, newX, newY):
        self.xCoord = newX
        self.yCoord = newY
        screen.blit(self.image, (self.xCoord, self.yCoord))
        if self.hasFired or self.bullets:
            if len(self.bullets) < 2 and self.hasFired:
                bulletY = self.yCoord
                bulletX = self.xCoord + (self.width / 2)
                self.bullets.append(Bullet(self.bulletWidth,self.bulletHeight,
                                           bulletX,bulletY,self.bulletHeight * -1))
            for i in self.bullets:
                collided = i.update()
                if collided:
                    del(self.bullets[self.bullets.index(i)])
                else:
                    pass
            self.hasFired = False

class Bullet(object):
    def __init__(self, width, height, x, y, speed):
        self.originalImage = pg.image.load('images/bullet.png')
        self.image = pg.transform.scale(self.originalImage, (width, height))
        self.xCoord = int(x)
        self.yCoord = int(y)
        self.speed = speed
    
    def update(self):
        self.yCoord += self.speed
        if 0 <= self.yCoord <= SCREEN_HEIGHT:
            screen.blit(self.image, (self.xCoord, self.yCoord))
            return False
        else:
            return True

def pauseMenu(playerX, playerY):
    paused = True
    while paused:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_BACKSPACE:
                    userQuit = False
                    paused = False
            if event.type == QUIT: 
                userQuit = True
                paused = False

        showPause()
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Schnapsen but not | FPS: ' + fps)
        pg.display.update()
        clock.tick(60)
    
    if userQuit:
        pg.quit()
        quit()
    
    else:
        return

def mainGameLoop(x,y):
    running = True
    hasFired = False
    while running: # Game loop - each loop is a frame
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_BACKSPACE:
                    userQuit = False
                    running = False
                if event.key == K_SPACE:
                    playerShip.fire()
            if event.type == QUIT: 
                userQuit = True
                running = False

        key = pg.key.get_pressed()
            
        if not key[K_RIGHT] and not key[K_d] and not key[K_LEFT] and not key[K_a]:
            shipImage = originalShipImage
            
        if key[K_RIGHT] or key[K_d]:
            x += xChange
            if x > SCREEN_WIDTH - SHIP_WIDTH:
                x = int(SCREEN_WIDTH - SHIP_WIDTH)

        elif key[K_LEFT] or key[K_a]:
            x -= xChange
            if x < 0:
                x = 0

        screen.fill(BG_COLOUR)
        playerShip.update(screen,x,y)
                
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Schnapsen but not | FPS: ' + fps)
        pg.display.update()
        clock.tick(60)

    if userQuit:
        pg.quit()
        quit()
    
    else:
        pauseMenu(x,y)
        
while True:
    pg.init() # Initialises pygame module

    ## Defining constants
    with open('options.txt') as f: # Reading game options from txt
        options = f.readlines()

    for line in options: # This loop removes comment lines from options.txt
        if line[0] == '#':
            del(options[options.index(line)])
        else: pass
        
    SCREEN_WIDTH = int(options[0])
    SCREEN_HEIGHT = int(options[1])

    if (SCREEN_WIDTH - 800) < (SCREEN_HEIGHT - 600):
        # Image scale used based on screen size
        SHIP_SIZE_MULT = SCREEN_WIDTH / 800
    else:
        SHIP_SIZE_MULT = SCREEN_HEIGHT / 600

    BG_COLOUR = (0, 0, 0)

    PLAYER_IMG_WIDTH = 64
    PLAYER_IMG_HEIGHT = 64

    SHIP_WIDTH = PLAYER_IMG_WIDTH * SHIP_SIZE_MULT
    SHIP_HEIGHT = PLAYER_IMG_HEIGHT * SHIP_SIZE_MULT
    ## End of constants

    ## Setting up pygame essentials
    screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.fill(BG_COLOUR)
    font = pg.font.Font(None, 30)
    clock = pg.time.Clock()
    running = True
    userQuit = False
    ## End of essentials

    ## Setting up sprites for the game
    originalShipImage = pg.image.load('images/ship.png')
    # Resizing image
    shipImage = pg.transform.rotozoom(originalShipImage, 0, SHIP_SIZE_MULT)

    pauseImage = pg.image.load('images/pause.png')
    pauseImage = pg.transform.scale(pauseImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def showPause():
        screen.blit(pauseImage, (0, 0))

    x = int((SCREEN_WIDTH * 0.45))
    y = int((SCREEN_HEIGHT * 0.8))

    # Change in x coord when moving horizontal
    xChange = int(SCREEN_WIDTH * 0.0075)
    if xChange == 0:
        xChange = 1
    # Change in y coord when moving vertical
    yChange = int(SCREEN_HEIGHT * 0.0075)
    if yChange == 0:
        yChange = 1

    playerShip = Ship(shipImage, x, y)
    
    mainGameLoop(x,y)
    ## End of game sprites
