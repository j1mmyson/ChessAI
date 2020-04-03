import chess
import random
import os
import time
import pickle
import sys


BOLD = '\033[1m'
CEND = '\033[0m'
CRED = '\033[31m'
CGRAY = '\033[90m'


class LinkedList:
    class Node:
        def __init__(self, move, prev):
            self.move = move
            self.reward = 0.5
            self.prev = prev
            self.next = []

    def __init__(self):
        self.head = self.Node(None, None)
        self.size = 0

    def insert(self, move, p):
        new_node = self.Node(move, p)
        p.next.append(new_node)
        self.size += 1


# board.move_stack을 사용, 마지막 움직임 출력
# def last_move():
#     move_list=[]
#     for i in board.move_stack:
#         move_list.append(str(i))
#     if len(move_list) > 0 :
#         print('\nmove: %s'%(move_list[-1]))


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
    # last_move()

    # # 누적 잡은 말 출력
    # for i in range(12):
    #     if piece[i][1] >= 1:
    #         print('%s: %d'%(piece[i][0],piece[i][1]))


# 잡은 말 count
def captured_count(before_board, after_board):
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
            if (sum(before_list) > sum(after_list)):
                piece[i][1]+=1


sys.setrecursionlimit(10000)
chess_model = LinkedList()
current_node = chess_model.head
accumulated_board = 0
piece_list = ['p','r','n','b','q','k','P','R','N','B','Q','K']
piece = []
for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0]= piece_list[i]


# main
for i in range(10):
    board = chess.Board()
    floor = 0
    os.system('clear')
    display()

    while True:
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))

        epsilon = 0.9999**accumulated_board # epsilon의 확률로 랜덤, 0.9999^x 곡선으로 epsilon 변화

        # epsilon의 확률로 랜덤
        random_value = random.random()
        if epsilon <= random_value: # 랜덤 선택
            if len(current_node.next) == 0:  # next가 비어있는 경우 랜덤
                random_move = random.choice(legal_list)
                chess_model.insert(random_move, current_node)
                current_node = current_node.next[0]
                selected_move = chess.Move.from_uci(current_node.move)
            else:  # reward가 가장 큰 노드 선택
                next_node = current_node.next[0]
                for i in current_node.next:
                    if next_node.reward < i.reward:
                        next_node = i
                current_node = next_node
                selected_move = chess.Move.from_uci(current_node.move)

        else:
            if len(current_node.next) == 0:  # next가 비어있는 경우 랜덤
                random_move = random.choice(legal_list)
                chess_model.insert(random_move, current_node)
                current_node = current_node.next[0]
                selected_move = chess.Move.from_uci(current_node.move)
            else:
                random_move = random.choice(legal_list)
                find = 0
                for i in current_node.next:
                    if random_move == i.move:
                        find = 1
                        current_node = i
                        break
                if find == 0:
                    chess_model.insert(random_move, current_node)
                    current_node = current_node.next[-1]
                selected_move = chess.Move.from_uci(current_node.move)

        before_board = str(board)
        board.push(selected_move)
        floor += 1
        after_board = str(board)
        captured_count(before_board, after_board)

        os.system('clear')
        display()

        print(epsilon)

        if board.is_game_over() is True:
            break

    my_floor = floor
    while True:
        if board.result() == "1/2-1/2":
            winning_point = 0.5
        else:
            winning_point = 1

        # print("winning_point = " + str(winning_point))
        if my_floor%2 == floor%2:
            current_node.reward = current_node.reward*2/3 + winning_point*(my_floor/floor)/3
        else:
            current_node.reward = current_node.reward*2/3 + (1-winning_point)*(my_floor/floor)/3

        my_floor -= 1
        print(str(current_node.reward))
        current_node = current_node.prev
        if current_node.prev is None:
            break

    accumulated_board += 1

with open('data.pickle', 'wb') as f:
    pickle.dump(chess_model, f, pickle.HIGHEST_PROTOCOL)

print()
print(accumulated_board)