import pygame
import numpy as np
 
class BoardClass:
    def __init__(self, screen, board):
        self.screenS, _ = pygame.display.get_surface().get_size()
        self.screen = screen
        self.board = board
        self.colors = {'w' : (255, 255, 255), 
                       'b' : (0, 0, 0),
                       'grey' : (85, 85, 85), 
                       'previewMove': (100, 100, 100), 
                       'highlight': (244,246,128), 
                       'text': (140,139,137),
                       'board': (181, 136, 99),
                       'field': (240, 217, 181),
                       'bg': (48,46,43)}
        self.squareS = 80
        self.bS = self.squareS * 8
        self.bP = (self.screenS - self.bS) / 2
        self.wT, self.bT = 10*60, 10*60
        self.lastMoves = []
        self.takenPieces = []
    

    def LoadImages(self):
        self.pieceImg = dict()
        for pieceName in ['p_w', 'p_b', 'r_w', 'r_b', 'n_w', 'n_b', 'b_w', 'b_b', 'q_w', 'q_b', 'k_w', 'k_b']:
            self.pieceImg[pieceName] = pygame.image.load(f"img/{pieceName}.svg")


    def drawBoard(self):
        self.screen.fill(self.colors['bg'])
        pygame.draw.rect(self.screen, self.colors['board'], 
                         (self.bP, self.bP, self.bS, self.bS))
             
        f = lambda x, y: pygame.draw.rect(self.screen, self.colors['field'],
                                     (self.bP + x*self.squareS, 
                                      self.bP + y*self.squareS, 
                                      self.squareS, 
                                      self.squareS))

        [f(x, y) for x in range(8) for y in range(8) if (x + y) % 2 == 0]

        self.font = pygame.font.SysFont('consolas', 25, True)
        for i in range(8): # Rank and file numbers and letters
            num = self.font.render(str(8 - i), 1, self.colors['text'])
            let = self.font.render(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][i], 1, self.colors['text'])
            self.screen.blit(num, (self.bP - num.get_width() - 8, self.bP + self.squareS/2 - num.get_height()/2 + self.squareS*i))
            self.screen.blit(let, (self.bP + self.squareS/2 - let.get_width()/2 + self.squareS*i, self.bP + self.bS + 5))


    def drawGui(self, a_player):
        self.wT -= 1/60 if a_player == 'white' else 0
        self.bT -= 1/60 if a_player == 'black' else 0
        self.drawText(f"P1: {divmod(int(self.wT), 60)}", self.bP)
        self.drawText(f"P2: {divmod(int(self.bT), 60)}", self.screenS - self.bP - 160)

        for move in self.lastMoves:
            highlight = pygame.Surface((self.squareS, self.squareS), pygame.SRCALPHA)
            highlight.fill((*self.colors['highlight'], 100))
            self.screen.blit(highlight, (move[0], move[1]))

    def drawTakenPieces(self, takenPieces):
        p = {'p' : 1, 'n' : 3, 'b' : 3, 'r' : 5, 'q' : 9, 'k' : 0}
        wP = sum([p[piece[:1]] for piece in takenPieces if piece[-1:] == 'b'])
        bP = sum([p[piece[:1]] for piece in takenPieces if piece[-1:] == 'w'])
        

    def drawText(self, text, pos=0, w=160, h=40):
        square = pygame.Surface((w, h), pygame.SRCALPHA)
        square.fill(self.colors['grey'])
        self.font = pygame.font.SysFont('consolas', 20, True)
        text = self.font.render(text, True, self.colors['w'])
        square.blit(text, (square.get_width()/2 - text.get_width()/2, square.get_height()/2 - text.get_height()/2)) 
        if not pos:
            self.screen.blit(square, (self.screenS/2 - square.get_width()/2, self.bP/2 - square.get_height()/2))
        else:
            self.screen.blit(square, (pos, self.bP/2 - square.get_height()/2))


    def transformCRToXY(self, c, r): # linalg magic
        rotMatrix = np.array([[0, -1], [1, 0]])
        vec = np.array([c, r])
        vec = np.matmul(rotMatrix, vec)
        c, r = vec[0] + 7, vec[1]
        xPos = int(self.bP + self.squareS * r)
        yPos = int(self.bP + self.squareS * c)
        return (xPos, yPos)
    

    def updatePieces(self):
        pieces = []
        for c, col in enumerate(self.board[:-2]):
            for r, piece in enumerate(col):
                if piece:
                    pieces.append(Piece(self.screen, (c, r), piece, self.pieceImg[piece], self.board))
        return pieces
  
    
class Piece(BoardClass):
    def __init__(self, screen, coordinate, type, img, board):
        BoardClass.__init__(self, screen, board)
        self.img = pygame.transform.scale(img, (self.squareS, self.squareS))
        self.type = type
        self.active = False
        self.c, self.r = coordinate

    
    def drawPiece(self):
        self.xPos, self.yPos = BoardClass.transformCRToXY(self, self.c, self.r)
        # Highlight piece if active
        piece = pygame.Surface((self.squareS, self.squareS), pygame.SRCALPHA)
        piece.fill((*self.colors['highlight'], 150)) if self.active else piece.fill((0, 0, 0, 0))
        # Draw piece
        piece.blit(self.img, (0, 0))
        self.screen.blit(piece, (self.xPos, self.yPos))    


    def checkForClick(self, click):          
        self.active = True if self.xPos + self.squareS > click.pos[0] > self.xPos and self.yPos + self.squareS > click.pos[1] > self.yPos and click.button == 1 else False


class MoveSquare():
    def __init__(self, screen, c, r, board):
        BoardClass.__init__(self, screen, board)
        self.xPos, self.yPos = BoardClass.transformCRToXY(self, c, r)
        square = pygame.Surface((self.squareS, self.squareS), pygame.SRCALPHA)
        if board[c][r]:
            pygame.draw.circle(square, 
                               (*self.colors['previewMove'], 100), 
                               (self.squareS/2, self.squareS/2), 0.48 * self.squareS, width=7)
        else:
            pygame.draw.circle(square, 
                               (*self.colors['previewMove'], 100), 
                               (self.squareS/2, self.squareS/2), 0.17 * self.squareS)
        self.screen.blit(square, (self.xPos, self.yPos))          

    def update(self, click):
        if click.button == 1:
            if self.xPos + self.squareS > click.pos[0] > self.xPos and self.yPos + self.squareS > click.pos[1] > self.yPos:
                return True