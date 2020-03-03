import chess
import os
import random
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
            if i.islower() is True:
                print(CRED+BOLD+i+CEND, "", end='')
            else:
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
print(" connect to white complete port number:", str(white_addr))

black_socket = socket(AF_INET, SOCK_STREAM)
black_socket.bind(('', black_port))
black_socket.listen(1)
print(" Connect to Black Player...")
black_connect, black_addr = black_socket.accept()
print(" connect to black complete port number:", str(black_addr))

turn = chess.WHITE
gameover = False
board = chess.Board()

print_board(board)

while True:
    if turn == chess.WHITE:
        '''
        Agent1 에게 현재의 State를 보내준다.
        Agent1은 상태를 받아 몬테카를로, 시간차학습, 살사 방법중 한가지의 방법으로
        현재상태의 가치함수값을 구하고 다음행동을 정한다.

        Alpha Zero의 경우 현재상태에서 가능한 미래의 시나리오를 플레이하고 좋은경로에 대해 우선순위를 두면서,
        동시에 다른 플레이어가 어떻게 반응할지를 생각하며, 아직 모르는 수들도 탐험해본다.
        처음보는 상태를 마주하면 그 상태를 평가하고 그렇게 평가된 점수를 이전의 수들의 가치함수에도 반영을 한다.

        미래의 가능성에 대한 생각이 끝나면 가장 많이 탐험한(우선순위가 높은?)행동을 취한다.

        위 행동들은 각 에이전트의 코드부분에서 실행한다.
        이 코드는 각 상태를 두 에이전트에게 보내는 역할만 하면 됨.

        '''
        if board.move_stack == []:
            send(white_connect, 'start')
        white_move = receive(white_connect)
        board.push(chess.Move.from_uci(white_move))
        if board.is_game_over() is True:
            send(black_connect, white_move)
            os.system('clear')
            print_board(board)
            break
        send(black_connect, white_move)
        # time.sleep(0.5)
        turn = chess.BLACK
    else:
        '''
        Agent2도 Agent1과 같은 방법으로 행동을 정한다.
        '''
        black_move = receive(black_connect)
        board.push(chess.Move.from_uci(black_move))
        if board.is_game_over() is True:
            send(white_connect, black_move)
            os.system('clear')
            print_board(board)
            break
        send(white_connect, black_move)
        # time.sleep(0.5)
        turn = chess.WHITE
    os.system('clear')
    print_board(board)

if board.is_game_over() is True:
    '''
    경기가 끝나게되면 두 에이전트에게 결과를 전달하고
    reward 혹은 가치함수값을 갱신할수 있도록 한다.
    경기가 끝나면 로그를 남길 수 있도록 한다.
    (그리고 아직 해결하지못한 어떻게 얘네둘이서 우리가 코드를 계속 실행시켜주지않아도
    알아서 계속 플레이하며 학습할 수 있을지 그 방법도 생각해 봐야할듯??
    이 코드를 버리고 다른 구조의 코드를 새로 짜서 학습 자동화를 해보는 것도 생각해봐야할듯??)
    '''
    print(board.result())
    if board.result() == "1-0":
        print('\nWHITE win\n')
    elif board.result() == "0-1":
        print('\nBLACK win\n')
    elif board.result() == "1/2-1/2":
        print('\nDraw!\n')
