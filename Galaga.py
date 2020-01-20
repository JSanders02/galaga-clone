import os
import random
import pygame as pg
from pygame.locals import *
from math import sin, cos, radians, log10, ceil

class Ship(object):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(center= (int(SCREEN_WIDTH * 0.5),
                                                 int(SCREEN_HEIGHT * 0.1)))
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.bulletHeight = int(self.height / 5)
        if self.bulletHeight < 2:
            self.bulletHeight = 2
        else:
            pass
        self.bulletWidth = int(self.bulletHeight / 2)
        self.bullets = []
        self.hasFired = False

    def fire(self):
        self.hasFired = True # Shows that player has requested to fire  

    def update(self, newX, newY):
        self.rect.x = newX
        self.rect.y = newY
        screen.blit(self.image, self.rect)
        if self.hasFired or self.bullets:
            if len(self.bullets) < 2 and self.hasFired:
                # Instatiates another bullet - maximum of two on screen at once
                bulletY = self.rect.y
                bulletX = self.rect.centerx
                self.bullets.append(Bullet(self.bulletWidth,self.bulletHeight,
                                           bulletX,bulletY,self.bulletHeight * -2))
            for i in self.bullets:
                collided = i.update()
                if collided: # Stops updating bullets that have collided
                    del(self.bullets[self.bullets.index(i)])
                else:
                    pass

            self.hasFired = False

class Bullet(object):
    def __init__(self, width, height, x, y, speed):
        self.originalImage = pg.image.load('images/bullet.png')
        self.image = pg.transform.scale(self.originalImage, (width, height))
        self.rect = self.image.get_rect(midbottom = (int(x),int(y)))
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed
        if 0 <= self.rect.y <= SCREEN_HEIGHT: # If bullet is on-screen
            screen.blit(self.image, self.rect)
            return False # Returns not collided
        else:
            return True # Else returns collided

class Enemy(object):
    def __init__(self, eType, path):
        self.type = eType
        self.originalImage = pg.image.load('images/' + eType + '.png')
        self.image = pg.transform.rotozoom(self.originalImage,0,SHIP_SIZE_MULT)
        self.originalImage = self.image
        self.path = path
        if self.path == 1:
            self.direction = 90
            self.rect=self.image.get_rect(topright=(0,int(SCREEN_HEIGHT * 0.5)))
        elif self.path == 2:
            self.direction = 270
            self.rect=self.image.get_rect(topleft = (SCREEN_WIDTH,
                                                     int(SCREEN_HEIGHT * 0.5)))
        self.speed = xChange
        self.movingToFormation = True
        screen.blit(self.image, self.rect)
        
    def update(self):
        for i in playerShip.bullets:
            if self.rect.colliderect(i.rect):
                i.rect.y = -1
                return True

        if self.movingToFormation:
            if self.path == 1:
                if self.rect.y <= SCREEN_HEIGHT * 0.1 or self.direction > 90:
                    self.direction += 3
                    if 175 < self.direction < 185:
                        self.direction = 180
                        self.speed = 2
                        self.movingToFormation = False
                elif self.direction <= 30:
                    pass
                elif self.rect.y >= SCREEN_HEIGHT * 0.3:
                    self.direction -= 3
            
            elif self.path == 2:
                if self.rect.y <= SCREEN_HEIGHT * 0.1 or self.direction < 270:
                    self.direction -= 3
                    if 175 < self.direction < 185:
                        self.direction = 180
                        self.speed = 2
                        self.movingToFormation = False
                elif self.direction >= 330:
                    pass
                elif self.rect.y >= SCREEN_HEIGHT * 0.3:
                    self.direction += 3

            self.image = pg.transform.rotate(self.originalImage, 
                                             self.direction * -1)
            newCoords = moveInDir(radians(self.direction + 90),self.speed * -1)
            self.rect.x += newCoords[0]
            self.rect.y += newCoords[1]
        
        elif SCREEN_WIDTH * 0.1 < self.rect.x < SCREEN_WIDTH * 0.9:
            self.rect.x += self.speed
        
        else:
            self.speed = self.speed * -1
            self.rect.x += self.speed

        screen.blit(self.image, self.rect)
        return False
            
