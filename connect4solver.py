import heapq
import numpy
import matplotlib.pyplot
import time
import os

def move(board, column, player):
    board = numpy.copy(board)
    row = -1
    for i in range(5,-1,-1):
        if board[i][column] == 0:
            board[i][column] = player
            row = i
            break
    if verticalCheck(board,row,column) >= 4 or horizontalCheck(board,row,column) >= 4 or diagonalCheck(board,row,column) >= 4 or diagonalCheck2(board,row,column) >= 4:
        return player, board, row
    if drawCheck(board):
        return -1, board, row
    return 0, board, row

def verticalCheck(board,row,col):
    count = 1
    player = board[row][col]
    for i in range(row+1,6,1):
        if board[i][col] == player:
            count+=1
        else:
            break
    for i in range(row-1,-1,-1):
        if board[i][col] == player:
            count+=1
        else:
            break
    return count
def horizontalCheck(board,row,col):
    count = 1
    player = board[row][col]
    for i in range(col+1,7,1):
        if board[row][i] == player:
            count+=1
        else:
            break
    for i in range(col-1,-1,-1):
        if board[row][i] == player:
            count+=1
        else:
            break
    return count
def diagonalCheck(board,row,col):
    count = 1
    player = board[row][col]
    for i in range(1, min(7-col,6-row), 1):
        if board[row+i][col+i] == player:
            count+=1
        else:
            break
    for i in range(1, min(col+1,row+1), 1):
        if board[row-i][col-i] == player:
            count+=1
        else:
            break
    return count
def diagonalCheck2(board,row,col):
    player = board[row][col]
    count = 1
    for i in range(1, min(7-col,row+1), 1):
        if board[row-i][col+i] == player:
            count+=1
        else:
            break
    for i in range(1, min(col+1,6-row), 1):
        if board[row+i][col-i] == player:
            count+=1
        else:
            break
    return count

def verticalSpaceCheck(board,row,col):
    count = 1
    player = board[row][col]
    for i in range(row+1,6,1):
        if board[i][col] == player or board[i][col] == 0:
            count+=1
        else:
            break
    for i in range(row-1,-1,-1):
        if board[i][col] == player or board[i][col] == 0:
            count+=1
        else:
            break
    return count
def horizontalSpaceCheck(board,row,col):
    count = 1
    player = board[row][col]
    for i in range(col+1,7,1):
        if board[row][i] == player or board[row][i] == 0:
            count+=1
        else:
            break
    for i in range(col-1,-1,-1):
        if board[row][i] == player or board[row][i] == 0:
            count+=1
        else:
            break
    return count
def diagonalSpaceCheck(board,row,col):
    count = 1
    player = board[row][col]
    for i in range(1, min(7-col,6-row), 1):
        if board[row+i][col+i] == player or board[row+i][col+i] == 0:
            count+=1
        else:
            break
    for i in range(1, min(col+1,row+1), 1):
        if board[row-i][col-i] == player or board[row-i][col-i] == 0:
            count+=1
        else:
            break
    return count
def diagonalSpaceCheck2(board,row,col):
    player = board[row][col]
    count = 1
    for i in range(1, min(7-col,row+1), 1):
        if board[row-i][col+i] == player or board[row-i][col+i] == 0:
            count+=1
        else:
            break
    for i in range(1, min(col+1,6-row), 1):
        if board[row+i][col-i] == player or board[row+i][col-i] == 0:
            count+=1
        else:
            break
    return count

def drawCheck(board):
    for i in range(0,6):
        for j in range(0,7):
            if board[i][j] == 0:
                return False
    return True

def alphaBetaSearch(result, player, state, limit):
    value, move = maxValue(result,player,state, float('-inf'),float('inf'),limit,0)
    return move

def maxValue(result, player, state, a, b, recursionLimit, recursionCount):
    if result != 0:
        if player == result:
            return 1000,None
        elif result == -1:
            return 0,None
        else:
            return -1000,None
    if recursionCount > recursionLimit:
        return eval(state,player),None
    v = float('-inf')
    m = None
    for act in actions(state):
        result, board,t = move(state,act,player)
        v2, a2 = minValue(result, player, board, a, b, recursionLimit, recursionCount+1)
        if v2 > v:
            v, m = v2, act
            a = max(a,v)
        if v >= b:
            return v,m
    return v,m

def minValue(result, player, state, a, b, recursionLimit, recursionCount):
    if result != 0:
        if player == result:
            return 1000,None
        elif result == -1:
            return 0,None
        else:
            return -1000,None
    if recursionCount > recursionLimit:
        return eval(state,player),None
    v = float('inf')
    m = None
    for act in actions(state):
        p = 1
        if player == 1:
            p = 2
        result, board,t = move(state,act,p)
        v2, a2 = maxValue(result, player, board, a, b, recursionLimit, recursionCount+1)
        if v2 < v:
            v, m = v2, act
            b = min(b,v)
        if v <= a:
            return v,m
    return v,m

def actions(board):
    for i in range(0,7):
        if board[0][i] == 0:
            yield i

