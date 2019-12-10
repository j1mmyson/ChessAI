import chess
import os
import random
import time
from socket import *


def send(sock, move):
    sendData = move
    sock.send(sendData.encode('utf-8'))


def receive(sock):
    recvData = sock.recv(1024)
    decodeMove = recvData.decode('utf-8')
    return decodeMove


def print_board(board):
    symbol = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    j = 7
    k = 0
    print("8"+"   ", end='')
    for i in board.board_fen():
        if i == '/':
            print()
            print(j, "  ", end='')
            j = j-1
        elif (i in symbol) is True:
            print(i, "", end='')
        else:
            for k in range(0, int(i)):
                print("- ", end='')
            k = 0
    print()
    print()
    print("    "+"a b c d e f g h")


# pick color randomly
if random.choice([1, 2]) is 1:
    p1_turn = True
    p2_turn = False
    white_port = 8080
    black_port = 8081
else:
    p2_turn = True
    p1_turn = False
    white_port = 8081
    black_port = 8080

# connect model1 - engine - model2
# p1's port = 8080 // p2's port = 8081

white_socket = socket(AF_INET, SOCK_STREAM)
white_socket.bind(('', white_port))
white_socket.listen(1)
print(" Connect to White Player...")
white_connect, white_addr = white_socket.accept()
print(" connect to white complete prot number:", str(white_addr))

black_socket = socket(AF_INET, SOCK_STREAM)
black_socket.bind(('', black_port))
black_socket.listen(1)
print(" Connect to Black Player...")
black_connect, black_addr = black_socket.accept()
print(" connect to black complete prot number:", str(black_addr))

turn = chess.WHITE
gameover = False
board = chess.Board()

print_board(board)

while board.is_game_over() is False:
    if turn == chess.WHITE:
        if board.move_stack == []:
            send(white_connect, 'start')
        white_move = receive(white_connect)
        board.push(chess.Move.from_uci(white_move))
        send(black_connect, white_move)
        time.sleep(1)
        turn = p2_turn
    else:
        black_move = receive(black_connect)
        board.push(chess.Move.from_uci(black_move))
        send(white_connect, black_move)
        time.sleep(1)
        turn = p1_turn
    os.system('clear')
    print_board(board)

if board.is_game_over() is True:
    # print(board.result())
    if board.result() is '1-0':
        print('\nWHITE win\n')
    elif board.result() is '0-1':
        print('\nBLACK win\n')
    else:
        print('\nDraw!\n')
