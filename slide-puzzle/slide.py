import pygame, sys, random
from pygame.locals import *

#create constants
BOARDWIDTH = 4
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 640

WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                 R    G    B

BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message: 
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)

        DISPLAYSURF.blit(textSurf, textRect)
    
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])
    
    left, top = getLeftTopOfTile(0,0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
    
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): #get all QUIT event
        terminate() #terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): #get all KEYUP events
        if event.key == K_ESCAPE:
            terminate() #terminate if the KEYUP was for the Esc key
        pygame.event.post(event) #put the other KEYUP even objects back   

def getStartingBoard():
    #return a board data structure with tiles in the solved state
    #for example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    #returns[[1,4,7], [2,5,8], [3,6,None]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH): 
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter +=  BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTh - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = None
    return board

def generateNewPuzzle(numSlides):
    #from a starting configuration, make numSlides number of moves (and animate moves)
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) #pause 500 ms for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)

def getBlankPosition(board):
    #return the x and y of board coords of the blank space
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == None:
                return (x,y)

def makeMoveBoard(board, move):
    #this function does not check if the move is valid
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
    board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blank != len(board[0] - 1) or \
        (move == DOWN and blanky !=0) or \
        (move == LEFT and blankx != len(board) - 1) or \
        (move == RIGHT and blankx != 0))

def getRandomMove(board, lastMove=None):
    #start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    #remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    #return a random move from the list or remaining moves
    return rand.choice(validMoves)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    # from the x & y pixel coords, get the x & y board coords
    for tileX in range(len(board)):
        left, top = getLeftTopOfTile(tileX, tileY)
        tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
        if tileRect.collidepoint(x, y):
            return(tileX, tileY)
    return(None, None)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    #draw a tile at board coords tilex and tiley, optionally a few
    #pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = text.Surf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + in(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
    #create the Surface and Rect objects for some text
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def 