import chess
import random
import os
import time


BOLD = '\033[1m'
CEND = '\033[0m'
CRED = '\033[31m'
CGRAY = '\033[90m'


# board.move_stack을 사용, 마지막 움직임 출력
def lastMove():
    moveList=[]
    for i in board.move_stack:
        moveList.append(str(i))
    if len(moveList) > 0 :
        print('\nmove: %s'%(moveList[-1]))


# display
def display():
    reboard = str(board)
    for i in range(len(reboard)):
        if reboard[i].islower() is True:
            print(CRED+BOLD+reboard[i]+CEND, end='')
        elif reboard[i].islower() is False:
            print(reboard[i], end='')
        else:
            print(CGRAY+BOLD+reboard[i]+CEND, end='')
    print()
    lastMove()

    # 누적 잡은 말 출력
    for i in range(12):
        if piece[i][1] >= 1:
            print('%s: %d'%(piece[i][0],piece[i][1]))


# 잡은 말 count
def capturedCount(before_board, after_board):
    before_list=[0]*12 
    after_list=[0]*12

    for i in range(len(before_board)):
        for j in range(len(pieceList)):
            if pieceList[j] is before_board[i]:
                before_list[j] += 1

    for i in range(len(after_board)):
        for j in range(len(pieceList)):
            if pieceList[j] is after_board[i]:
                after_list[j] += 1

    for i in range(len(before_list)):
        if before_list[i] > after_list[i]:
            if (sum(before_list) > sum(after_list)):
                piece[i][1]+=1 


board = chess.Board()
pieceList = ['p','r','n','b','q','k','P','R','N','B','Q','K']
piece = []
for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0]= pieceList[i]

os.system('clear')
display()

epsilon = 0.7 # epsilon의 확률로 랜덤
randomValue = random.random()

while True:
    legalList = []
    for i in board.legal_moves:
        legalList.append(str(i))

    # epsilon의 확률로 랜덤
    if epsilon <= randomValue:
        selectedMove = chess.Move.from_uci(random.choice(legalList))
    else:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        selectedMove = chess.Move.from_uci(random.choice(legalList))

    beforeBoard = str(board)
    board.push(selectedMove)
    afterBoard = str(board)
    capturedCount(beforeBoard, afterBoard)

    os.system('clear')
    display()

    if board.is_game_over() is True:
        print()
        print(board.result())
        if board.result() == "1-0":
            print('\nWHITE win\n')
            break
        elif board.result() == "0-1":
            print('\nBLACK win\n')
            break
        elif board.result() == "1/2-1/2":
            print('\nDraw!\n')
            break