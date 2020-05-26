import chess
import random
import pickle
import sys
import copy
import time
import os

BOLD = '\033[1m'
CEND = '\033[0m'
CRED = '\033[31m'
CGRAY = '\033[90m'
REPEAT = 1

class LinkedList:
    class Node:
        def __init__(self, move, prev, state):
            self.move = move
            self.reward = 0.5
            self.prev = prev
            self.next = []
            self.state = state
            self.visited = 0

    def __init__(self):
        self.head = self.Node(None, None, None)
        self.size = 0
        self.accumulated_board = 1

    def insert(self, move, p, state):
        new_node = self.Node(move, p, state)
        p.next.append(new_node)
        self.size += 1
    
    def pre_order1(self,node):
        node.visited += 1
        if node.visited > 1 : return
        else:
            print(str(node.move)+', '+str(node.visited))
            for i in node.next:
                self.pre_order1(i)

    def pre_order(self, node, new_state, current_node):
        node.visited += 1
        if node.visited > 1 : return
        if(str(node.state) == str(new_state)) and (node.state.turn is new_state.turn):
            print("find")
            print('node.move: '+str(node.move))
            current_node.next.append(node)
            return 100, node
        else:  
            for i in node.next:
                if self.pre_order(i, new_state, current_node)[0] == 100:
                    return 100, current_node.next[-1]
        return 0, node

    def reset(self,node, size):
        if size < 0: return
        # print('visited = 0')
        node.visited = 0
        size -= 1
        for i in node.next:
            self.reset(i,size)

def pre_order3(node):
    node.visited += 1
    if node.visited > 1 : return
    else:
        next_list = []
        for i in node.next:
            next_list.append(i.move)
        print(str(node.move)+' -> '+str(next_list))
        for i in node.next:
            pre_order3(i)

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

sys.setrecursionlimit(10000000)
current_node = chess_model.head
piece_list = ['p','r','n','b','q','k','P','R','N','B','Q','K']
piece = []

random.seed(345)

for i in range(12):
    line = [0, 0]
    piece.append(line)
    piece[i][0]= piece_list[i]

# main
for i in range(REPEAT):
    board = chess.Board()
    chess_model.head.state = copy.deepcopy(board)
    floor = 0
    my_list = []

    while True:
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))

        display()
        # print('accumulated_board: '+ str(chess_model.accumulated_board))
        # print('current_node id: '+ str(id(current_node))+'\ncurrent_node move: '+str(current_node.move))

        # next가 비어있는 경우: 탐험
        if not current_node.next:
            print('next is empty')
        
        # next가 비어있지 않은 경우
        else:
            next_list = []
            for i in current_node.next:
                next_list.append(i.move)
            print('next is: ' + str(next_list))

        print('\nlegal list: '+str(legal_list))
        user_move = input("enter the move(like 'e2e4'): ")
        
        # user_move is not legal
        if user_move not in legal_list:
            print(CRED+"your choice is NOT legal"+CEND)
        
        # user_move is legal
        else:
            print('user_move is legal')
            find = False
            for i in current_node.next:
                if user_move == i.move:
                    find = True
                    break
            if find == True:
                print('and find is True')
                board.push(chess.Move.from_uci(user_move))
                current_node = i

            else:
                print('and find is False')
                board.push(chess.Move.from_uci(user_move))
                my_list.append([user_move, id(user_move)])
                state = copy.deepcopy(board)

                # print('before reset')
                print('model_size: '+str(chess_model.size))
                chess_model.reset(chess_model.head, chess_model.size)
                print("\npre_order start")
                search_result = chess_model.pre_order(chess_model.head, state, current_node)
                print("pre_order end")
                if search_result[0] == 100:
                    current_node = search_result[1]
                    print("\nfound by pre_order\n")
                    print(str(my_list)+'\n')

                    # print('search_result[1] id : '+ str(id(search_result[1])))
                    # print('search_result[1].move: '+ str(search_result[1].move))
                    # print('current_node id: '+ str(id(current_node)))
                    # print('current_node.move: '+ str(current_node.move))

                else:
                    print("\ncannot found by pre_order")
                    chess_model.insert(user_move, current_node, state)
                    current_node = current_node.next[-1]
                    print()

                chess_model.reset(chess_model.head,chess_model.size)
                print('pre_order1111111')
                chess_model.pre_order1(chess_model.head)
                chess_model.reset(chess_model.head,chess_model.size)
                print('\npre_order3333333')
                pre_order3(chess_model.head)


        floor += 1
        if board.is_game_over() is True:
            break

    my_floor = floor
    if board.result() == "1/2-1/2":
        winning_point = 0.5
    else:
        winning_point = 1

    # reward
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
