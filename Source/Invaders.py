import pygame
import sys
import os
import random
from player import *
from laser import *
from alien import *

pygame.init()
my_path = os.path.abspath(os.path.dirname(__file__))

#<----------PYGAME SPECIFIC OBJECTS---------->

#basic screen setup
screenSize = screenWidth, screenHeight = 640, 480
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Invaders!")

#creating font
game_font_path = os.path.join(my_path, '../Fonts/Atari.ttf')
gameFont = pygame.font.Font(game_font_path, 28)

#framerate clock
clock = pygame.time.Clock()

#<----------Main Menu---------->
def MainMenu():
    icon_path = os.path.join(my_path, '../Images/icon.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    startButton = pygame.Rect(190, 200, 256, 64)

    title_font_path = os.path.join(my_path, "../Fonts/SPACEBAR.ttf")
    font = pygame.font.Font(title_font_path, 32)
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
    title_font_path = os.path.join(my_path, "../Fonts/SPACEBAR.ttf")
    font = pygame.font.Font(title_font_path, 32)

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
    spaceship_path = os.path.join(my_path, "../Images/spaceship.png")
    ssImage = pygame.image.load(spaceship_path)
    ssImage = ssImage.convert()

    #loading laser image
    laser_path = os.path.join(my_path, "../Images/laser_bullet.png")
    laserImg = pygame.image.load(laser_path)
    laserImg = laserImg.convert()

    #loading alien Image
    alien_path = os.path.join(my_path, "../Images/alien_ship.png")
    alienImg = pygame.image.load(alien_path)
    alienImg = alienImg.convert()

    explosionImg = [pygame.image.load(os.path.join(my_path, "../Images/explosion_1.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_2.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_3.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_4.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_5.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_6.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_7.png"))]

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

    #explosion event
    EXPLOSION_SPEED = 200
    EXPLOSION_EVENT = pygame.USEREVENT + 4
    pygame.time.set_timer(EXPLOSION_EVENT, EXPLOSION_SPEED)

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
        scoreText = gameFont.render("Score: "+ str(score), 1, (255,255,255))
        screen.blit(scoreText, (480, 10))

        mainPlayer.draw(screen, ssImage)

        for alien in aliens:
            alien.draw(screen, alienImg)

        for laser in playerLasers:
            laser.draw(screen, laserImg)

        for laser in alienLasers:
            laser.draw(screen, laserImg)

            
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
    animCount = 0
    explosion = False
    playerLasers = []
    alienLasers = []
    numAliens = len(aliens)

    #<----------GAME LOOP---------->
    while run:
        screen.fill((0,0,0))

        largestX = 0
        smallestX = 1000
        clock.tick(56)

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
                        tempX, tempY = alien.x, alien.y
                        aliens.pop(aliens.index(alien))

                        explosion = True
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

        #explosion animation
        if animCount + 1 >= 56:
            animCount = 0
            explosion = False

        if explosion:
            screen.blit(explosionImg[animCount//8], (tempX, tempY))
            animCount += 1

        redrawGameWindow()

        pygame.display.update()

MainMenu()