def moveInDir(direction, magnitude):
    # Allows a sprite to move in the direction it is facing
    x = magnitude * cos(direction)
    y = magnitude * sin(direction)
    return [int(x),int(y)]

def writeToOptions(width, height):
    with open('options.txt') as f:
        overwrite = f.readlines()

    overwrite[1], overwrite[3] = str(width) + '\n', str(height)

    with open('options.txt', 'w') as f:
        for i in overwrite:
            f.write(i)
            
def changeScreenSize(bg):
    changing = True
    selected = 0
    selectList = [widthSelectArrows, heightSelectArrows, confirmSelectArrows]
    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    pg.key.set_repeat(500, 5)

    def generateText(text):
        numDigits = int(log10(int(text))) + 1
        outputText = gameFont.render(text.upper(), False, (255, 255, 255))
        outputText = pg.transform.scale(outputText, 
                                        (int(SCREEN_WIDTH * (0.034375 * numDigits)), 
                                         int(SCREEN_HEIGHT * 0.05666)))  
        return outputText 

    widthText = generateText(str(width))
    heightText = generateText(str(height))

    def showMenu(selected):
        screen.blit(bg, (0,0))
        screen.blit(pausedTitleImage, (0,0))
        screen.blit(sizeMenuImage, (0,0))
        screen.blit(selectList[selected], (0,0))

    while changing:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    changing = False
                    pg.key.set_repeat(0, 0)
                    return False
                
                elif event.key == K_RETURN:
                    if selected == 2:
                        if width != SCREEN_WIDTH or height != SCREEN_HEIGHT:
                            changing = False
                            writeToOptions(width, height)
                            pg.key.set_repeat(0, 0)
                            return True
                        else:
                            changing = False
                            pg.key.set_repeat(0, 0)
                            return False
                    else:
                        pass

                elif event.key == K_UP or event.key == K_w:
                    if selected > 0:
                        selected -= 1
                    else:
                        pass

                elif event.key == K_DOWN or event.key == K_s:
                    if selected < 2:
                        selected += 1
                    else:
                        pass

                elif event.key == K_RIGHT or event.key == K_d:
                    if selected == 0:
                        if 100 <= width < 5000:
                            width += 2
                            widthText = generateText(str(width))

                    elif selected == 1:
                        if 100 <= height < 5000:
                            height += 2
                            heightText = generateText(str(height))
                
                elif event.key == K_LEFT or K_a:
                    if selected == 0:
                        if 100 < width <= 5000:
                            width -= 2
                            widthText = generateText(str(width))
                    
                    elif selected == 1:
                        if 100 < height <= 5000:
                            height -= 2
                            heightText = generateText(str(height))

            if event.type == QUIT:
                changing = False
        
        screen.fill(BG_COLOUR)
        showMenu(selected)
        screen.blit(widthText, (int(SCREEN_WIDTH * 0.43), 
                                int(SCREEN_HEIGHT * 0.45333)))
        
        screen.blit(heightText, (int(SCREEN_WIDTH * 0.43),
                                 int(SCREEN_HEIGHT * 0.6933)))
        pg.display.update()
        clock.tick(60)

    pg.quit()
    quit()
    
def pauseMenu(playerX, playerY):
    # Secondary gameloop for the pause menu - stops main one
    paused = True
    selected = optionSelectImage
    bgImage = pg.image.load('temp_bg.png')

    def showPause(selected): # Shows arrows over selected option
        screen.blit(pausedTitleImage, (0,0))
        screen.blit(pauseImage, (0, 0))
        screen.blit(selected, (0, 0))

    while paused:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = False
                    return False
                elif event.key == K_RETURN:
                    if selected == optionSelectImage:
                        if changeScreenSize(bgImage):
                            paused = False
                            return True
                        else:
                            pass
                    elif selected == resumeSelectImage:
                        paused = False
                        return False
                elif event.key == K_UP or event.key == K_w:
                    selected = optionSelectImage
                elif event.key == K_DOWN or event.key == K_s:
                    selected = resumeSelectImage
            if event.type == QUIT: 
                userQuit = True
                paused = False

        screen.fill(BG_COLOUR)
        screen.blit(bgImage, (0,0))
        showPause(selected)
        pg.display.update()
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Galaga | FPS: ' + fps)
        pg.display.update()
        clock.tick(60)

    pg.quit()
    quit()

