import pygame
import time

class Piece():
    def __init__(self, screen, cordinate, side, type, square_size, board_padding):
        self.screen = screen
        self.size = 80
        self.square_size = square_size
        self.board_padding = board_padding
        self.side = side
        self.type = type
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
        self.valid_moves = []
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
            self.xpos, self.ypos = int(self.start_pos[0] + self.square_size * self.x_cord + self.piece_padding), int(self.start_pos[1] + self.square_size * self.y_cord + self.piece_padding)
            piece = pygame.Surface((self.size, self.size))
            piece.fill(self.color)
            self.screen.blit(piece, (self.xpos, self.ypos))
            self.screen.blit(self.font.render(self.type, True, self.opposite), (self.xpos, self.ypos))
            surface = pygame.Surface((self.size, self.size))
            surface.fill((100, 100, 100))
            surface.set_alpha(100)
            if self.active or self.xpos + self.size > pygame.mouse.get_pos()[0] > self.xpos and self.ypos + self.size > pygame.mouse.get_pos()[1] > self.ypos:
                self.screen.blit(surface, (self.xpos, self.ypos))    


    def check_for_click(self, click, board):         
        if not self.taken: 
            if self.xpos + self.size > click.pos[0] > self.xpos and self.ypos + self.size > click.pos[1] > self.ypos:
                self.active = True
                self.gen_moves(board) 
            else:
                self.active = False



    def gen_moves(self, board):
        valid_moves = []
        def moves(cords):
                temp = None
                for i, cord in enumerate(cords):
                    if 7 < cord[0] or cord[0] < 0 or 7 < cord[1] or cord[1] < 0:
                        cords.pop(i)
                        continue
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
        self.valid_moves = valid_moves