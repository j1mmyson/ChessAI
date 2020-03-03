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
    os.system('clear')
    print(board)

    if board.is_game_over() is True:
        os.system('clear')
        print(board)
        break

    legal_list = []
    for i in board.legal_moves:
        legal_list.append(str(i))
    rmove = chess.Move.from_uci(random.choice(legal_list))
    board.push(rmove)
    # time.sleep(0.5)

    send(clientSock, str(rmove))
    os.system('clear')
    print(board)
    if board.is_game_over() is True:
        os.system('clear')
        print(board)
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
