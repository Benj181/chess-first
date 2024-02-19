import pygame
import time
from lib.movesquare import MoveSquare

class Piece():
    def __init__(self, screen, cordinate, side, type, square_size, board_padding):
        self.screen = screen
        self.size = 80
        self.square_size = square_size
        self.board_padding = board_padding
        self.side = side
        self.type = type
        self.t = time.time()
        self.active = False
        self.taken = False
        self.x_cord = cordinate[0]
        self.y_cord = cordinate[1]
        self.piece_padding = int((self.square_size - self.size) / 2)
        self.start_pos = self.board_padding[0], self.board_padding[1]
        self.xpos = self.start_pos[0] + self.square_size * self.x_cord + self.piece_padding
        self.ypos = self.start_pos[1] + self.square_size * self.y_cord + self.piece_padding
        self.data = [self.type, self.side]
        self.font = pygame.font.SysFont('consolas', 20, True)
        if self.side == 'white':
            self.color = (255, 255, 255)
            self.opposite = (0, 0, 0)
        else:
            self.color = (0, 0, 0)
            self.opposite = (255, 255, 255)


    def cordinates(self):
        return (self.x_cord, self.y_cord)


    def draw_piece(self):
        if not self.taken:
            self.cursorPos = pygame.mouse.get_pos()
            self.xpos = int(self.start_pos[0] + self.square_size * self.x_cord + self.piece_padding)
            self.ypos = int(self.start_pos[1] + self.square_size * self.y_cord + self.piece_padding)
            piece = pygame.Surface((self.size, self.size))
            piece.fill(self.color)
            self.screen.blit(piece, (self.xpos, self.ypos))
            self.screen.blit(self.font.render(self.type, True, self.opposite), (self.xpos, self.ypos))
            surface = pygame.Surface((self.size, self.size))
            surface.fill((100, 100, 100))
            surface.set_alpha(100)
            if self.active:
                surface.fill((80, 80, 80))
                self.screen.blit(surface, (self.xpos, self.ypos))    
            else:
                if self.xpos + self.size > self.cursorPos[0] > self.xpos and self.ypos + self.size > self.cursorPos[1] > self.ypos:
                    self.screen.blit(surface, (self.xpos, self.ypos))
                    # insert pic 
        else:
            self.active = False


    def check_for_click(self, board):         
        self.cursorPos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if not self.taken: 
            if self.active: # if a piece is clicked on, draw its possible moves
                if self.click[0] and time.time() - self.t > 0.3:
                    self.active, self.t = False, time.time()
                return self.draw_moves(board)
            else: # else, check for click on piece
                if self.xpos + self.size > self.cursorPos[0] > self.xpos and self.ypos + self.size > self.cursorPos[1] > self.ypos and self.click[0] and time.time() - self.t > 0.3:
                    self.active, self.t = True, time.time()


    def draw_moves(self, board):
        for new_x, new_y in self.valid_moves(board)[0]:
            if MoveSquare(self.screen, [new_x, new_y], self.square_size, self.board_padding, board).update():
                board[self.y_cord][self.x_cord] = [None, None]
                self.taken_data = (new_x, new_y)
                board[new_y][new_x] = self.data
                self.x_cord, self.y_cord = new_x, new_y
                self.draw_piece()
                self.active, self.t = False, time.time()
                return True


    def valid_moves(self, board):
        valid_moves = []
        self.check = False
        def moves(cords):
                temp = None
                for i, cord in enumerate(cords):
                    if 7 < cord[0] or cord[0] < 0 or 7 < cord[1] or cord[1] < 0:
                        cords.pop(i)
                        continue
                    if board[cord[1]][cord[0]][0] == 'king' and board[cord[1]][cord[0]][1] != self.side:
                        self.check = True
                    if board[cord[1]][cord[0]][1] == self.side:
                        temp = i
                        break
                    elif board[cord[1]][cord[0]][1]:
                        temp = i + 1
                        break
                        
                if type(temp) == int:
                    return cords[:temp]
                else:
                    return cords
