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
    (현재 상태함수값, 혹은 현재상태의 reward를 구하는것이 위 세가지 방법이 아닐수도?
    아니라면 어떤 방법으로 현재의 상태함수값, reward를 구할지 생각해보아야함.)

    미래에 체크메이트를 할 수 있는 수라면 +? 반대로 체크메이트를 당할 미래라면 -?
    minmax알고리즘을 통해 미래의 상대의 수 까지 어느정도 예측이 가능할수도?
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
    (이때 기억이라는 것이 새 파일을 만들어서 테이블을 만들어야 하는것인지 아니면 다른 방법이 있는지 알아보아야함.)
    특정 정책에 따라 가치가 높은 행동을 취할지, 새로운 탐험을 할지 정해준다.
    특정행동의 가치함수값이 낮다면 그 노드에 대해서는 깊게 탐험해보지 않는다.=>시간절약?

    행동이라는것이 다음상태의 reward, 가치함수값을 알면 되는것인가?? 
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
