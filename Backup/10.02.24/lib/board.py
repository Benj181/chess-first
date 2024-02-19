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
        self.check = False
        

    def draw_board(self):
        self.screen.fill(self.bg)
        pygame.draw.rect(self.screen, self.black, (self.board_padding[0], self.board_padding[1], self.board_size, self.board_size))
        for y in range(8):
            if y % 2 == 0:
                for x in range(0, 8, 2):
                    pygame.draw.rect(self.screen, self.white, (self.x_start + x*self.square_size, self.y_start + y*self.square_size, self.square_size, self.square_size))
            else:
                for x in range(1, 8, 2):
                    pygame.draw.rect(self.screen, self.white, (self.x_start + x*self.square_size, self.y_start + y*self.square_size, self.square_size, self.square_size))


    def draw_GUI(self, turn, taken_pieces):
        if turn:
            temp = self.font.render('white', True, self.black)
        else:
            temp = self.font.render('black', True, self.black)
        self.screen.blit(temp, (self.board_padding[0] + self.board_size - temp.get_width(), self.board_padding[1] - temp.get_height()))
        taken_white = [piece.type for piece in taken_pieces if piece.side == 'white']
        taken_black = [piece.type for piece in taken_pieces if piece.side == 'black']
        for i, word in enumerate(sorted(taken_white)):
            temp = self.font.render(word, True, self.black)
            self.screen.blit(temp, (self.board_padding[0] - temp.get_width() - 5, self.board_padding[1] + temp.get_height()*i))            
        for i, word in enumerate(sorted(taken_black)):
            temp = self.font.render(word, True, self.black)
            self.screen.blit(temp, (self.board_padding[0] + self.board_size + 5, self.board_padding[1] + self.board_size - temp.get_height()*(i + 1)))


    def draw_labels(self):
        for i, pos in enumerate([(self.x_start + self.board_size - self.square_size/6, self.y_start + self.square_size*i) for i in range(8)]):
            self.screen.blit(self.font.render(str(8 - i), 1, (0, 0, 0)), (pos[0], pos[1]))
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i, pos in enumerate([(self.x_start + self.square_size*i + 2, self.y_start + self.board_size - self.square_size/5) for i in range(8)]):
            self.screen.blit(self.font.render(self.letters[i], 1, (0, 0, 0)), (pos[0], pos[1]))
