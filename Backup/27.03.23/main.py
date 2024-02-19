from lib.board import Board
from lib.classes import Piece
import pygame 
import time

pygame.init()
screen = pygame.display.set_mode((900, 800)) #, pygame.FULLSCREEN
pygame.display.set_caption('chess')
clock = pygame.time.Clock()

Board = Board(screen)
white_pieces = [*[Piece(screen, (i, 6), 'white', 'pawn', Board.square_size, Board.board_padding) for i in range(8)],
                Piece(screen, (0, 7), 'white', 'rook', Board.square_size, Board.board_padding),
                Piece(screen, (1, 7), 'white', 'knight', Board.square_size, Board.board_padding),
                Piece(screen, (2, 7), 'white', 'bishop', Board.square_size, Board.board_padding),
                Piece(screen, (3, 7), 'white', 'queen', Board.square_size, Board.board_padding),
                Piece(screen, (4, 7), 'white', 'king', Board.square_size, Board.board_padding),
                Piece(screen, (5, 7), 'white', 'bishop', Board.square_size, Board.board_padding),
                Piece(screen, (6, 7), 'white', 'knight', Board.square_size, Board.board_padding),
                Piece(screen, (7, 7), 'white', 'rook', Board.square_size, Board.board_padding)]

black_pieces = [*[Piece(screen, (i, 1), 'black', 'pawn', Board.square_size, Board.board_padding) for i in range(8)],
                Piece(screen, (0, 0), 'black', 'rook', Board.square_size, Board.board_padding),
                Piece(screen, (1, 0), 'black', 'knight', Board.square_size, Board.board_padding),
                Piece(screen, (2, 0), 'black', 'bishop', Board.square_size, Board.board_padding),
                Piece(screen, (3, 0), 'black', 'queen', Board.square_size, Board.board_padding),
                Piece(screen, (4, 0), 'black', 'king', Board.square_size, Board.board_padding),
                Piece(screen, (5, 0), 'black', 'bishop', Board.square_size, Board.board_padding),
                Piece(screen, (6, 0), 'black', 'knight', Board.square_size, Board.board_padding),
                Piece(screen, (7, 0), 'black', 'rook', Board.square_size, Board.board_padding)]

board = [[['rook', 'black'], ['knight', 'black'], ['bishop', 'black'], ['queen', 'black'], ['king', 'black'], ['bishop', 'black'], ['knight', 'black'], ['rook', 'black']], 
        [['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black']], 
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white']], 
        [['rook', 'white'], ['knight', 'white'], ['bishop', 'white'], ['queen', 'white'], ['king', 'white'], ['bishop', 'white'], ['knight', 'white'], ['rook', 'white']]]

taken_pieces = []
turn = 'white'
local_toggle = [False, 0]
check = False
while True:
    clock.tick(60)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    cursorPos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    Board.draw_board()
    Board.draw_GUI(turn, taken_pieces)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit(0)
    
    for piece in white_pieces + black_pieces:
        piece.draw_piece()
        if piece.valid_moves(board)[1]:
            check = True
            print('WARNING')

    if turn == 'white':
        for i, piece in enumerate(white_pieces):
            if piece.active:
                local_toggle = [True, i]

        if not white_pieces[local_toggle[1]].active:
            local_toggle = [False, 0]
            
        if local_toggle[0]:
            if white_pieces[local_toggle[1]].check_for_click(board):
                for i, piece in enumerate(black_pieces):
                    if piece.cordinates() == white_pieces[local_toggle[1]].taken_data:
                        black_pieces[i].taken = True
                        taken_pieces.append(piece)
                turn = 'black'
        else:
            for piece in white_pieces:
                piece.check_for_click(board)                    

    if turn == 'black':
        for i, piece in enumerate(black_pieces):
            if piece.active:
                local_toggle = [True, i]

        if not black_pieces[local_toggle[1]].active:
            local_toggle = [False, 0]

        if local_toggle[0]:
            if black_pieces[local_toggle[1]].check_for_click(board):
                for i, piece in enumerate(white_pieces):
                    if piece.cordinates() == black_pieces[local_toggle[1]].taken_data:
                        white_pieces[i].taken = True
                        taken_pieces.append(piece)
                turn = 'white'
        else:
            for piece in black_pieces:
                piece.check_for_click(board)
    Board.draw_labels()
