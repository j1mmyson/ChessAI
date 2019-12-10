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

    for i in range(len(before_board)):
        for j in range(len(piece_list)):
            if piece_list[j] is before_board[i]:
                before_list[j] += 1

    for i in range(len(after_board)):
        for j in range(len(piece_list)):
            if piece_list[j] is after_board[i]:
                after_list[j] += 1

    for i in range(len(before_list)):
        if before_list[i] > after_list[i]:
            piece[i][1]+=1


port = 8080
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)
print('%d : LOADING...' % port)
connectionSock, addr = serverSock.accept()
print('CONNECTED in ', str(addr))

board = chess.Board()
piece_list = ['p','r','n','b','q','k','P','R','N','B','Q','K']
piece = []
for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0]= piece_list[i]

beforeBoard = str(board)
os.system('clear')
display()
while True:
    legal_list = []
    for i in board.legal_moves:
        legal_list.append(str(i))
    rmove = chess.Move.from_uci(random.choice(legal_list))
    board.push(rmove)

    afterBoard = str(board)
    capturedCount(beforeBoard, afterBoard)

    os.system('clear')
    display()

    send(connectionSock, str(rmove))
    beforeBoard = afterBoard
    if board.is_game_over() is True:
        break

    receive(connectionSock)
    afterBoard = str(board)
    os.system('clear')
    display()
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