def eval(board, player):
    p1total = 1
    p2total = 1
    for i in range(0,6):
        for j in range(0,7):
            if board[i][j] == 1:
                p1total+=pow(10,horizontalCheck(board,i,j))+pow(10,verticalCheck(board,i,j))+pow(10,diagonalCheck(board,i,j))+pow(10,diagonalCheck2(board,i,j))
                p1total+=(horizontalSpaceCheck(board,i,j)+verticalSpaceCheck(board,i,j)+diagonalSpaceCheck(board,i,j)+diagonalSpaceCheck2(board,i,j))/100
            elif board[i][j] == 2:
                p2total+=pow(10,horizontalCheck(board,i,j))+pow(10,verticalCheck(board,i,j))+pow(10,diagonalCheck(board,i,j))+pow(10,diagonalCheck2(board,i,j))
                p2total+=(horizontalSpaceCheck(board,i,j)+verticalSpaceCheck(board,i,j)+diagonalSpaceCheck(board,i,j)+diagonalSpaceCheck2(board,i,j))/100
    if player == 1:
        return (p1total-((p1total+p2total)/2))/((p1total+p2total)/2)*100
    else:
        return (p2total-((p1total+p2total)/2))/((p1total+p2total)/2)*100
    
def depthChart(turn):
    if turn <= 15:
        return 6
    elif turn <= 25:
        return 7
    elif turn <= 30:
        return 8
    elif turn <= 35:
        return 9
    elif turn <= 40:
        return 10
    elif turn <= 45:
        return 15
    else:
        return 20

class Node:
    def __init__(self,board,player,parent,terminal,C):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.wins = 0
        self.playouts = 0
        self.C = C
        self.remainingMoves = list(actions(board))
        self.actions = []
        self.terminal = terminal
    
    def uctScore(self):
        if self.playouts == 0:
            return float('inf')
        else:
            return (self.wins/self.playouts) + self.C*numpy.sqrt(numpy.log10(self.parent.playouts)/self.playouts)
        
    def bestChild(self):
        child = 0
        maxPlayouts = 0
        for i in self.children:
            if i.playouts > maxPlayouts:
                child = i
                maxPlayouts = i.playouts
        return child
    
    def bestChildUCT(self):
        child = 0
        maxScore = 0
        for i in self.children:
            if i.uctScore() > maxScore:
                child = i
                maxScore = i.uctScore()
        return child

def mcts(board, player, timeLimit,C, count):
    root = Node(board,player,None,0,C)
    t = time.time()
    while time.time()-t < timeLimit:
        node = select(root)
        child = expand(node)
        result = simulate(child)
        backPropagate(result, child)
    while node.parent != None:
        node = node.parent  
    return node.bestChild().actions[0]

def select(node):
    while node.remainingMoves == []:
        if node.children == []:
            return node
        node = node.bestChildUCT()
    return node


def expand(node):
    if node.remainingMoves:
        m = numpy.random.choice(node.remainingMoves)
        node.remainingMoves.remove(m)
        r,board,t = move(node.board,m,node.player)
        p = 1
        if node.player == 1:
            p = 2
        child = Node(board,p,node,node.terminal,node.C)
        if child.terminal == 0 and r != 0:
            child.terminal = r
        child.actions.append(m)
        node.children.append(child)
        return child
    return node
    
def simulate(child):
    if child.terminal != 0:
        return child.terminal
    playoutStyle = 1 # 1 for completely random, 2 for random until near terminal
    result = 0
    player = child.player
    board = child.board.copy()
    if playoutStyle == 1:
        while result == 0 and len(list(actions(board))) != 0:
            result, board,t = move(board,numpy.random.choice(list(actions(board))),player)
            if result != 0:
                break
            if player == 1:
                player = 2
            else:
                player = 1
        return result
    if playoutStyle == 2:
        while result == 0 and len(list(actions(board))) != 0:
            m = numpy.random.choice(list(actions(board)))
            for i in range(0,7):
                for p in range(0,2):
                    if move(board.copy(),i,p)[0] != 0:
                        m = i
                    
            result, board,t = move(board,m,player)
            if result != 0:
                break
            if player == 1:
                player = 2
            else:
                player = 1
        return result

def backPropagate(result, node):
    while node is not None:
        node.playouts+=1
        if result == -1:
            node.wins+=0.5
        elif result != node.player:
            node.wins+=1
        node = node.parent

board = numpy.zeros((6,7))
print(board)
result = 0
turn = 0
while result == 0:
    col = int(input("Pick a column (1-7)"))
    result,board,t = move(board,col-1, turn%2+1)
    turn+=1
    print(board)
    if result != 0:
        break
    #result,board,t = move(board,alphaBetaSearch(result,(turn%2)+1,board,depthChart(turn)), turn%2+1)
    result,board,t = move(board,mcts(board,turn%2+1,5,1.5,(turn+1)//2), turn%2+1)
    turn+=1
    print(board)

print("Game Over")
print("Player "+str(result)+" wins")
