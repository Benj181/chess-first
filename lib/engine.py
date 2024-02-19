# https://stackoverflow.com/questions/65629923/detecting-checks-more-efficiently-chess
from collections import defaultdict
from copy import deepcopy
from collections import defaultdict
import lib.globals as g
 
targets   = dict()
positions = [ (c,r) for c in range(8) for r in range(8) ]
def valid(P): 
    return [(c,r) for c,r in P if c in range(8) and r in range(8)]

targets["up"]        = { (c,r):valid( (c,r+v) for v in range(1,8))
                        for c,r in positions }
targets["down"]      = { (c,r):valid( (c,r-v) for v in range(1,8))
                        for c,r in positions }
targets["left"]      = { (c,r):valid( (c-h,r) for h in range(1,8))
                        for c,r in positions }
targets["right"]     = { (c,r):valid( (c+h,r) for h in range(1,8))
                        for c,r in positions }
targets["upleft"]    = { (c,r):[(cl,ru) for (_,ru),(cl,_) in zip(targets["up"][c,r],targets["left"][c,r])]
                        for c,r in positions }
targets["upright"]   = { (c,r):[(cr,ru) for (_,ru),(cr,_) in zip(targets["up"][c,r],targets["right"][c,r])]
                        for c,r in positions }
targets["downleft"]  = { (c,r):[(cl,rd) for (_,rd),(cl,_) in zip(targets["down"][c,r],targets["left"][c,r])]
                        for c,r in positions }
targets["downright"] = { (c,r):[(cr,rd) for (_,rd),(cr,_) in zip(targets["down"][c,r],targets["right"][c,r])]
                        for c,r in positions }
targets["vhPaths"]   = ["up","down","left","right"] 
targets["diagPaths"] = ["upleft","upright","downleft","downright"] 
targets["allPaths"]  = targets["vhPaths"]+targets["diagPaths"]
targets["rook"]    = { (c,r):[p for path in targets["vhPaths"] for p in targets[path][c,r]]
                        for c,r in positions }
targets["bishop"]  = { (c,r):[p for path in targets["diagPaths"] for p in targets[path][c,r]]
                        for c,r in positions }
targets["queen"]   = { (c,r):[p for path in targets["allPaths"] for p in targets[path][c,r]]
                        for c,r in positions }
targets["king"]    = { (c,r):[p for path in targets["allPaths"] for p in targets[path][c,r][:1]]
                        for c,r in positions }
targets["knight"]  = { (c,r):valid((c+h,r+v) for v,h in [(2,1),(2,-1),(1,2),(1,-2),(-2,1),(-2,-1),(-1,2),(-1,-2)])
                        for c,r in positions }
targets["wpawn"]   = { (c,r):valid([(c,r+1)]*(r>0) + [(c,r+2)]*(r==1))
                        for c,r in positions }
targets["bpawn"]   = { (c,r):valid([(c,r-1)]*(r<7) + [(c,r-2)]*(r==6))
                        for c,r in positions }
targets["wptake"]  = { (c,r):valid([(c+1,r+1),(c-1,r+1)]*(r>0))
                        for c,r in positions }
targets["bptake"]  = { (c,r):valid([(c+1,r-1),(c-1,r-1)]*(r<7))
                        for c,r in positions }
targets["wcastle"] = defaultdict(list,{ (4,0):[(2,0),(6,0)] })
targets["bcastle"] = defaultdict(list,{ (4,7):[(2,7),(6,7)] })
targets["breakCastle"] = defaultdict(list,{ (4,7):[(2,7),(6,7)], 
                                            (7,7):[(6,7)], (0,7):[(2,7)],
                                            (4,0):[(2,0),(6,0)],
                                            (7,0):[(6,0)], (1,0):[(2,0)]})
targets["rook"]["paths"]   = targets["vhPaths"]
targets["bishop"]["paths"] = targets["diagPaths"]
targets["queen"]["paths"]  = targets["allPaths"]
targets["q_w"]  = targets["q_b"] = targets["queen"]
targets["k_w"]  = targets["k_b"] = targets["king"]
targets["r_w"]  = targets["r_b"] = targets["rook"]
targets["b_w"]  = targets["b_b"] = targets["bishop"]
targets["n_w"]  = targets["n_b"] = targets["knight"]
targets["p_w"],targets["p_w!"]   = targets["wpawn"],targets["wptake"] 
targets["p_b"],targets["p_b!"]   = targets["bpawn"],targets["bptake"]  


for r,c in positions:
    targets[(r,c)] = defaultdict(list)
    for direction in targets["allPaths"]:
        path = targets[direction][r,c]
        for i,(tr,tc) in enumerate(path):
            targets[(r,c)][tr,tc]=path[:i]

def lineOfSight(board,A,B,ignore=None): 
    return all(board[c][r]=="" or (c,r)==ignore for c,r in targets[A][B])

