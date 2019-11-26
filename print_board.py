import chess

board = chess.Board()
symbol = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
j = 7
k = 0
print("8"+"   ", end='')
for i in board.board_fen():
    if i == '/':
        print()
        print(j,"  ", end='')
        j = j-1
    elif (i in symbol) is True:
        print(i,"", end='')
    else:
        for k in range(0, int(i)):
            print("- ", end='')
        k = 0

print()
print()
print("    "+"a b c d e f g h")

