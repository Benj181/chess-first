from locale import locale_alias
from turtle import width
from matplotlib.pyplot import pie
from numpy import squeeze, take
from lib import Board, Piece
import pygame 
import time

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('chess')
clock = pygame.time.Clock()

Board = Board(screen)
white_pieces = [*[Piece(screen, (i, 6), 'white', 'pawn') for i in range(8)],
                    *[Piece(screen, (i*7, 7), 'white', 'rook') for i in range(2)],
                    *[Piece(screen, (i*5 + 1, 7), 'white', 'knight') for i in range(2)],
                    *[Piece(screen, (i*3 + 2, 7), 'white', 'bishop') for i in range(2)],
                    Piece(screen, (3, 7), 'white', 'queen'),
                    Piece(screen, (4, 7), 'white', 'king')]

black_pieces = [*[Piece(screen, (i, 1), 'black', 'pawn') for i in range(8)],
                    *[Piece(screen, (i*7, 0), 'black', 'rook') for i in range(2)],
                    *[Piece(screen, (i*5 + 1, 0), 'black', 'knight') for i in range(2)],
                    *[Piece(screen, (i*3 + 2, 0), 'black', 'bishop') for i in range(2)],
                    Piece(screen, (3, 0), 'black', 'queen'),
                    Piece(screen, (4, 0), 'black', 'king')]
taken_pieces = []
timer = time.time()
turn = 'white'
local_toggle = [False, 0]
while True:
    # init stuff
    clock.tick(60)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    cursorPos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit(0)
    
    Board.draw_board()
    Board.draw_GUI(turn, taken_pieces)

    for piece in white_pieces:
        piece.update_piece(Board)

    for piece in black_pieces:
        piece.update_piece(Board)

    if turn == 'white':
        for i, piece in enumerate(white_pieces):
            if piece.hover_toggle:
                local_toggle = [True, i]

        if not white_pieces[local_toggle[1]].hover_toggle:
            local_toggle = [False, 0]
            
        if local_toggle[0]:
            if white_pieces[local_toggle[1]].update_hover(Board):
                data = white_pieces[local_toggle[1]].taken_data
                if data[1][0]:
                    for i, piece in enumerate(black_pieces):
                        if piece.cordinates() == data[0]:
                            black_pieces[i].taken = True
                            taken_pieces.append(piece)
                turn = 'black'

        else:
            for piece in white_pieces:
                piece.update_hover(Board)                    

    if turn == 'black':
        for i, piece in enumerate(black_pieces):
            if piece.hover_toggle:
                local_toggle = [True, i]

        if not black_pieces[local_toggle[1]].hover_toggle:
            local_toggle = [False, 0]
            
        if local_toggle[0]:
            if black_pieces[local_toggle[1]].update_hover(Board):
                data = black_pieces[local_toggle[1]].taken_data
                if data[1][0]:
                    for i, piece in enumerate(white_pieces):
                        if piece.cordinates() == data[0]:
                            white_pieces[i].taken = True
                            taken_pieces.append(piece)
                turn = 'white'

        else:
            for piece in black_pieces:
                piece.update_hover(Board)


    Board.draw_labels()
