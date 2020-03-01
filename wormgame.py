import time
import pygame
import random
import math
pygame.init()
MYFONT = pygame.font.SysFont('Lucida Console', 60)
SMALLFONT = pygame.font.SysFont('Lucida Console', 30)
WINDOW_WIDTH = 500
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH + 50))
pygame.display.set_caption("Worm Game")

SQUARES_WIDE = 40
LINE_WIDTH = 1
GRID_SQUARE_SIZE = ((WINDOW_WIDTH - LINE_WIDTH)/ SQUARES_WIDE) - LINE_WIDTH

def MainMenu():
    def Refresh():
        WIN.fill((20, 20, 20))
        t_surface = MYFONT.render("Worm Game", False, (255, 255, 255))
        WIN.blit(t_surface, (90, 10))
    def ShowMenu():
        
        pygame.draw.rect(WIN, (0, 0, 0), (145, 205, 230, 40))
        t_surface = SMALLFONT.render("Apple Lovers", False, (255, 255, 255))
        WIN.blit(t_surface, (150, 210))

        pygame.draw.rect(WIN, (0, 0, 0), (195, 125, 120, 40))
        t_surface = SMALLFONT.render("Normal", False, (255, 255, 255))
        WIN.blit(t_surface, (200, 130))

        pygame.draw.rect(WIN, (0, 0, 0), (205, 285, 95, 40))
        t_surface = SMALLFONT.render("Quit", False, (255, 255, 255))
        WIN.blit(t_surface, (210, 290))

    def SelectAppleMode():
        Refresh()
        pygame.draw.rect(WIN, (255, 255, 255), (140, 200, 240, 50))
        ShowMenu()
    def SelectNormal():
        Refresh()
        pygame.draw.rect(WIN, (255, 255, 255), (190, 120, 130, 50))
        ShowMenu()
    def SelectQuit():
        Refresh()
        pygame.draw.rect(WIN, (255, 255, 255), (200, 280, 105, 50))
        ShowMenu()
    
    SelectNormal()
    selected = 0
    
    startgame = False
    appleMode = False
    while not(startgame):
        holddownkey = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                holddownkey = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if selected == 0:
                startgame = True
                appleMode = False
            elif selected == 1:
                startgame = True
                appleMode = True
            elif selected == 2:
                pygame.quit()
        elif keys[pygame.K_UP] and holddownkey:
            if selected == 1:
                SelectNormal()
                selected = 0
            elif selected == 2:
                SelectAppleMode()
                selected = 1
        elif keys[pygame.K_DOWN] and holddownkey:
            if selected == 0:
                SelectAppleMode()
                selected = 1
            elif selected == 1:
                SelectQuit()
                selected = 2
        pygame.display.update()
    return appleMode