def mainGameLoop(x,y):
    running = True
    enemy = Enemy('bug1', 2)

    while running: # Game loop - each loop is a frame
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.image.save(screen, 'temp_bg.png')
                    if pauseMenu(x,y):
                        running = False
                        userQuit = False
                if event.key == K_SPACE:
                    playerShip.fire()
            if event.type == QUIT: 
                userQuit = True
                running = False

        key = pg.key.get_pressed()
            
        if key[K_RIGHT] or key[K_d]:
            x += xChange
            if x > SCREEN_WIDTH - SHIP_WIDTH:
                x = int(SCREEN_WIDTH - SHIP_WIDTH)

        elif key[K_LEFT] or key[K_a]:
            x -= xChange
            if x < 0:
                x = 0

        screen.fill(BG_COLOUR)
        playerShip.update(x,y)

        try:
            if enemy.update():
                del enemy
        except:
            enemy = Enemy('bug1', random.choice([1,2]))
                
        fps = str(int(clock.get_fps()))
        pg.display.set_caption('Galaga | FPS: ' + fps)
        pg.display.update()
        clock.tick(60)

    if userQuit:
        pg.quit()
        quit()
        
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

    if (SCREEN_WIDTH - 1600) < (SCREEN_HEIGHT - 1200):
        # Image scale used based on screen size
        SHIP_SIZE_MULT = SCREEN_WIDTH / 1600
    else:
        SHIP_SIZE_MULT = SCREEN_HEIGHT / 1200

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

    pausedTitleImage = pg.image.load('images/game-paused-title.png')
    pausedTitleImage = pg.transform.scale(pausedTitleImage,
                                          (SCREEN_WIDTH, SCREEN_HEIGHT))

    pauseImage = pg.image.load('images/pause-menu.png')
    pauseImage = pg.transform.scale(pauseImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

    optionSelectImage = pg.image.load('images/selected-options.png')
    optionSelectImage = pg.transform.scale(optionSelectImage, 
                                           (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    resumeSelectImage = pg.image.load('images/selected-resume.png')
    resumeSelectImage = pg.transform.scale(resumeSelectImage, 
                                           (SCREEN_WIDTH, SCREEN_HEIGHT))

    sizeMenuImage = pg.image.load('images/size-menu.png')
    sizeMenuImage = pg.transform.scale(sizeMenuImage, 
                                       (SCREEN_WIDTH, SCREEN_HEIGHT))

    widthSelectArrows = pg.image.load('images/selected-width.png')
    widthSelectArrows = pg.transform.scale(widthSelectArrows, 
                                           (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    heightSelectArrows = pg.image.load('images/selected-height.png')
    heightSelectArrows = pg.transform.scale(heightSelectArrows, 
                                            (SCREEN_WIDTH, SCREEN_HEIGHT))

    confirmSelectArrows = pg.image.load('images/selected-confirm.png')
    confirmSelectArrows = pg.transform.scale(confirmSelectArrows,
                                             (SCREEN_WIDTH, SCREEN_HEIGHT))

    x = int((SCREEN_WIDTH * 0.45))
    y = int((SCREEN_HEIGHT * 0.9))

    # Change in x coord when moving horizontal
    xChange = ceil(SCREEN_WIDTH * 0.0075)
    # Change in y coord when moving vertical
    yChange = ceil(SCREEN_HEIGHT * 0.0075)

    playerShip = Ship(shipImage, x, y)

    gameFont = pg.font.Font('PixelFont.ttf', int(SCREEN_HEIGHT * 0.053))

    mainGameLoop(x,y)
    ## End of game sprites
