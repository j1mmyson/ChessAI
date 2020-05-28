import chess
import random
import pickle
import sys
import copy

REPEAT = 3

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
        self.search_list = []
        self.size = 0
        self.accumulated_play = 0

    def insert(self, move, p, state):
        new_node = self.Node(move, p, state)
        p.next.append(new_node)
        self.search_list.append(new_node)
        self.size += 1

    def search(self, new_state, current_node):
        for i in self.search_list:
            if(str(i.state) == str(new_state) and i.state.turn == new_state.turn):
                print("진입")
                current_node.next.append(i)
                return True
        return False

try:
    data = open('data.pickle', 'rb')
except FileNotFoundError:
    print("Make new List (Error: FileNotFoundError)")
    chess_model = LinkedList()
else:
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    chess_model = data

sys.setrecursionlimit(10**7)
current_node = chess_model.head

record_list = []
# main
for i in range(REPEAT):
    board = chess.Board()
    floor = 0

    while True:
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))

        if 0.99999**chess_model.accumulated_play >= 0.2:
            epsilon = 0.99999**chess_model.accumulated_play # epsilon의 확률로 랜덤, 0.99999^x 곡선으로 epsilon 변화
        else:
            epsilon = 0.2

        # epsilon의 확률로 랜덤
        random_value = random.random()

        if not current_node.next: # next가 비어있는 경우 랜덤
            random_move = random.choice(legal_list)
            selected_move = chess.Move.from_uci(random_move)
            board.push(selected_move)

            state = copy.deepcopy(board)
            search_result = chess_model.search(state, current_node)

            if search_result is True:
                current_node.next[-1].prev = current_node
                current_node = current_node.next[-1]
            else:
                chess_model.insert(random_move, current_node, state)
                current_node = current_node.next[-1]

        elif epsilon <= random_value: # 최선의 수 선택
            current_node.next[0].prev = current_node
            current_node = current_node.next[0]
            selected_move = chess.Move.from_uci(current_node.move)
            board.push(selected_move)

        else: # 탐험
            random_move = random.choice(legal_list)
            find = False

            for i in current_node.next:
                if random_move == i.move:
                    find = True
                    i.prev = current_node
                    current_node = i
                    break

            if find is True:
                selected_move = chess.Move.from_uci(current_node.move)
                board.push(selected_move)
            else:
                selected_move = chess.Move.from_uci(random_move)
                board.push(selected_move)

                state = copy.deepcopy(board)
                search_result = chess_model.search(state, current_node)


                if search_result is True:
                    current_node.next[-1].prev = current_node
                    current_node = current_node.next[-1]
                else:
                    chess_model.insert(random_move, current_node, state)
                    current_node = current_node.next[-1]

        floor += 1
        record_list.append(current_node)
        if board.is_game_over() is True:
            record_list.reverse()
            break

    my_floor = floor

    if board.result() == "1/2-1/2":
        winning_point = 0.5
    else:
        winning_point = 1

    for i in range(len(record_list)):  # 갱신
        if i % 2 == 0:
            print("+")
            record_list[i].reward = record_list[i].reward + 1
        else:
            print("-")
            record_list[i].reward = record_list[i].reward - 1

    record_list.clear()




    chess_model.accumulated_play += 1
    if chess_model.accumulated_play%100 == 0:
        log = open("log.txt", 'a')
        log.write(str(chess_model.accumulated_play)+"\n")
        log.close()

    print(str(chess_model.accumulated_play))

with open('data.pickle', 'wb') as f:
    pickle.dump(chess_model, f, pickle.HIGHEST_PROTOCOL)

print("OK")
