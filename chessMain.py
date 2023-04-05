""" responsible for user input an show the state of the game """



import pygame as p 
import chessEngine


p.init()
WIDTH = HEIGHT = 800
DIMENSION = 8 #8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #animations 
IMAGES = {}


def loadimages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ' ]
    for piece in pieces:
        IMAGES [piece] = p.transform.scale((p.image.load("image/" + piece + ".png")), (SQ_SIZE, SQ_SIZE))

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    # call for game state
    gs = chessEngine.GameState()
    loadimages()
    run = True
    while run:
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()#(x,y)
                cool = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"),p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE ))

def drawPieces(screen , board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty
                screen.blit(IMAGES [piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE ))

if __name__ == "__main__":
    main()