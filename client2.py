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


port = 8081

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', port))

print('CONNECTED')

board = chess.Board()

while True:
    receive(clientSock)
    if board.is_game_over() is True:
        break

    os.system('clear')
    print(board)

    legal_list = []
    for i in board.legal_moves:
        legal_list.append(str(i))
    rmove = chess.Move.from_uci(random.choice(legal_list))
    board.push(rmove)
    # time.sleep(0.5)

    os.system('clear')
    print(board)
    send(clientSock, str(rmove))
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
