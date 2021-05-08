# -*- coding: utf-8 -*-
# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
"""
Created on Sun May 26 16:36:27 2019

@author: Hannah_Noh, Soyoon_Lee, SoJeong_Lee, Seungwon_Jang
"""

import random, time, pygame, sys
from pygame.locals import *

# Setting global variables
FPS = 15
WINDOWWIDTH = 810
WINDOWHEIGHT = 640
BOXSIZE = 22
BOARDWIDTH = 13
BOARDHEIGHT = 23
BLANK = '.'
itemKEY = False
i_itemCount, o_itemCount, l_itemCount = 3, 3, 3
roundCount = 1
BGimage = 'BGimage_1.jpg'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5


#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = ( 20,  20, 175)
LIGHTBLUE   = (  0, 102, 255)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
PURPLE      = (128,   0, 255)
LIGHTPURPLE = (163, 140, 255)

BORDERCOLOR = PURPLE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = BLACK
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW,    GRAY,      PURPLE)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW,   BLACK, LIGHTPURPLE)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

# Set piece
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

A_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..O..',
                     '.....',
                     '.....']]

ITEM_SHAPE_TEMPLATE = [['.....',
                        '.....',
                        '.000.',
                        '.....',
                        '.....']]

PIECES_in = {'S': S_SHAPE_TEMPLATE,
             'Z': Z_SHAPE_TEMPLATE,
             'J': J_SHAPE_TEMPLATE,
             'L': L_SHAPE_TEMPLATE,
             'I': I_SHAPE_TEMPLATE,
             'O': O_SHAPE_TEMPLATE,
             'T': T_SHAPE_TEMPLATE,
             'A': A_SHAPE_TEMPLATE}

PIECES_out = {'S': S_SHAPE_TEMPLATE,
              'Z': Z_SHAPE_TEMPLATE,
              'J': J_SHAPE_TEMPLATE,
              'L': L_SHAPE_TEMPLATE,
              'I': I_SHAPE_TEMPLATE,
              'O': O_SHAPE_TEMPLATE,
              'T': T_SHAPE_TEMPLATE,
              'A': A_SHAPE_TEMPLATE,
              'ITEM' : ITEM_SHAPE_TEMPLATE}

# main game loop
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, roundLevel, i_itemCount, o_itemCount, l_itemCount, roundCount, BGimage
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('ISH')

    showTextScreen('ISH')
    showRuleScreen()
    while True: # game loop
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.play(-1, 0.0)
        run = runGame()
        pygame.mixer.music.stop()
        if run == 1: # next Round
            BGimage = random.choice(['BGimage_1.jpg', 'BGimage_2.jpg', 'BGimage_3.jpg', 'BGimage_4.jpg', 'BGimage_5.jpg'])
            i_itemCount, o_itemCount, l_itemCount = 3, 3, 3 # reset Item
            roundCount += 1
        else : # can't fit a new piece on the board, so game over
            showTextScreen('Game Over')
            terminate()
    
# runGame - event loop, drawing on the board
def runGame():
    # setup variables for the start of the game
    global itemKEY, i_itemCount, o_itemCount, l_itemCount
    board = getNewBoard()

    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if checkEnd(board) :
                return 1

            if not isValidPosition(board, fallingPiece):
                return 2

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_s):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_w):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_a):
                    movingDown = False

            elif event.type == KEYDOWN:
                # about item event
                if event.key == K_i and i_itemCount >0 :
                    # remove the box on the board
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    itemKEY = True
                    fallingPiece = {'shape': 'ITEM',
                                    'rotation': 0,
                                    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                                    'y': -2,
                                    'color': 4}
                    lastFallTime = time.time()
                 
                elif event.key == K_o and o_itemCount >0 :
                    # change the fallingPiece
                    o_itemCount -= 1
                    fallingPiece = nextPiece
                    nextPiece = getNewPiece()
                    lastFallTime = time.time()
                    
                elif event.key == K_l and l_itemCount >0:
                    # change the nextPiece
                    l_itemCount -= 1               
                    nextPiece = getNewPiece()
                    lastFallTime = time.time()
                    
                # moving the piece sideways
                elif (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()
                    
                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s) and isValidPosition(board, fallingPiece, adjY=1):
                    movingDown = True
                    fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES_out[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES_out[fallingPiece['shape']])
                        
                elif (event.key == K_q): # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES_out[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES_out[fallingPiece['shape']])

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                if itemKEY :
                    removeToBoard(board, fallingPiece)
                    fallingPiece['color'] = BLANK
                    i_itemCount -= 1
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
                itemKEY = False
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        pieceImageRect = pygame.Rect(0, 0, 10, 10)
        pieceImageSurf = pygame.image.load(BGimage)
        DISPLAYSURF.blit(pieceImageSurf, pieceImageRect)
        drawBoard(board)
        drawStatus(score, roundCount, i_itemCount, o_itemCount, l_itemCount)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getNewBoard():
    # create and return a new board data structure (include random box)
    board = []
    for i in range(BOARDWIDTH): # create a new blank board
        board.append([BLANK] * BOARDHEIGHT)
        
    if roundCount <= 10 :
        for x in range (0, 6, 1) :
            for y in range (0, roundCount, 1) :
                if random.randint(0, 1) == 1:
                    board[x][(BOARDHEIGHT-1)-y] = 5
                    
    elif roundCount <= 20 :
        for x in range (0, 8, 1) :
            for y in range (0, roundCount-10, 1) :
                if random.randint(0, 1) == 1:
                    board[x][(BOARDHEIGHT-1)-y] = 5
                    
    else :
        for x in range (0, BOARDWIDTH, 1) :
            for y in range (0, 10, 1) :
                if random.randint(0, 1) == 1:
                    board[x][(BOARDHEIGHT-1)-y] = 5
                    
    return board


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def checkEnd(board) :
    # This function checks that all random boxes have been cleared.
    for x in range (BOARDWIDTH) :
        for y in range (BOARDHEIGHT) :
            if board[x][y] == 5:
                return False # All random BOX are not removed
            elif board[x][y] == BLANK :
                continue # Blank, continue
            elif board[x][y] < 5 :
                continue # Other piece, continue
    return True # if ALL ramdom BOX are removed, return True

