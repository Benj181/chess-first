from lib.board import Board
from lib.classes import Piece
from lib.movesquare import MoveSquare
import pygame 
import time

pygame.init()
screen = pygame.display.set_mode((900, 800)) #, pygame.FULLSCREEN
clock = pygame.time.Clock()
pygame.display.set_caption('chess')

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
turn = True
local_toggle = [False, 0]
click = None
check = False

while True:
    clock.tick(60)
    pygame.display.update()
    Board.draw_GUI(turn, taken_pieces)
    Board.draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = event

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        exit(0)
    
    for piece in white_pieces + black_pieces:
        piece.draw_piece()

                    
    for piece in white_pieces + black_pieces:
        for new_x, new_y in piece.valid_moves:
            if board[new_y][new_x][0] == 'king':
                check = True

    if turn:
        for piece in white_pieces:
            if piece.active:
                for new_x, new_y in piece.valid_moves:
                    if MoveSquare(piece.screen, [new_x, new_y], piece.square_size, Board.board_padding, piece.piece_padding, board).update(click):       
                        board[piece.y_cord][piece.x_cord], board[new_y][new_x] = [None, None], piece.data
                        piece.x_cord, piece.y_cord, piece.active = new_x, new_y, False 
                        for b_piece in black_pieces:
                            if b_piece.cordinates() == piece.cordinates():
                                b_piece.taken = True
                                taken_pieces.append(b_piece)
                        turn = not turn
                piece.check_for_click(click, board)  
            else:
                if click:
                    piece.check_for_click(click, board)  

    else:
        for piece in black_pieces:
            if piece.active:
                for new_x, new_y in piece.valid_moves:
                    if MoveSquare(piece.screen, [new_x, new_y], piece.square_size, Board.board_padding, piece.piece_padding, board).update(click):
                        board[piece.y_cord][piece.x_cord], board[new_y][new_x] = [None, None], piece.data
                        piece.x_cord, piece.y_cord, piece.active = new_x, new_y, False 
                        for w_piece in white_pieces:
                            if w_piece.cordinates() == piece.cordinates():
                                w_piece.taken = True
                                taken_pieces.append(w_piece)
                        turn = not turn
                piece.check_for_click(click, board)  
            else:
                if click:
                    piece.check_for_click(click, board)

    Board.draw_labels()
