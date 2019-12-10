import chess
import random
import os
import time
from socket import *


BOLD = '\033[1m'
CEND = '\033[0m'
CRED = '\033[31m'
CGRAY = '\033[90m'


def send(sock, move):
    sendData = move
    sock.send(sendData.encode('utf-8'))


def receive(sock):
    recvData = sock.recv(1024)
    decodeMove = recvData.decode('utf-8')
    board.push(chess.Move.from_uci(decodeMove))


# board.move_stack을 사용, 마지막 움직임 출력
def moveStackList():
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
    moveStackList()

    # p,r,n,b,q,k,P,R,N,B,Q,K = 0
    for i in range(12):
        if piece[i][1] >= 1:
            print('%s: %d'%(piece[i][0],piece[i][1]))


# 잡은 말 count
def capturedCount(before_board, after_board):
    before_list=[0]*12 
    after_list=[0]*12

    for i in before_board:
        if i is 'p':
            before_list[0] += 1
        elif i is 'r':
            before_list[1] += 1
        elif i is 'n':
            before_list[2] += 1
        elif i is 'b':
            before_list[3] += 1
        elif i is 'q':
            before_list[4] += 1
        elif i is 'k':
            before_list[5] += 1
        elif i is 'P':
            before_list[6] += 1
        elif i is 'R':
            before_list[7] += 1
        elif i is 'N':
            before_list[8] += 1
        elif i is 'B':
            before_list[9] += 1
        elif i is 'Q':
            before_list[10] += 1
        elif i is 'K':
            before_list[11]+=1
        else:
            continue

    for i in after_board:
        if i is 'p':
            after_list[0] += 1
        elif i is 'r':
            after_list[1] += 1
        elif i is 'n':
            after_list[2] += 1
        elif i is 'b':
            after_list[3] += 1
        elif i is 'q':
            after_list[4] += 1
        elif i is 'k':
            after_list[5] += 1
        elif i is 'P':
            after_list[6] += 1
        elif i is 'R':
            after_list[7] += 1
        elif i is 'N':
            after_list[8] += 1
        elif i is 'B':
            after_list[9] += 1
        elif i is 'Q':
            after_list[10] += 1
        elif i is 'K':
            after_list[11]+=1  
        else:
            continue

    for i in range(len(before_list)):
        if before_list[i] > after_list[i]:
            piece[i][1]+=1


port = 8080
clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', port))
print('CONNECTED')

board = chess.Board()
piece_list = ['p','r','n','b','q','k','P','R','N','B','Q','K']
piece = []
for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0]= piece_list[i]

beforeBoard = str(board)
while True:
    receive(clientSock)
    afterBoard = str(board)
    os.system('clear')
    display()
    if board.is_game_over() is True:
        break

    legal_list = []
    for i in board.legal_moves:
        legal_list.append(str(i))
    rmove = chess.Move.from_uci(random.choice(legal_list))
    board.push(rmove)

    afterBoard = str(board)
    capturedCount(beforeBoard, afterBoard)

    os.system('clear')
    display()

    send(clientSock, str(rmove))
    beforeBoard = afterBoard
    if board.is_game_over() is True:
        break


if board.is_game_over() is True:
    # print(board.result())
    if board.result() is '1-0':
        print('\nWHITE win\n')
    elif board.result() is '0-1':
        print('\nBLACK win\n')
    else:
        print('\nDraw!\n')