def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None
    
def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()
        
def showRuleScreen():
    # This function displays the game Rule
    DISPLAYSURF.fill(BGCOLOR)
    RuleBoldFONT = pygame.font.Font('NanumGothic.ttf', 60)
    RuleFONT = pygame.font.Font('NanumGothic.ttf', 30)
    itemFONT = pygame.font.Font('NanumGothic.ttf', 15)
    
    text1 = "게임 방법"
    text2 = "1. 보드에 나타나는 보라색 박스를 모두 지우면 next Round!"
    text3 = "2. 아이템은 각 Round마다 3번 사용 가능"
    text4 = "(I : 아이템 피스가 떨어지며 박스 삭제, O : 현재 떨어지는 피스 바꾸기, L : 다음 피스 바꾸기)"

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text1, RuleBoldFONT, WHITE)
    titleRect.center = (int(WINDOWWIDTH / 2), 50)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = makeTextObjs(text2, RuleFONT, WHITE)
    titleRect.center = (int(WINDOWWIDTH / 2), 120)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = makeTextObjs(text3, RuleFONT, WHITE)
    titleRect.center = (int(WINDOWWIDTH / 2), 160)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = makeTextObjs(text4, itemFONT, WHITE)
    titleRect.center = (int(WINDOWWIDTH / 2), 190)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the piece image
    pieceImageRect = pygame.Rect(50, 210, 10, 10)
    pieceImageSurf = pygame.image.load('piece.png')
    DISPLAYSURF.blit(pieceImageSurf, pieceImageRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, BLACK)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 250)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score
    # how many seconds pass until a falling piece falls one space.
    fallFreq = 0.27 - ((int(score / 10) + 1) * 0.02)
    return fallFreq


def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES_in.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES_in[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-3)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES_out[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']
        
        
def removeToBoard(board, piece):
    # remove item, remove the box form the board
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES_out[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']+1] = BLANK


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES_out[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True


def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 3, (BOARDWIDTH * BOXSIZE) + 6, (BOARDHEIGHT * BOXSIZE) + 6), 5)
    # fill the BLACK color of the board
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, roundCount, i_itemCount, o_itemCount, l_itemCount):
    # draw the border around the status board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (WINDOWWIDTH - 173, 7, 135, 305))
    # fill the BLACK color of the status board
    pygame.draw.rect(DISPLAYSURF, BLACK, (WINDOWWIDTH - 170, 10, 130, 300))
    
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
    # draw the round text
    roundSurf = BASICFONT.render('Round: %s' % roundCount, True, TEXTCOLOR)
    roundRect = roundSurf.get_rect()
    roundRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(roundSurf, roundRect)
    
    # draw the i_item text
    i_itemSurf = BASICFONT.render('I Item: %s' % i_itemCount, True, TEXTCOLOR)
    i_itemRect = i_itemSurf.get_rect()
    i_itemRect.topleft = (WINDOWWIDTH - 150, 80)
    DISPLAYSURF.blit(i_itemSurf, i_itemRect)
    
    # draw the o_item text
    o_itemSurf = BASICFONT.render('O Item: %s' % o_itemCount, True, TEXTCOLOR)
    o_itemRect = o_itemSurf.get_rect()
    o_itemRect.topleft = (WINDOWWIDTH - 150, 110)
    DISPLAYSURF.blit(o_itemSurf, o_itemRect)
    
    # draw the l_item text
    l_itemSurf = BASICFONT.render('L Item: %s' % l_itemCount, True, TEXTCOLOR)
    l_itemRect = l_itemSurf.get_rect()
    l_itemRect.topleft = (WINDOWWIDTH - 150, 140)
    DISPLAYSURF.blit(l_itemSurf, l_itemRect)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES_out[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 150, 170)
    DISPLAYSURF.blit(nextSurf, nextRect)
    
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-150, pixely=200)

# main
if __name__ == '__main__':
    main()
