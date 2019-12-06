import chess
import random
import os
import time
from socket import *

board = chess.Board()

def send(sock, move):
    sendData = move
    sock.send(sendData.encode('utf-8'))

def receive(sock):
    recvData = sock.recv(1024)
    decodeMove = recvData.decode('utf-8')
    board.push(chess.Move.from_uci(decodeMove))

port = 8080

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print('%d : LOADING...'%port)

connectionSock, addr = serverSock.accept()

print('CONNECTED in ', str(addr))

while board.is_game_over() is False:
    os.system('clear')
    print(board)

    legal_list = []
    for i in board.legal_moves:
        legal_list.append(str(i))
    rmove = chess.Move.from_uci(random.choice(legal_list))
    board.push(rmove)
    time.sleep(0.5)
    
    send(connectionSock, str(rmove))
    
    receive(connectionSock)

if board.is_game_over() is True:
    print(board.result())
