from turtle import width
from matplotlib.pyplot import pie
from numpy import squeeze, take
from lib import Board, Piece
import pygame 
import time

pygame.init()
screen = pygame.display.set_mode((0, 0))#, pygame.FULLSCREEN
pygame.display.set_caption('chess')
clock = pygame.time.Clock()

Board = Board(screen)
white_piece_types = [[Piece(screen, (i, 6), 'white', 'pawn') for i in range(8)]]
black_piece_types = [[Piece(screen, (i, 1), 'black', 'pawn') for i in range(8)]]
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
        # [print(i) for i in Board.board]
        pygame.quit()
        exit(0)
    
    Board.draw_board()
    Board.draw_GUI(turn)

    for pieces in white_piece_types:
        for piece in pieces:
            piece.update_piece(Board)

    for pieces in black_piece_types:
        for piece in pieces:
            piece.update_piece(Board)

    if turn == 'white':
        for pieces in white_piece_types:
            for i, piece in enumerate(pieces):
                if piece.hover_toggle:
                    local_toggle = [True, i]

            if not pieces[local_toggle[1]].hover_toggle:
                local_toggle = [False, 0]
            
            if local_toggle[0]:
                if pieces[local_toggle[1]].update_pos(Board):
                    data = pieces[local_toggle[1]].taken_data
                    if data[1][0]:
                        for pieces in black_piece_types:
                            for i, piece in enumerate(pieces):
                                if (piece.x_cord, piece.y_cord) == data[0]:
                                    black_piece_types[0][i].taken = True
                                    taken_pieces.append(piece)
                    turn = 'black'

            else: 
                for piece in pieces:
                    piece.update_pos(Board)                    

    if turn == 'black':
        for pieces in black_piece_types:
            for i, piece in enumerate(pieces):
                if piece.hover_toggle:
                    local_toggle = [True, i]

            if not pieces[local_toggle[1]].hover_toggle:
                local_toggle = [False, 0]
            
            if local_toggle[0]:
                if pieces[local_toggle[1]].update_pos(Board):
                    data = pieces[local_toggle[1]].taken_data
                    if data[1][0]:
                        for pieces in white_piece_types:
                            for i, piece in enumerate(pieces):
                                if (piece.x_cord, piece.y_cord) == data[0]:
                                    white_piece_types[0][i].taken = True
                                    taken_pieces.append(piece)
                    turn = 'white'

            else:
                for piece in pieces:
                    piece.update_pos(Board)

    Board.draw_labels()
