import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)

YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def splitIntoGroups(groupSize, theList):
    #splits a list into a list of lists, where the inner list have at 
    #most groupSize number of items
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    #convert baord coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x,y):
                return(boxx, boxy)
            return (None, None) 


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # get a list of every possible shape in every possible color
    icons = []
    for color in ALLCOLORS:
        for shapes in ALLSHAPES:
            icons.append((shape, color))

    random.shuffle(icons) #randomize icons
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT /2) #calc how many icons are needed
    icons = icons[:numIconsUsed] *2 #make two of each
    random.shuffle(icons)

    # create the board data structure, with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del.icons[0] # removes icons are they are assigned
        board.append(column)
    return board

def drawBoxCovers(board, boxes, coverage):
    # draw boxes being covered/revealed. 'boxes' is a list
    # of two-items, which have the x & y spot of the box
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: #only draw the cover if there is coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
          

def revealBoxesAnimation(board, boxesToReveal):
    # reveal box animation
    for coverage in range(BOXSIZE, (-REVEALSPEED) -1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    # cover box animation
    for coverage in range(0, BOXSIZE, +REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawHighlightBox(boxx, boxy:)
left, top = leftTopCoordsOfBox(boxx, boxy)
pygame.draw.rect(DISPLAYSUR,F HIGHLIGHTCOLOR, (left -5 , top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def startGameAnimation(board):
    #randomly reveal the boxes 8 at a time
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
        random.shuffle(boxes)
        boxGroups = splitIntoGroups(8, boxes)
    
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coveredBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    # flash the background color when player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    #returns true if all boxes have been revealed, otherwise returns false
    for i in revealedBoxes:
        if False in i:
            return False #returns false if any boxes are covered
        return True

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 #stores x coordinate of mouse event
    mousey = 0 # y event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of first box clicked

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)


if __name__ = '__main__':
    main()

