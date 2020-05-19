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
        def __init__(self, move, prev, state):
            self.move = move
            self.reward = 0.5
            self.prev = prev
            self.next = []
            self.state = state

    def __init__(self):
        self.head = self.Node(None, None, None)
        self.size = 0
        self.accumulated_board = 0

    def insert(self, move, p, state):
        new_node = self.Node(move, p, state)
        p.next.append(new_node)
        self.size += 1


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


# 잡은 말 count
def captured_count(before_board, after_board):
    before_list = [0]*12
    after_list = [0]*12

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
                piece[i][1] += 1


try:
    data = open('bw.pickle', 'rb')
except FileNotFoundError:
    print("Make new List (Error: FileNotFoundError)")
    chess_model = LinkedList()
else:
    with open('bw.pickle', 'rb') as f:
        data = pickle.load(f)
    chess_model = data

sys.setrecursionlimit(10000)
current_node = chess_model.head
piece_list = ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']
piece = []
floor = 0
repeat = 200000
for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0] = piece_list[i]

# main
for i in range(REPEAT):
    board = chess.Board()
    floor = 0

    while True:
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))

        if 0.99999**chess_model.accumulated_board >= 0.2:
            epsilon = 0.99999**chess_model.accumulated_board  # epsilon의 확률로 랜덤, 0.9999^x 곡선으로 epsilon 변화
        else:
            epsilon = 0.2

        # epsilon의 확률로 랜덤
        random_value = random.random()
        state = str(board)
        if epsilon <= random_value:  # greedy
            if len(current_node.next) == 0:  # next가 비어있는 경우 랜덤
                random_move = random.choice(legal_list)
                chess_model.insert(random_move, current_node, state)
                current_node = current_node.next[0]
                selected_move = chess.Move.from_uci(current_node.move)
            else:  # reward가 가장 큰 노드 선택
                next_node = current_node.next[0]
                for i in current_node.next:
                    if next_node.reward < i.reward:
                        next_node = i
                current_node = next_node
                selected_move = chess.Move.from_uci(current_node.move)

        else:  # random
            if len(current_node.next) == 0:  # next가 비어있는 경우 랜덤
                random_move = random.choice(legal_list)
                chess_model.insert(random_move, current_node, state)
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
                    chess_model.insert(random_move, current_node, state)
                    if current_node.next[0].reward < current_node.next[-1].reward:  # 새로만든 노드의 reward가 더 크면 자리바꿈
                        temp = current_node.next[0]
                        current_node.next[0] = current_node.next[-1]
                        current_node.next[-1] = temp
                        current_node = current_node.next[0]
                    else:
                        current_node = current_node.next[-1]
                selected_move = chess.Move.from_uci(current_node.move)

        before_board = str(board)
        board.push(selected_move)
        floor += 1
        after_board = str(board)
        captured_count(before_board, after_board)

        if board.is_game_over() is True:
            break

    my_floor = floor

    if board.result() == "1/2-1/2":
        winning_point = 0.5
    else:
        winning_point = 1

    while True:
        if my_floor % 2 == floor % 2:
            current_node.reward = current_node.reward*2/3 + winning_point*(my_floor/floor)/3
            if current_node.reward > current_node.prev.next[0].reward:
                temp = current_node
                current_node = current_node.prev.next[0]
                current_node.prev.next[0] = temp
        else:
            current_node.reward = current_node.reward*2/3 + (1-winning_point)*(my_floor/floor)/3
            if current_node.reward > current_node.prev.next[0].reward:
                temp = current_node
                current_node = current_node.prev.next[0]
                current_node.prev.next[0] = temp

        my_floor -= 1
        current_node = current_node.prev
        if current_node.prev is None:
            break

    chess_model.accumulated_board = chess_model.accumulated_board+1
    # print(str(chess_model.accumulated_board))
    if chess_model.accumulated_board % 100 == 0:
        log = open("bwlog.txt", 'a')
        log.write(str(chess_model.accumulated_board)+"\n")
        log.close()


with open('bw.pickle', 'wb') as f:
    pickle.dump(chess_model, f, pickle.HIGHEST_PROTOCOL)
    f.close()
