import chess
import pickle


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

with open('data.pickle', 'rb') as f:
    data = pickle.load(f)

current_node = data.head
board = chess.Board()

while(1):
    display()
    count = 1
    for i in current_node.next:
        print(str(count) + " / " + str(i.move) + " / " + str(i.reward))
        count += 1
    
    user = input("select : ")
    board.push(chess.Move.from_uci(current_node.next[int(user)-1].move))

    current_node = current_node.next[int(user)-1]
    
    if board.is_game_over() is True:
        break
