import chess
import random
import pickle
import sys
import os
import time

BOLD = '\033[1m'
CEND = '\033[0m'
CRED = '\033[31m'
CGRAY = '\033[90m'
REPEAT = 1

class LinkedList:
    class Node:
        def __init__(self, move, state):
            self.move = move
            self.reward = 0.5
            self.next = []
            self.state = state

    def __init__(self):
        self.head = self.Node(None, None)
        self.search_list = []
        self.size = 0
        self.accumulated_board = 0

    def insert(self, move, p, state):
        new_node = self.Node(move, state)
        p.next.append(new_node)
        self.search_list.append(new_node)
        self.size += 1

    def search(self, new_state, current_node):
        for i in self.search_list:
            if(str(i.state) == str(new_state) and i.state.turn == new_state.turn):
                current_node.next.append(i)
                return True
        return False

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

print("data load start\n\n")

with open('data.pickle', 'rb') as f:
    chess_model = pickle.load(f)

sys.setrecursionlimit(10**7)
current_node = chess_model.head

# model's win rate
win = 0
lose = 0
draw = 0
no_data = 0
play_rand = 0
max = 0
min = 100
rand_num = 0
floor = 0
floor_sum = 0
floor_list = []
grd_list = []

# main
for i in range(REPEAT):
    print(str(i))
    turn = chess.WHITE
    board = chess.Board()
    current_node = chess_model.head
    floor = 0
    rand_num = 0
    play_rand = 0

    while True:
        # os.system('clear')
        display()

        if turn is chess.WHITE:
            legal_list = []
            for i in board.legal_moves:
                legal_list.append(str(i))

            while True:
                print('you can choose>> \n'+str(legal_list))
                user_move = input("enter the move(like 'e2e4'): ")
                if user_move not in legal_list:
                    print(CRED+"You make the wrong choice. Retry"+CEND)
                else:
                    break

            find = 0
            if play_rand == 0:
                for i in current_node.next:
                    if str(user_move) == i.move:
                        find = 1
                        current_node = i
                if find == 0:
                    no_data = no_data + 1
                    play_rand = 1

            board.push(chess.Move.from_uci(user_move))
            turn = chess.BLACK
            time.sleep(0.5)

        else:
            if play_rand == 1:
                rand_num = rand_num+1
                legal_list = []
                for i in board.legal_moves:
                    legal_list.append(str(i))

                random_move = random.choice(legal_list)
                selected_move = chess.Move.from_uci(random_move)

            else:
                legal_list = []
                for i in board.legal_moves:
                    legal_list.append(str(i))

                # epsilon의 확률로 랜덤

                if len(current_node.next) == 0:  # next가 비어있는 경우 랜덤
                    random_move = random.choice(legal_list)
                    chess_model.insert(random_move, current_node, None)
                    current_node = current_node.next[0]
                    selected_move = chess.Move.from_uci(current_node.move)

                else:  # reward가 가장 큰 노드 선택
                    next_node = current_node.next[0]
                    for i in current_node.next:
                        if next_node.reward < i.reward:
                            next_node = i
                    current_node = next_node
                    selected_move = chess.Move.from_uci(current_node.move)

            board.push(selected_move)
            floor = floor + 1
            turn = chess.WHITE
            time.sleep(0.5)

        if board.is_game_over() is True:
            floor_sum = floor_sum + floor
            floor_list.append(floor)
            grd_list.append(floor-rand_num)

            log = open("random_log.txt", 'a')
            log.write(str(floor-rand_num) + "/" + str(floor) + "\n")
            log.close()

            if max < floor - rand_num:
                max = floor - rand_num
            if min > floor - rand_num:
                min = floor - rand_num
            # print(board.result())
            if board.result() == "1-0":
                # print('\nWHITE win\n')
                win = win+1
            elif board.result() == "0-1":
                # print('\nBLACK win\n')
                lose = lose + 1
            elif board.result() == "1/2-1/2":
                # print('\nDraw!\n')
                draw = draw + 1
            break

grd_avg = sum(grd_list)/len(grd_list)
average = floor_sum / REPEAT

log = open("random_log.txt", 'a')
log.write("win = " + str(win) + "\n")
log.write("lose = " + str(lose) + "\n")
log.write("draw = " + str(draw) + "\n")
log.write("no_data = " + str(no_data) + "\n\n")

log.write("max = " + str(max) + "\n")
log.write("min = " + str(min) + "\n")
log.write("average = " + str(grd_avg) + "\n")
log.close()