def getKingPos(board,player):
    king = "k_"+player
    return [(c,r) for c,r in positions if board[c][r]==king][0]

def isCheck(board,player,kingPos=None,ignore=None):
    paths = ("q_b","r_b","b_b","n_b",f"p_{player}!")
    if kingPos is None: kingPos = getKingPos(board,player)
    return any( board[c][r][:1]==path[:1]
                and board[c][r][-1:] != player
                and lineOfSight(board,kingPos,(c,r),ignore)
                for path in paths
                for c,r in targets[path][kingPos] )


# { pinnedPosition : pinnedByPosition }
def getPinned(board,player):
    kingPos  = getKingPos(board,player)
    pinned   = dict()
    for path in targets["allPaths"]:
        inLine = ((c,r) for c,r in targets[path][kingPos] if board[c][r])
        pc,pr = next(inLine,(None,None)) # own piece
        if pc is None or board[pc][pr][-1:] != player: continue
        ac,ar = next(inLine,(None,None)) # opponent attacker
        if ac is None or board[ac][ar][-1:] == player: continue
        aPiece = board[ac][ar][:1]
        if aPiece == "q" \
        or aPiece == "r" and (ac == pc or  ar == pr) \
        or aPiece == "b" and (ac != pc and ar != pr):
            pinned[pc,pr] = (ac,ar) 
    return pinned

def linearMoves(board,position,player,piece):
    for path in targets[piece]["paths"]:
        for c,r in targets[path][position]:
            if board[c][r][-1:] != player : yield (position,(c,r))
            if board[c][r]      != ""     : break

def directMoves(board,position,player,piece,condition=lambda *p:True):
    for c,r in targets[piece][position]:
        if board[c][r][-1:] == player: continue
        if condition(c,r): yield (position,(c,r))

def switch(v): yield lambda *c: v in c

def getMoves(board,player):
    enPassant,brokenCastles = board[8:] or (None,set())
    moves = []
    for c,r in positions:
        if board[c][r][-1:] != player: continue
        piece = board[c][r]
        for case in switch(piece[0]):
            if   case("b","r","q"):
                moves += linearMoves(board,(c,r),player,piece)
            elif case("n"):
                moves += directMoves(board,(c,r),player,piece)                
            elif case("p"):
                moves += directMoves(board,(c,r),player,piece,
                         lambda tc,tr:board[tc][tr]==""
                            and lineOfSight(board,(c,r),(tc,tr)))
                moves += directMoves(board,(c,r),player,piece+"!",
                         lambda tc,tr:board[tc][tr] != "" or (tc,tr) == enPassant )
            elif case("k"):
                moves += directMoves(board,(c,r),player,piece,
                         lambda tc,tr: not isCheck(board,player,(tc,tr),(c,r)))
                if isCheck(board,player): continue
                moves += directMoves(board,(c,r),player,player+"castle",
                         lambda tc,tr: board[tc][tr] == ""
                            and not (tc,tr) in brokenCastles
                            and lineOfSight(board,(c,r),(tc,tr))
                            and not isCheck(board,player,(tc,tr),(c,r))
                            and not isCheck(board,player,targets[c,r][tc,tr][0],(c,r)))        
    pinned = getPinned(board,player)
    if pinned:   # Pinned pieces can only move on the threat line
        kingPos = getKingPos(board,player)
        moves   = [ (p,t) for p,t in moves if p not in pinned
                    or t == pinned[p] or t in targets[kingPos][pinned[p]] ]
    return moves
        

def playMove(board,fromPosition,toPosition,promotion="q"):
    (fromC,fromR),(toC,toR) = fromPosition,toPosition
    piece,player = board[fromC][fromR].split("_")
    board = [deepcopy(r) for r in board]
    g.takenPiece = ''
    if board[toC][toR]: # capture
        g.takenPiece = board[toC][toR]
    board[toC][toR],board[fromC][fromR] = board[fromC][fromR],""
    
    # promotion
    if piece == "p" and toR in (0,7):            
        piece = promotion
        board[toC][toR] = piece+"_"+player
        
    # en passant
    enPassant,brokenCastles = board[8:] or (None,set())
    if piece=="p" and toPosition == enPassant:
        g.takenPiece = board[toC][fromR]
        board[toC][fromR] = ""
    enPassant = next(iter(targets[fromPosition][toPosition]*(piece=="p")),None)
    
    # castle    
    if piece=="k" and abs(toC-fromC)>1:
        rookFrom = ((fromC<toC)*7,fromR)
        rookTo   = targets[fromPosition][toPosition][0]
        board    = playMove(board, rookFrom,rookTo) 
    brokenCastles   = brokenCastles.union(targets["breakCastle"][fromPosition])
    
    board[8:]    = (enPassant,brokenCastles)    
    return board
