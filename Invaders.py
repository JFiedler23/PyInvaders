import pygame
import sys
import random
from player import *
from laser import *
from alien import *

pygame.init()

#<----------PYGAME SPECIFIC OBJECTS---------->

#basic screen setup
screenSize = screenWidth, screenHeight = 640, 480
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Invaders!")

#creating font
gameFont = pygame.font.Font('Atari.ttf', 28)

#framerate clock
clock = pygame.time.Clock()

#<----------Main Menu---------->
def MainMenu():
    startButton = pygame.Rect(190, 200, 256, 64)
    font = pygame.font.Font("SPACEBAR.ttf", 32)
    clock.tick(60)

    while True:
        mx, my = pygame.mouse.get_pos()
        titleText = font.render("INVADERS", 1, (255,255,255))
        buttonText= font.render("Start", 1, (0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if startButton.collidepoint((mx, my)):
                        game()

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (69, 180, 186), startButton, 0)
        screen.blit(titleText, (210, 20))
        screen.blit(buttonText, (250, 210))
        pygame.display.update()

#<----------GAME OVER SCREEN---------->
def GameOver():
    font = pygame.font.Font("SPACEBAR.ttf", 32)

    while True:
        clock.tick(60)

        gameOverText = font.render("GAME OVER", 1, (255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((0,0,0))
        screen.blit(gameOverText, (210, 20))
        pygame.display.update()

#<----------GAME---------->
def game():
    #loading player image
    ssImage = pygame.image.load("Images/spaceship.png")
    pygame.display.set_icon(ssImage)
    ssImage = ssImage.convert()

    #loading laser image
    laserImg = pygame.image.load("Images/laser_bullet.png")
    laserImg = laserImg.convert()

    #loading alien Image
    alienImg = pygame.image.load("Images/alien_ship.png")
    alienImg = alienImg.convert()

    #creating player shoot event
    RELOAD_SPEED = 350
    RELOADED_EVENT = pygame.USEREVENT + 1
    reloaded = True
    pygame.time.set_timer(RELOADED_EVENT, RELOAD_SPEED)

    #creating alien movement event
    move_speed = 850
    ALIEN_MOVE_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(ALIEN_MOVE_EVENT, move_speed)

    #creating alien shoot event
    ALIEN_SHOOT_SPEED = 900
    ALIEN_SHOOT_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(ALIEN_SHOOT_EVENT, ALIEN_SHOOT_SPEED)

    #<----------INITIALIZING GAME OBJECTS---------->

    #initializing Player
    mainPlayer = Player(64, 64, (screenWidth // 2), (screenHeight - 64))

    #alien initialization variables
    aliens = []
    aliensInRow = (screenWidth // 64) - 2
    numRows = 4

    #initializing all aliens
    for i in range(aliensInRow):
        for j in range(numRows):
            aliens.append(Alien(64, 64, (70 * i+1), (64 * j)+40))


    #<----------GAMEPLAY FUNCTIONS---------->
    #image draw
    def redrawGameWindow():
        screen.fill((0,0,0))

        scoreText = gameFont.render("Score: "+ str(score), 1, (255,255,255))
        screen.blit(scoreText, (480, 10))

        mainPlayer.draw(screen, ssImage)

        for alien in aliens:
            alien.draw(screen, alienImg)

        for laser in playerLasers:
            laser.draw(screen, laserImg)

        for laser in alienLasers:
            laser.draw(screen, laserImg)

        pygame.display.update()

    def playerDestory():
        #checking for alien-player collision
        for alien in aliens:
            if (mainPlayer.hitbox[1] < alien.hitbox[1] + alien.hitbox[3]) and (mainPlayer.hitbox[1] + mainPlayer.hitbox[3] > alien.hitbox[1]):
                if (mainPlayer.hitbox[0] < alien.hitbox[0] + alien.hitbox[2]) and (mainPlayer.hitbox[0] + mainPlayer.hitbox[2] > alien.hitbox[0]):
                    return True

    #<----------GAMEPLAY VARIABLES---------->
    run = True
    movingRight = True #alien movement direction
    score = 0
    playerLasers = []
    alienLasers = []
    numAliens = len(aliens)

    #<----------GAME LOOP---------->
    while run:
        largestX = 0
        smallestX = 1000
        clock.tick(60)

        #Getting all key presses
        keys = pygame.key.get_pressed()

        #Checking for custom events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #player reload event
            if event.type == RELOADED_EVENT:
                mainPlayer.shoot(keys, playerLasers)

            #Alien movement
            if event.type == ALIEN_MOVE_EVENT:
                #Keeping track of smallest and largest x values
                for alien in aliens:
                    if alien.x > largestX:
                        largestX = alien.x

                    if alien.x < smallestX:
                        smallestX = alien.x

                #Checking boundaries
                for alien in aliens:
                    #moving right
                    if largestX < (screenWidth - alien.width - alien.moveDistance) and movingRight:
                        alien.x += alien.moveDistance
                    #Moving down when right edge of screen is reached
                    elif largestX+5 == (screenWidth - alien.width - alien.moveDistance):
                        alien.y += alien.moveDistance
                    else:
                        movingRight = False

                    #moving left
                    if smallestX >= alien.moveDistance and not movingRight:
                        alien.x -= alien.moveDistance
                    else:
                        movingRight = True

            #Alien shooting
            if event.type == ALIEN_SHOOT_EVENT:
                if len(aliens) > 0:
                    choice = random.randint(0, len(aliens)-1)
                    aliens[choice].shoot(alienLasers)

        if playerDestory():
            run = False
            GameOver()

        #Player laser manager
        for laser in playerLasers:
            #Checking if an alien has been hit
            for alien in aliens:
                if (laser.hitbox[1]) < (alien.hitbox[1] + alien.hitbox[3]) and (laser.hitbox[1] + laser.hitbox[3]) > alien.hitbox[1]:
                    if (laser.hitbox[0] - laser.hitbox[2]) < (alien.hitbox[0] + alien.hitbox[2]) and (laser.hitbox[0] + laser.hitbox[2]) > alien.hitbox[0]:
                        score += 100
                        aliens.pop(aliens.index(alien))

                        #just in case two aliens are hit at once
                        try:
                            playerLasers.pop(playerLasers.index(laser))
                        except ValueError:
                            continue

            if laser.y > 0 and laser.y < screenHeight:
                laser.y -= laser.velocity
            else:
                playerLasers.pop(playerLasers.index(laser))

        #Alien laser manager
        for laser in alienLasers:
            #checking if player has been hit
            if (laser.hitbox[1] < mainPlayer.hitbox[1] + mainPlayer.hitbox[3]) and (laser.hitbox[1] + laser.hitbox[3] > mainPlayer.hitbox[1]):
                if (laser.hitbox[0] - laser.hitbox[2] < mainPlayer.hitbox[0] + mainPlayer.hitbox[2]) and (laser.hitbox[0] + laser.hitbox[2] > mainPlayer.hitbox[0]):
                    run = False
                    GameOver()

            if laser.y < screenHeight and laser.y > 0:
                laser.y += laser.velocity
            else:
                alienLasers.pop(alienLasers.index(laser))

        #player controller
        mainPlayer.controller(screenWidth, keys)

        redrawGameWindow()

MainMenu()
