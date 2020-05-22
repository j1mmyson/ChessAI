import chess
import random
#import os
#import time
import pickle
import sys


BOLD = '\033[1m'
CEND = '\033[0m'
CRED = '\033[31m'
CGRAY = '\033[90m'
REPEAT = 100

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

def pre_order(node, new_state, current_node):
    if(node.state == new_state and node.state.turn == new_state.turn):
        current_node.next.append(node)
        return 100
    else:
        for i in node.next:
            pre_order(i, new_state, current_node)
    return 0

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


try:
    data = open('data.pickle', 'rb')
except FileNotFoundError:
    print("Make new List (Error: FileNotFoundError)")
    chess_model = LinkedList()
else:
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    chess_model = data

sys.setrecursionlimit(10000)
current_node = chess_model.head
piece_list = ['p','r','n','b','q','k','P','R','N','B','Q','K']
piece = []
for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0]= piece_list[i]

# main
for i in range(REPEAT):
    board = chess.Board()
    floor = 0

    while True:
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))

        if 0.99999**chess_model.accumulated_board >= 0.2:
            epsilon = 0.99999**chess_model.accumulated_board # epsilon의 확률로 랜덤, 0.99999^x 곡선으로 epsilon 변화
        else:
            epsilon = 0.2

        # epsilon의 확률로 랜덤
        random_value = random.random()
        
        if not current_node.next: # next가 비어있는 경우 랜덤
        #if len(current_node.next) == 0:  
            random_move = random.choice(legal_list)
            selected_move = chess.Move.from_uci(random_move)
            board.push(selected_move)
                
            state = board
            search_result = pre_order(chess_model.head, state, current_node)

            if search_result is 100:
                current_node = current_node.next[-1]
            else:
                chess_model.insert(random_move, current_node, state)
                current_node = current_node.next[-1]

        elif epsilon <= random_value: # 최선의 수 선택
            current_node = current_node[0]
            selected_move = chess.Move.from_uci(current_node.move)
            board.push(selected_move)

        else: # 탐험
            random_move = random.choice(legal_list)
            find = False
            for i in current_node.next:
                if random_move == i.move:
                    find = True
                    break
            if find is True:
                current_node = i
                selected_move = chess.Move.from_uci(current_node.move)
                board.push(selected_move)
            else:
                selected_move = chess.Move.from_uci(random_move)
                board.push(selected_move)
                
                state = board
                search_result = pre_order(chess_model.head, state, current_node)

                if search_result is 100:
                    current_node = current_node.next[-1]
                else:
                    chess_model.insert(random_move, current_node, state)
                    current_node = current_node.next[-1]

        floor += 1

        if board.is_game_over() is True:
            break

    my_floor = floor

    if board.result() == "1/2-1/2":
        winning_point = 0.5
    else:
        winning_point = 1

    while True:
        before_reward = 0
        if my_floor%2 == floor%2:
            before_reward = current_node.reward
            current_node.reward = current_node.reward*2/3 + winning_point*(my_floor/floor)/3
        else:
            before_reward = current_node.reward
            current_node.reward = current_node.reward*2/3 + (1-winning_point)*(my_floor/floor)/3

        if current_node.prev.next[0] == current_node and before_reward-current_node.reward > 0:
            max_reward = current_node.reward
            for i in current_node.prev.next:
                if max_reward < i.reward:
                    tmp = i
                    i = current_node
                    current_node = tmp
        elif current_node.reward > current_node.prev.next[0].reward and before_reward-current_node.reward < 0:
            tmp = current_node
            current_node = current_node.prev.next[0]
            current_node.prev.next[0] = tmp

        my_floor -= 1
        current_node = current_node.prev
        if current_node.prev is None:
            break

    chess_model.accumulated_board += 1
    # print(str(chess_model.accumulated_board))
    if chess_model.accumulated_board%100 == 0:
        log = open("log.txt", 'a')
        log.write(str(chess_model.accumulated_board)+"\n")
        log.close()
        

with open('data.pickle', 'wb') as f:
    pickle.dump(chess_model, f, pickle.HIGHEST_PROTOCOL)