def DrawGrid():
    WIN.fill((20, 20, 20))
    for x in range (SQUARES_WIDE):
        for y in range (SQUARES_WIDE):
            pygame.draw.rect(WIN, (0, 0, 0), (int(x * ((WINDOW_WIDTH - LINE_WIDTH) / SQUARES_WIDE) + LINE_WIDTH), int(y * ((WINDOW_WIDTH - LINE_WIDTH)/ SQUARES_WIDE) + LINE_WIDTH) + 50, GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
def NewApple(WORM_BODY, APPLE_POS):
    x = WORM_BODY[0][0]
    y = WORM_BODY[0][1]
    i = 0
    while [x, y] in WORM_BODY or [x, y] in APPLE_POS:
        x = random.randrange(0, SQUARES_WIDE)
        y = random.randrange(0, SQUARES_WIDE)
        i += 100
        if i > 100:
            return None
    world_pos = CoordsToWorld([x, y])
    pygame.draw.rect(WIN, (0, 255, 0), (world_pos[0], world_pos[1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
    return([x, y])
def CoordsToWorld(COORDS):
    return [int(COORDS[0] * ((WINDOW_WIDTH - LINE_WIDTH) / SQUARES_WIDE) + LINE_WIDTH), int(COORDS[1] * ((WINDOW_WIDTH - LINE_WIDTH) / SQUARES_WIDE) + LINE_WIDTH + 50)]

def WorldToCoords(WORLD):
    return [int(WINDOW_WIDTH/WORLD[0]), int(WINDOW_WIDTH/WORLD[1])]

def RefreshScoreBar(SCORE):
    pygame.draw.rect(WIN, (0, 0, 0), (250, 0, 250, 50 - LINE_WIDTH))
    return MYFONT.render("Score: " + str(SCORE), False, (255, 255, 255))
def UpdateEnergyBar(ENERGY):
    if ENERGY <= 0:
        pygame.draw.rect(WIN, (255, 0, 0), (405, 5, 90, 40))
        pygame.draw.rect(WIN, (0, 0, 0), (410, 10, 80, 30))
    else:
        pygame.draw.rect(WIN, (255, 255, 255), (405, 5, 90, 40))
        pygame.draw.rect(WIN, (0, 0, 0), (410, 10, 80, 30))
        pygame.draw.rect(WIN, (255, 255, 0), (410, 10, ENERGY, 30))
def GAME():
    if SQUARES_WIDE % 2 == 0:
        X = int(SQUARES_WIDE / 2)
        Y = int(SQUARES_WIDE / 2)
    else:
        X = int(SQUARES_WIDE / 2 + .5)
        Y = int(SQUARES_WIDE / 2 + .5)
    WORM_BODY = [[X, Y], [X - 1, Y], [X - 2, Y]]
    WORM_BODY_UNDERGROUND = [False, False, False]
    SPEED = 2
    SCORE = 0
    ENERGY = 80
    DIR = 2
    APPLEMODE = MainMenu()
    DrawGrid()
    pygame.draw.rect(WIN, (0, 0, 0), (0, 0, WINDOW_WIDTH/2, 50 - LINE_WIDTH))
    TEXT_SURFACE = RefreshScoreBar(SCORE)
    APPLE_POS = []
    APPLE_POS.append(NewApple(WORM_BODY, APPLE_POS))
    DIGGING = False
    HIDEDIGGING = False
    RUN = True
    while RUN:
        pygame.time.delay(int(200 / SPEED))
        WIN.blit(TEXT_SURFACE, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        KEYS = pygame.key.get_pressed()
        DIGGING = KEYS[pygame.K_LSHIFT] and ENERGY > 0
        ENDOFWORM = [WORM_BODY[len(WORM_BODY) - 1][0], WORM_BODY[len(WORM_BODY) - 1][1]]
        if not (ENDOFWORM in APPLE_POS):
            if [ENDOFWORM[0], ENDOFWORM[1]] in WORM_BODY[0:len(WORM_BODY)-1]:
                WORLDPOS = CoordsToWorld(ENDOFWORM)
                if WORM_BODY_UNDERGROUND[WORM_BODY.index(ENDOFWORM)]:
                    pygame.draw.rect(WIN, (50, 0, 0), (WORLDPOS[0], WORLDPOS[1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
                else:
                    pygame.draw.rect(WIN, (255, 0, 0), (WORLDPOS[0], WORLDPOS[1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
            else:
                WORLDPOS = CoordsToWorld(ENDOFWORM)
                pygame.draw.rect(WIN, (0, 0, 0), (WORLDPOS[0], WORLDPOS[1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
        
        if (KEYS[pygame.K_LEFT] or KEYS[pygame.K_a]) and DIR != 2:
            DIR = 4
        if (KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]) and DIR != 4:
            DIR = 2
        if (KEYS[pygame.K_UP] or KEYS[pygame.K_w]) and DIR != 3:
            DIR = 1
        if (KEYS[pygame.K_DOWN] or KEYS[pygame.K_s]) and DIR != 1:
            DIR = 3
        if DIR == 2:
            X += 1
        elif DIR == 3:
            Y += 1
        elif DIR == 1:
            Y -= 1
        else:
            X -= 1

        if X > SQUARES_WIDE - 1:
            X -= SQUARES_WIDE
        if Y > SQUARES_WIDE - 1:
            Y -= SQUARES_WIDE
        if Y < 0:
            Y += SQUARES_WIDE
        if X < 0:
            X += SQUARES_WIDE

        if DIGGING:
            WORM_BODY.pop(len(WORM_BODY)-1)
            WORM_BODY_UNDERGROUND.pop(len(WORM_BODY_UNDERGROUND)-1)
        else:
            if [X, Y] in APPLE_POS:
                SCORE += 1
                if SPEED < 5:
                    SPEED += 0.05
                ENERGY += 10
                if ENERGY > 80:
                    ENERGY = 80
                TEXT_SURFACE = RefreshScoreBar(SCORE)
                APPLE_POS.remove([X, Y])
                if APPLEMODE:
                    for i in range(SCORE):
                        APPLE_POS.append(NewApple(WORM_BODY, APPLE_POS))
                else:
                    APPLE_POS.append(NewApple(WORM_BODY, APPLE_POS))
            elif [X, Y] in WORM_BODY:
                if not WORM_BODY_UNDERGROUND[WORM_BODY.index([X, Y])]:
                    RUN = False
            else:
                WORM_BODY.pop(len(WORM_BODY)-1)
                WORM_BODY_UNDERGROUND.pop(len(WORM_BODY_UNDERGROUND)-1)
        if DIGGING:
            if ENERGY < 0:
                DIGGING = False
                ENERGY = 0
            else:
                ENERGY -= 5
        if ENERGY > 80:
            ENERGY = 80
        UpdateEnergyBar(ENERGY)
        HIDEDIGGING = False
        if DIGGING and ([X, Y] in APPLE_POS or [X, Y] in WORM_BODY):
            HIDEDIGGING = True
        WORM_BODY.insert(0, [X, Y])
        WORM_BODY_UNDERGROUND.insert(0, DIGGING)
        WORLDPOS = CoordsToWorld([X, Y])
        if DIGGING:
            if not HIDEDIGGING:
                pygame.draw.rect(WIN, (50, 0, 0), (WORLDPOS[0], WORLDPOS[1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
        else:
            pygame.draw.rect(WIN, (255, 0, 0), (WORLDPOS[0], WORLDPOS[1], GRID_SQUARE_SIZE, GRID_SQUARE_SIZE))
        pygame.display.update()
    TEXT_SURFACE = MYFONT.render("You Died!", False, (255, 255, 255))
    WIN.blit(TEXT_SURFACE, (0, (WINDOW_WIDTH + 50) / 2))
    pygame.display.update()
    time.sleep(2)
    GAME()
GAME()