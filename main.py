from lib.classes import *
from lib.engine import *
import lib.globals as g
import pygame 

pygame.init()
screenSize = 800
screen = pygame.display.set_mode((screenSize, screenSize))
clock = pygame.time.Clock()
pygame.display.set_caption('chess')

initialBoard  = [ ["r_w","p_w","","","","","p_b","r_b"],
                  ["n_w","p_w","","","","","p_b","n_b"],
                  ["b_w","p_w","","","","","p_b","b_b"],
                  ["q_w","p_w","","","","","p_b","q_b"],
                  ["k_w","p_w","","","","","p_b","k_b"],
                  ["b_w","p_w","","","","","p_b","b_b"],
                  ["n_w","p_w","","","","","p_b","n_b"],
                  ["r_w","p_w","","","","","p_b","r_b"],
                   None, set()] # enPassant, brokenCastles  

Board = BoardClass(screen, initialBoard)
Board.LoadImages()
pieces = Board.updatePieces()
player = 'white'
click = None
gameover = False

while True:
    pygame.display.update()
    clock.tick(60)
    Board.drawBoard()
    Board.drawGui(player)  
    [piece.drawPiece() for piece in pieces]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = event

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        exit(0)

    if not gameover:
        # Checks for checks
        legalMoves = getMoves(Board.board,player[:1])
        if isCheck(Board.board,player[:1]):
            legalMoves = [move for move in legalMoves
                        if not isCheck(playMove(Board.board,*move,"q"),player[:1])]
            if not legalMoves: 
                
                gameover = 'checkMate'
            else:
                Board.drawText("CHECK!")

        elif not legalMoves:
            Board.drawText("STALEMATE!")
            gameover = 'staleMate'


        # Checks for clicks and updates board
        for piece in pieces:
            if piece.type[-1:] == player[0] and piece.active: 
                for c, r in [(tc, tr) for (fc,fr),(tc,tr) in legalMoves
                        if (fc,fr) == (piece.c, piece.r)]:
                    if MoveSquare(piece.screen, c, r, Board.board).update(click):                  
                        Board.board = playMove(Board.board, (piece.c, piece.r), (c, r), "q")
                        Board.lastMoves = [Board.transformCRToXY(c, r), Board.transformCRToXY(piece.c, piece.r)]
                        Board.takenPieces.append(g.takenPiece) if g.takenPiece else None
                        pieces = Board.updatePieces()
                        player = 'black' if player == 'white' else 'white'
                piece.checkForClick(click)
            else:
                try: piece.checkForClick(click) if piece.type[-1:] == player[0] else None
                except: pass

        # checks for timeout
        if Board.wT < 0 or Board.bT < 0:
            Board.drawText("TIME OUT!")
            gameover = 'timeOut'

    else:
        Board.drawText(f"GAME OVER! {gameover.upper()}", w=300)

        