import pygame, sys
import time
from collections import deque

SCREEN = (600,800)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
END_COLOR = (255,0,0)
START_COLOR = (28,170,156)
SPEED = 0.05

def initBoard():
    return [[0 for _x in range(20)] for _y in range(20)]

def drawLines():
    global screen

    for i in range(0,600+1,30):
        pygame.draw.line(screen, BLACK, (i, 0), (i, 600), 2)
        pygame.draw.line(screen, BLACK, (0, i), (600, i), 2)
def drawBlock(pos_X0Y1, type):
    global screen

    color_type = type
    pygame.draw.rect(screen, color_type, pygame.Rect((pos_X0Y1[0]*30+2,pos_X0Y1[1]*30+2),(28,28)))


def checkBlock(pos_X0Y1):
    if Board[pos_X0Y1[1]][pos_X0Y1[0]] != 0: return True
    else: return False

Points = []
def checkPoints():
    if len(Points): return True
    else: return False
def setBlock(pos_X0Y1, val):
    Board[pos_X0Y1[1]][pos_X0Y1[0]] = val


def validPosOnBoard(pos):
    if pos[0] < 20 and pos[1] < 20: return True
def validSearchPos(pos, arr):
    x, y = pos[0], pos[1]
    if (-1 < y and y < len(arr)) and (-1 < x and x < len(arr)):
         if arr[y][x] != 1: return True
    else: return False


def bfsSearch(points, arr):
    q = deque()
    start, end = points


    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    q.append(start)
    visited = [start]

    current_pos = q.popleft()
    poss = []
    x, y = current_pos[0], current_pos[1]
    for move in movements:
        poss.append((x + move[0], y + move[1]))

    for pos in poss:
        if validSearchPos(pos, arr) and (pos not in visited):
            q.append(pos)
            visited.append(pos)

    drawBlock(start, GREEN)
    pygame.display.update()
    time.sleep(0.1)
    drawBlock(current_pos, START_COLOR)
    pygame.display.update()


    while q:

        current_pos = q.popleft()
        drawBlock(current_pos, YELLOW)
        time.sleep(SPEED)
        pygame.display.update()

        if current_pos == end:
            drawBlock(end, GREEN)
            pygame.display.update()
            time.sleep(0.1)
            drawBlock(end, END_COLOR)
            pygame.display.update()
            break
        else:
            poss = []
            x , y = current_pos[0] , current_pos[1]
            for move in movements:
                poss.append((x + move[0], y + move[1]))

            for pos in poss:
                if validSearchPos(pos,arr) and (pos not in visited):
                    q.append(pos)
                    visited.append(pos)





def runPygame():
    global screen

    Setting = True
    SavePath = False
    temp_path = []
    mouseBefore=(0,0)

    while Setting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Setting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseBefore = event.pos
                pos = ( int(mouseBefore[0] // 30), int(mouseBefore[1] // 30) )

                if event.button == 1 and validPosOnBoard(pos):
                    if not checkBlock(pos):
                        drawBlock(pos, BLACK)
                        setBlock(pos, 1)
                    else:
                        drawBlock(pos, WHITE)
                        setBlock(pos, 0)

                elif event.button == 3 and validPosOnBoard(pos):
                    if not checkBlock(pos) and len(Points) < 2:
                        if checkPoints():
                            drawBlock(pos, END_COLOR)
                            setBlock(pos, -1)
                            Points.append(pos)
                        else:
                            drawBlock(pos, START_COLOR)
                            setBlock(pos, -1)
                            Points.append(pos)
                    else:
                        if pos in Points:
                            drawBlock(pos, WHITE)
                            setBlock(pos, 0)
                            Points.pop(-1)

                else: pass

            if event.type == pygame.MOUSEMOTION and event.pos != mouseBefore:
                pos = (int(event.pos[0] // 30), int(event.pos[1] // 30))

                if event.buttons == (1,0,0) and validPosOnBoard(pos):
                    SavePath = True
                    temp_path.append(pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if(SavePath):
                    temp_first = temp_path[0]
                    temp_path = set(temp_path)

                    for pos in temp_path:
                        if pos in Points:
                            continue
                        if not checkBlock(pos):
                            drawBlock(pos, BLACK)
                            setBlock(pos, 1)
                        else:
                            drawBlock(pos, WHITE)
                            setBlock(pos, 0)

                    if not checkBlock(temp_first):
                        drawBlock(temp_first, BLACK)
                        setBlock(temp_first, 1)
                    else:
                        drawBlock(temp_first, WHITE)
                        setBlock(temp_first, 0)

                    SavePath = False
                    temp_path = []

        pygame.display.update()

    bfsSearch(Points,Board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


def initPygame():
    global screen
    global Board

    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    pygame.display.set_caption('PathFinder')
    screen.fill(WHITE)
    drawLines()
    Board = initBoard()


initPygame()
runPygame()