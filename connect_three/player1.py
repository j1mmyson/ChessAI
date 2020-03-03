import chess
import random
import os
import time
from socket import *


def send(sock, move):
    sendData = move
    sock.send(sendData.encode('utf-8'))


def receive(sock):
    recvData = sock.recv(1024)
    decodeMove = recvData.decode('utf-8')
    if decodeMove != 'start':
        board.push(chess.Move.from_uci(decodeMove))


port = 8080

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', port))

print('CONNECTED')

board = chess.Board()

while True:
    receive(clientSock)
    os.system('clear')
    print(board)
    '''
    현재 상태를 받아와 현재상태가 얼마나 유리한지 구해준다.
    몬테카를로, 시간차학습, 살사 방법중 택1?
    '''

    if board.is_game_over() is True:
        '''
        경기가 끝났다면 에이전트의 승패에 따라 reward 혹은 가치함수값들을 갱신해준다.
        '''
        os.system('clear')
        print(board)
        break


    legal_list = []
    '''
    현재 상태(Board)에서의legal_list만큼의 행동을 취할 수 있으며
    탐험을 해보았던 행동들에 대해서는 그 행동의 reward 혹은 가치함수 값을 기억한다.
    특정 정책에 따라 가치가 높은 행동을 취할지, 새로운 탐험을 할지 정해준다.
    특정행동의 가치함수값이 낮다면 그 노드에 대해서는 깊게 탐험해보지 않는다.=>시간절약?
    
    '''
    for i in board.legal_moves:
        legal_list.append(str(i))
    rmove = chess.Move.from_uci(random.choice(legal_list))
    board.push(rmove)
    # time.sleep(0.5)

    '''
    해당 에이전트가 정한 행동을 engine에게 보낸다.
    '''
    send(clientSock, str(rmove))
    os.system('clear')
    print(board)
    if board.is_game_over() is True:
        os.system('clear')
        print(board)
        print("fin!")
        break

if board.is_game_over() is True:
    # print(board.result())
    os.system('clear')
    print(board)
    if board.result() == '1-0':
        print('\nWHITE win\n')
    elif board.result() == '0-1':
        print('\nBLACK win\n')
    else:
        print('\nDraw!\n')
