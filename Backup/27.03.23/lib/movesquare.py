import pygame
class MoveSquare():
    def __init__(self, screen, cordinate, square_size, board_padding, board):
        self.screen = screen
        self.board = board
        self.size = 80
        self.x = cordinate[0]
        self.y = cordinate[1]
        self.x_pos = board_padding[0] + square_size * self.x + int((square_size - self.size) / 2)
        self.y_pos = board_padding[1] + square_size * self.y + int((square_size - self.size) / 2)

    def update(self):
        cursorPos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        padding = 5
        square = pygame.Surface((self.size + padding*2, self.size + padding*2), pygame.SRCALPHA)
        if self.x_pos + self.size > cursorPos[0] > self.x_pos and self.y_pos + self.size > cursorPos[1] > self.y_pos and click[0]:
            return True
        elif self.x_pos + self.size > cursorPos[0] > self.x_pos and self.y_pos + self.size > cursorPos[1] > self.y_pos:
            if self.board[self.y][self.x][0]:
                square.fill((255, 100, 100))
                pygame.draw.rect(square, (0, 0 ,0, 0), (padding, padding, self.size, self.size))
            else:
                square.fill((129, 150, 105))
        else:
            if self.board[self.y][self.x][0]:
                square.fill((129, 150, 105))
                pygame.draw.rect(square, (0, 0 ,0, 0), (padding, padding, self.size, self.size)) 
            else:
                pygame.draw.circle(square, (129, 150, 105, 255), (self.size/2 + padding, self.size/2 + padding), self.size/4)
        self.screen.blit(square, (self.x_pos-5, self.y_pos-5))  