#--------------------------------------------------------------------------------------------------------------------------
        if self.type == 'pawn':
            if self.side == 'white':
                if self.y_cord != 0:
                    if not board[self.y_cord - 1][self.x_cord][1]:
                        valid_moves.append((self.x_cord, self.y_cord - 1))                          
                        if self.y_cord == 6:
                            if not board[self.y_cord - 2][self.x_cord][1]:
                                valid_moves.append((self.x_cord, self.y_cord - 2))
                if self.x_cord != 7:
                    if board[self.y_cord - 1][self.x_cord + 1][1] == 'black':
                        valid_moves.append((self.x_cord + 1, self.y_cord - 1))
                if self.x_cord != 0:
                    if board[self.y_cord - 1][self.x_cord - 1][1] == 'black':
                        valid_moves.append((self.x_cord - 1, self.y_cord - 1))
            if self.side == 'black':
                if self.y_cord != 7:
                    if not board[self.y_cord + 1][self.x_cord][0]:
                        valid_moves.append((self.x_cord, self.y_cord + 1))
                        if self.y_cord == 1:
                            if not board[self.y_cord + 2][self.x_cord][1]:
                                valid_moves.append((self.x_cord, self.y_cord + 2))
                if self.x_cord != 7:
                    if board[self.y_cord + 1][self.x_cord + 1][1] == 'white':
                        valid_moves.append((self.x_cord + 1, self.y_cord + 1))
                if self.x_cord != 0:
                    if board[self.y_cord + 1][self.x_cord - 1][1] == 'white':
                        valid_moves.append((self.x_cord - 1, self.y_cord + 1))
#--------------------------------------------------------------------------------------------------------------------------
        if self.type == 'rook':
            for x, y in moves(list(zip([i for i in range(self.x_cord + 1, 8)], [self.y_cord for i in range(8)]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([self.x_cord for i in range(8)], [i for i in range(self.y_cord + 1, 8)]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([self.x_cord for i in range(8)], [i for i in range(0, self.y_cord)][::-1]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(0, self.x_cord)][::-1], [self.y_cord for i in range(8)]))):
                valid_moves.append((x, y))
#--------------------------------------------------------------------------------------------------------------------------
        if self.type == 'queen':              
            for x, y in moves(list(zip([i for i in range(self.x_cord + 1, 8)], [i for i in range(0, self.y_cord)][::-1]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(self.x_cord + 1, 8)], [i for i in range(self.y_cord + 1, 8)]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(0, self.x_cord)][::-1], [i for i in range(0, self.y_cord)][::-1]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(0, self.x_cord)][::-1], [i for i in range(self.y_cord + 1, 8)]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(self.x_cord + 1, 8)], [self.y_cord for i in range(8)]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([self.x_cord for i in range(8)], [i for i in range(self.y_cord + 1, 8)]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([self.x_cord for i in range(8)], [i for i in range(0, self.y_cord)][::-1]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(0, self.x_cord)][::-1], [self.y_cord for i in range(8)]))):
                valid_moves.append((x, y))
#--------------------------------------------------------------------------------------------------------------------------
        if self.type == 'king':
            for x, y in moves([(self.x_cord, self.y_cord - 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord, self.y_cord + 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord - 1, self.y_cord)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord + 1, self.y_cord)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord + 1, self.y_cord - 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord + 1, self.y_cord + 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord - 1, self.y_cord - 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord - 1, self.y_cord + 1)]):
                valid_moves.append((x, y))
#--------------------------------------------------------------------------------------------------------------------------
        if self.type == 'bishop':
            for x, y in moves(list(zip([i for i in range(self.x_cord + 1, 8)], [i for i in range(0, self.y_cord)][::-1]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(self.x_cord + 1, 8)], [i for i in range(self.y_cord + 1, 8)]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(0, self.x_cord)][::-1], [i for i in range(0, self.y_cord)][::-1]))):
                valid_moves.append((x, y))
            for x, y in moves(list(zip([i for i in range(0, self.x_cord)][::-1], [i for i in range(self.y_cord + 1, 8)]))):
                valid_moves.append((x, y))
#--------------------------------------------------------------------------------------------------------------------------
        if self.type == 'knight':
            for x, y in moves([(self.x_cord - 1, self.y_cord - 2)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord + 1, self.y_cord - 2)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord - 1, self.y_cord + 2)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord + 1, self.y_cord + 2)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord + 2, self.y_cord - 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord + 2, self.y_cord + 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord - 2, self.y_cord - 1)]):
                valid_moves.append((x, y))
            for x, y in moves([(self.x_cord - 2, self.y_cord + 1)]):
                valid_moves.append((x, y))
        return valid_moves, self.check
