import pygame, sys
import time
from collections import deque
import queue


SCREEN = (600,800)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
END_COLOR = (255,0,0)
START_COLOR = (28,170,156)
SPEED = 0.02




def initBoard():
    return [[0 for _x in range(20)] for _y in range(20)]
def drawLines():
    global screen

    for i in range(0,600+1,30):
        pygame.draw.line(screen, BLACK, (i, 0), (i, 600), 2)
        pygame.draw.line(screen, BLACK, (0, i), (600, i), 2)
def dispMessage(text, XY,size=20,color=BLACK):
    global screen

    textfont = pygame.font.Font('freesansbold.ttf', size)
    text = textfont.render(text, True, color)
    textpos = text.get_rect()
    textpos.center = XY
    screen.blit(text, textpos)
    pygame.display.update()
def drawBlock(pos_X0Y1, type):
    global screen

    color_type = type
    pygame.draw.rect(screen, color_type, pygame.Rect((pos_X0Y1[0]*30+2,pos_X0Y1[1]*30+2),(28,28)))
def drawMsgBlock(X,Y):
    global screen

    pygame.draw.rect(screen, WHITE, pygame.Rect((X,Y),(90,30)))
    pygame.display.update()

def initState():
    global Board
    global Points

    Points = []
    Board = initBoard()
    pygame.draw.rect(screen, WHITE, pygame.Rect((0,0), (600, 600)))
    drawLines()
    pygame.display.update()

def initSearch(arr):
    for x in range(20):
        for y in range(20):
            if arr[y][x] == 0:
                drawBlock((x,y),WHITE)
    pygame.display.update()

def checkBlock(pos_X0Y1):
    if Board[pos_X0Y1[1]][pos_X0Y1[0]] != 0: return True
    else: return False
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

'''def dfsSearch(points, arr):
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
            q.appendleft(pos)
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
            temp = []
            x , y = current_pos[0] , current_pos[1]
            for move in movements:
                poss.append((x + move[0], y + move[1]))

            for pos in poss:
                if validSearchPos(pos,arr) and (pos not in visited):
                    q.appendleft(pos)
                    visited.append(pos)'''
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

def astarSearch(points, arr):

    q = queue.PriorityQueue()
    start, end = points
    depth = 0

    def h(pos): return (pos[0] - end[0])**2 + (pos[1] - end[1])**2
    def g(): return depth
    def f(pos): return h(pos) + g()

    class ListNode:
        def __init__(self, pos, depth=0):
            self.pos = pos
            self.next = []
            self.depth = depth
            self.val = f(self.pos)
        def __lt__(self,other):
            return self.val < other.val


    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    q.put(ListNode(start))
    visited = [start]

    current_node = q.get()
    depth = current_node.depth + 1
    poss = []
    x, y = current_node.pos
    for move in movements:
        poss.append((x + move[0], y + move[1]))

    for pos in poss:
        if validSearchPos(pos, arr) and (pos not in visited):
            q.put(ListNode(pos, depth))


    while not q.empty():
        current_node = q.get()
        drawBlock(current_node.pos, YELLOW)
        time.sleep(SPEED)
        pygame.display.update()

        if current_node.pos == end:
            drawBlock(end, GREEN)
            pygame.display.update()
            time.sleep(0.1)
            drawBlock(end, END_COLOR)
            pygame.display.update()
            break

        depth = current_node.depth + 1
        poss = []
        x, y = current_node.pos
        for move in movements:
            poss.append((x + move[0], y + move[1]))

        for pos in poss:
            if validSearchPos(pos, arr) and (pos not in visited):
                q.put(ListNode(pos,depth))

        visited.append(current_node.pos)

def printDiscriptions():
    dispMessage('1. PRESS "A" or "B"', (443, 705), 15)
    dispMessage('2. RIGHT CLICK : SET POINTS', (480, 725), 15)
    dispMessage('3. SPACE : SEARCH', (443, 745), 15)
    dispMessage('4. SHIFT : CLEAN PATH', (456, 765), 15)
    dispMessage('ESC : RESET BOARD', (432, 785), 12)
    drawMsgBlock(20, 635)
    drawMsgBlock(80, 635)
    drawMsgBlock(140, 635)
def runPygame():
    global screen
    global Points
    global Board

    SavePath = False
    temp_path = []
    mouseBefore=(0,0)
    SearchType = None
    Setting = True

    printDiscriptions()
    dispMessage('SearchType : ', (80, 700))
    dispMessage(f'{SearchType}',(170,700))
    while True:

        while Setting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if len(Points)==2 and SearchType != None:
                            Setting = False
                        else:
                            if len(Points) != 2:
                                dispMessage('2. RIGHT CLICK : SET POINTS', (480, 725), 15,color=END_COLOR)
                            if len(Points) == 2:
                                dispMessage('2. RIGHT CLICK : SET POINTS', (480, 725), 15)
                            if SearchType == None:
                                drawMsgBlock(142, 685)
                                dispMessage(f'{SearchType}', (169, 700),color=END_COLOR)
                    if event.key == pygame.K_a:
                        drawMsgBlock(141,685)
                        SearchType = 'A-star'
                        dispMessage(f'{SearchType}',(169,700))
                    if event.key == pygame.K_b:
                        drawMsgBlock(141,685)
                        SearchType = 'BFS'
                        dispMessage(f'{SearchType}',(159,700))
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        initSearch(Board)
                    if event.key == pygame.K_ESCAPE:
                        initState()

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
                                for idx,point in enumerate(Points):
                                    if len(Points)==2 and point == pos and idx == 0:
                                        drawBlock(Points[1], START_COLOR)
                                        Points.pop(0)
                                    elif len(Points)==2 and point == pos and idx == 1:
                                        Points.pop(1)
                                    else:
                                        Points.pop()
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
                            pygame.display.update()
                        if not checkBlock(temp_first):
                            drawBlock(temp_first, BLACK)
                            setBlock(temp_first, 1)
                        else:
                            drawBlock(temp_first, WHITE)
                            setBlock(temp_first, 0)

                        SavePath = False
                        temp_path = []

            pygame.display.update()


        pygame.draw.rect(screen, WHITE, pygame.Rect((0, 610), (600, 190)))
        dispMessage(f'SearchType : {SearchType}', (120, 700))
        printDiscriptions()
        dispMessage('SEARCHING', (121,650),30)

        if SearchType == 'A-star':
            astarSearch(Points,Board)
        elif SearchType == 'BFS':
            bfsSearch(Points, Board)
        else:
            pass


        Setting = True

        pygame.draw.rect(screen, WHITE, pygame.Rect((0, 610), (600, 190)))
        printDiscriptions()
        dispMessage('SearchType : ', (80, 700))
        dispMessage(f'{SearchType}', (170, 700))



def initPygame():
    global screen
    global Board
    global Points

    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    pygame.display.set_caption('PathFinder')
    screen.fill(WHITE)
    drawLines()
    Board = initBoard()
    Points = []


initPygame()
runPygame()