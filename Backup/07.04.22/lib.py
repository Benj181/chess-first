from string import whitespace
import pygame
import time

class Board:
    def __init__(self, screen):
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.screen = screen
        self.black = (181, 136, 99)
        self.white = (240, 217, 181)
        self.bg = (22, 21, 18)
        self.square_size = 90
        self.board_size = self.square_size*8
        self.board_padding = ((self.screen_width - self.board_size) / 2, (self.screen_height - self.board_size) / 2)
        self.x_start = self.board_padding[0]
        self.y_start = self.board_padding[1]
        self.hover_active = False
        self.font = pygame.font.SysFont('consolas', 20, True)
        self.board =   [[['rook', 'black'], ['knight', 'black'], ['bishop', 'black'], ['queen', 'black'], ['king', 'black'], ['bishop', 'black'], ['knight', 'black'], ['rook', 'black']], 
                        [['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black'], ['pawn', 'black']], 
                        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
                        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
                        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
                        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
                        [['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white'], ['pawn', 'white']], 
                        [['rook', 'white'], ['knight', 'white'], ['bishop', 'white'], ['queen', 'white'], ['king', 'white'], ['bishop', 'white'], ['knight', 'white'], ['rook', 'white']]]


    def draw_board(self):
        # bg
        self.screen.fill(self.bg)
        pygame.draw.rect(self.screen, self.black, (self.board_padding[0], self.board_padding[1], self.board_size, self.board_size))
        # sqaures
        for y in range(8):
            if y % 2 == 0:
                for x in range(0, 8, 2):
                    pygame.draw.rect(self.screen, self.white, (self.x_start + x*self.square_size, self.y_start + y*self.square_size, self.square_size, self.square_size))
            else:
                for x in range(1, 8, 2):
                    pygame.draw.rect(self.screen, self.white, (self.x_start + x*self.square_size, self.y_start + y*self.square_size, self.square_size, self.square_size))


    def draw_GUI(self, turn, taken_pieces):
        temp = self.font.render(turn, True, self.black)
        self.screen.blit(temp, (self.board_padding[0] + self.board_size - temp.get_width(), self.board_padding[1] - temp.get_height()))
        taken_white = []
        taken_black = []
        for piece in taken_pieces:
            if piece.side == 'white':
                taken_white.append(piece.type) 
            else:
                taken_black.append(piece.type)
        # draws the taken pieces
        for i, word in enumerate(sorted(taken_white)):
            temp = self.font.render(word, True, self.black)
            self.screen.blit(temp, (self.board_padding[0] - temp.get_width() - 5, self.board_padding[1] + temp.get_height()*i))
        
        for i, word in enumerate(sorted(taken_black)):
            temp = self.font.render(word, True, self.black)
            self.screen.blit(temp, (self.board_padding[0] + self.board_size + 5, self.board_padding[1] + self.board_size - temp.get_height()*(i + 1)))


    def draw_labels(self):
        # labels
            # numbers
        for i, pos in enumerate([(self.x_start + self.board_size - self.square_size/6, self.y_start + self.square_size*i) for i in range(8)]):
            self.screen.blit(self.font.render(str(8 - i), 1, (0, 0, 0)), (pos[0], pos[1]))
            # letters
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i, pos in enumerate([(self.x_start + self.square_size*i + 2, self.y_start + self.board_size - self.square_size/5) for i in range(8)]):
            self.screen.blit(self.font.render(self.letters[i], 1, (0, 0, 0)), (pos[0], pos[1]))


