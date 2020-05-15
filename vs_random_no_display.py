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
        self.accumulated_board = 0

    def insert(self, move, p):
        new_node = self.Node(move, p)
        p.next.append(new_node)
        self.size += 1


print("data load start\n")
sys.setrecursionlimit(10000)
with open('data.pickle', 'rb') as f:
    chess_model = pickle.load(f)

current_node = chess_model.head

piece_list = ['p','r','n','b','q','k','P','R','N','B','Q','K']
piece = []
for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0] = piece_list[i]

# model's win rate
win = 0
lose = 0
draw = 0
match_num = 50  # number of match
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
for i in range(match_num):
    turn = chess.WHITE
    board = chess.Board()
    current_node = chess_model.head
    floor = 0
    rand_num = 0
    play_rand = 0
    game_num = 0


    while True:
        os.system('clear')
        # print(game_num, "game\n")
        game_num = game_num+1

        if turn is chess.BLACK:
            legal_list = []
            for i in board.legal_moves:
                legal_list.append(str(i))
            r_move = chess.Move.from_uci(random.choice(legal_list))
            find = 0
            if play_rand == 0:
                for i in current_node.next:
                    if str(r_move) == i.move:
                        find = 1
                        current_node = i
                if find == 0:
                    no_data = no_data + 1
                    play_rand = 1

            board.push(r_move)
            turn = chess.WHITE

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

            board.push(selected_move)
            floor = floor + 1
            turn = chess.BLACK

        if board.is_game_over() is True:
            floor_sum = floor_sum + floor
            floor_list.append(floor)
            grd_list.append(floor-rand_num)

            log = open("random_log.txt", 'a')
            log.write(str(game_num) + ":" + str(floor-rand_num) + "/" + str(floor) + "\n")
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
            time.sleep(1)
            break

average = floor_sum / match_num

log = open("random_log.txt", 'a')
log.write("\nwin lose draw nodata\n")
log.write(str(win) + str(lose) + str(draw) + str(no_data) + "\n")

# print("Floor")
# for i in range(match_num):
#     print("Floor", i+1, ":", grd_list[i], "/", floor_list[i])

log.write("max = " + str(max) + "\n")
log.write("min = " + str(min) + "\n")
log.write("average = " + str(average) + "\n")
log.close()
