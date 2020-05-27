import chess
import random
import pickle
import sys
import copy

REPEAT = 10

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
        self.accumulated_board = 0

    def insert(self, move, p, state):
        new_node = self.Node(move, p, state)
        p.next.append(new_node)
        self.search_list.append(new_node)
        self.size += 1

    def search(self, new_state, current_node):
        for i in self.search_list:
            if(str(i.state) == str(new_state) and i.state.turn == new_state.turn):
                current_node.next.append(i)
                return True
        return False
        

# def pre_order(node, new_state, current_node):
#     if(str(node.state) == str(new_state) and node.state.turn == new_state.turn):
#         print("preorder if 진입")
#         current_node.next.append(node)
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!" + str(chess_model.accumulated_board))
#         return True
#     else:
#         for i in node.next:
#             if pre_order(i, new_state, current_node) is True:
#                 return True
#     return False

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

# main
for i in range(REPEAT):
    board = chess.Board()
    floor = 0

    while True:
        print("넘어감")
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))

        if 0.99999**chess_model.accumulated_board >= 0.2:
            epsilon = 0.99999**chess_model.accumulated_board # epsilon의 확률로 랜덤, 0.99999^x 곡선으로 epsilon 변화
        else:
            epsilon = 0.2

        # epsilon의 확률로 랜덤
        random_value = random.random()
        
        print("if-elif-else 진입")
        if not current_node.next: # next가 비어있는 경우 랜덤
            print("if 진입 - next가 비어있는 경우 랜덤")
            random_move = random.choice(legal_list)
            selected_move = chess.Move.from_uci(random_move)
            board.push(selected_move)
                
            state = copy.deepcopy(board)
            search_result = chess_model.search(state, current_node)
            print(str(chess_model.accumulated_board) + " !!!")

            if search_result is True:
                current_node = current_node.next[-1]
            else:
                chess_model.insert(random_move, current_node, state)
                current_node = current_node.next[-1]

        elif epsilon <= random_value: # 최선의 수 선택
            print("if 거짓 elif 진입 - 최선의 수 선택")
            current_node = current_node.next[0]
            selected_move = chess.Move.from_uci(current_node.move)
            board.push(selected_move)

        else: # 탐험
            print("elif 거짓 else 진입 - 탐험")
            random_move = random.choice(legal_list)
            find = False

            print("탐험 - for 시작 - 내 자식에 찾는게 있는지")
            for i in current_node.next:
                if random_move == i.move:
                    find = True
                    current_node = i
                    break
            
            if find is True:
                print("탐험 내부 for 끝 - if 찾은게 있으면 푸시")
                selected_move = chess.Move.from_uci(current_node.move)
                board.push(selected_move)
            else:
                print("탐험 내부 for 끝 - if find 거짓 - pre_order진입")
                selected_move = chess.Move.from_uci(random_move)
                board.push(selected_move)
                
                state = copy.deepcopy(board)
                print("pre_order 진입 직전")
                search_result = chess_model.search(state, current_node)
                print(str(chess_model.accumulated_board) + " !!!")

                if search_result is True:
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
    if chess_model.accumulated_board%100 == 0:
        log = open("log.txt", 'a')
        log.write(str(chess_model.accumulated_board)+"\n")
        log.close()
        

with open('data.pickle', 'wb') as f:
    pickle.dump(chess_model, f, pickle.HIGHEST_PROTOCOL)

print("OK")