class Piece(Board):
    def __init__(self, screen, cordinate, side, type):
        Board.__init__(self, screen)
        self.size = 80
        self.side = side
        self.type = type
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)
        self.t = time.time()
        self.hover_toggle = False
        self.taken = False
        self.x_cord = cordinate[0]
        self.y_cord = cordinate[1]
        self.piece_padding = int((self.square_size - self.size) / 2)
        self.start_pos = self.board_padding[0], self.board_padding[1]
        self.xpos = self.start_pos[0] + self.square_size * self.x_cord + self.piece_padding
        self.ypos = self.start_pos[1] + self.square_size * self.y_cord + self.piece_padding
        self.data = [self.type, self.side]
        if self.side == 'white':
            self.color = self.white
        else:
            self.color = self.black


    def cordinates(self):
        return (self.x_cord, self.y_cord)


    def update_piece(self, Board):
        if not self.taken:
            self.keys = pygame.key.get_pressed()
            self.cursorPos = pygame.mouse.get_pos()
            piece = pygame.Surface((self.size, self.size))
            piece.fill(self.color)
            highlight = pygame.Surface((self.size, self.size))
            highlight.fill(self.grey)
            highlight.set_alpha(100)
            self.xpos = int(self.start_pos[0] + self.square_size * self.x_cord + self.piece_padding)
            self.ypos = int(self.start_pos[1] + self.square_size * self.y_cord + self.piece_padding)
            if self.hover_toggle:
                pygame.draw.rect(self.screen, (100,111,65), (self.xpos - self.piece_padding, self.ypos - self.piece_padding, self.square_size, self.square_size))    
            else:
                if self.xpos + self.size > self.cursorPos[0] > self.xpos and self.ypos + self.size > self.cursorPos[1] > self.ypos:
                    self.screen.blit(piece, (self.xpos, self.ypos))
                    self.screen.blit(highlight, (self.xpos, self.ypos))
                else:
                    self.screen.blit(piece, (self.xpos, self.ypos))
            self.screen.blit(self.font.render(self.type, True, self.grey), (self.xpos, self.ypos))
        else:
            self.hover_toggle = False


    def valid_moves(self, Board):
        valid_moves = []
        if self.type == 'pawn':
            if self.side == 'white':
                if self.y_cord == 6:
                    if not Board.board[self.y_cord - 2][self.x_cord][0]:
                        valid_moves.append((self.x_cord, self.y_cord - 2))
                if self.y_cord != 0:
                    if not Board.board[self.y_cord - 1][self.x_cord][0]:
                            valid_moves.append((self.x_cord, self.y_cord - 1))
                if self.x_cord != 7:
                    if Board.board[self.y_cord - 1][self.x_cord + 1][1] == 'black':
                        valid_moves.append((self.x_cord + 1, self.y_cord - 1))
                if self.x_cord != 0:
                    if Board.board[self.y_cord - 1][self.x_cord - 1][1] == 'black':
                        valid_moves.append((self.x_cord - 1, self.y_cord - 1))
            if self.side == 'black':
                if self.y_cord == 1:
                    if not Board.board[self.y_cord + 2][self.x_cord][0]:
                        valid_moves.append((self.x_cord, self.y_cord + 2))
                if self.y_cord != 7:
                    if not Board.board[self.y_cord + 1][self.x_cord][0]:
                            valid_moves.append((self.x_cord, self.y_cord + 1))
                if self.x_cord != 7:
                    if Board.board[self.y_cord + 1][self.x_cord + 1][1] == 'white':
                        valid_moves.append((self.x_cord + 1, self.y_cord + 1))
                if self.x_cord != 0:
                    if Board.board[self.y_cord + 1][self.x_cord - 1][1] == 'white':
                        valid_moves.append((self.x_cord - 1, self.y_cord + 1))
        return valid_moves


    def hover_square(self):
        self.cursorPos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if self.xpos + self.size > self.cursorPos[0] > self.xpos and self.ypos + self.size > self.cursorPos[1] > self.ypos and self.click[0]:
            return True
        elif self.xpos + self.size > self.cursorPos[0] > self.xpos and self.ypos + self.size > self.cursorPos[1] > self.ypos:
            pygame.draw.rect(self.screen, (129,150,105), (self.xpos - self.piece_padding, self.ypos - self.piece_padding, self.square_size, self.square_size))
        else:
            pygame.draw.circle(self.screen, (129,150,105), (int(self.xpos + self.size/2), int(self.ypos + self.size/2)), 20)
    

    def draw_hover_square(self, Board):
        if self.xpos + self.size > self.cursorPos[0] > self.xpos and self.ypos + self.size > self.cursorPos[1] > self.ypos and self.click[0] and time.time() - self.t > 0.3:
            self.hover_toggle = False
            self.t = time.time()
        if self.valid_moves(Board): # if there are possible moves, highlight them
            for move in self.valid_moves(Board):
                if Piece(self.screen, [move[0], move[1]], self.side, self.type).hover_square():
                    return self.do_move(move[0], move[1], Board)


    def update_hover(self, Board):         
        self.cursorPos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if not self.taken: # checks if the user has clicked a piece
            if self.hover_toggle:
                return self.draw_hover_square(Board)
            else:
                if self.xpos + self.size > self.cursorPos[0] > self.xpos and self.ypos + self.size > self.cursorPos[1] > self.ypos and self.click[0] and time.time() - self.t > 0.3:
                    self.hover_toggle = True
                    self.t = time.time()


    def do_move(self, new_x, new_y, Board):
        Board.board[self.y_cord][self.x_cord] = [None, None]
        self.taken_data = ((new_x, new_y), Board.board[new_y][new_x])
        Board.board[new_y][new_x] = self.data
        self.x_cord = new_x
        self.y_cord = new_y
        self.update_piece(Board)
        self.t = time.time()
        self.hover_toggle = False
        return True