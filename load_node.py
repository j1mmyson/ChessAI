import pickle


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


with open('data.pickle', 'rb') as f:
    data = pickle.load(f)

current_node = data.head

while(1):
    # print(current_node.reward)
    current_node = current_node.next[0]
    if len(current_node.next) == 0:
        print(data.size)
        break


