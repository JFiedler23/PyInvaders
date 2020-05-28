import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

#Main menu
def MainMenu(screen):
    startButton = pygame.Rect(190, 200, 256, 64)
    font = pygame.font.Font("SPACEBAR.ttf", 32)
    clock.tick(60)

    while True:
        mx, my = pygame.mouse.get_pos()
        titleText = font.render("INVADERS", 1, (255,255,255))

        click = False
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
                        print("start game")

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (69, 180, 186), startButton, 0)
        screen.blit(titleText, (210, 20))
        pygame.display.update()
