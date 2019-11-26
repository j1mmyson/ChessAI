import chess
import os
import random
import time



def print_board(board):
    symbol = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    j = 7
    k = 0
    print("8"+"   ", end='')
    for i in board.board_fen():
        print()
        print(j, "  ", end='')
        j = j-1
    elif (i in symbol) is True:
        print(i, "", end='')
    else:
        for k in range(0, int(i)):
            print("- ", end='')
        k = 0
    print()
    print()
    print("    "+"a b c d e f g h")


turn = chess.WHITE
gameover = False
board = chess.Board()


while board.is_game_over() is False:
    os.system('clear')
    print_board(board)
    print(board.is_game_over())
    # if board.is_game_over() is True:
    #     print("GAME OVER")
    #     break
    if turn is chess.BLACK:
        # computer(AI) play
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))
        c_move = chess.Move.from_uci(random.choice(legal_list))
        board.push(c_move)
        time.sleep(1.5)
        turn = chess.WHITE
    else:
        # player
        legal_list = []
        for i in board.legal_moves:
            legal_list.append(str(i))

        p_move = input("type your move(just like 'a2a4'):")
        while True:
            if p_move in legal_list:
                board.push(chess.Move.from_uci(p_move))
                break
            else:
                p_move = input("type your move(just like 'a2a4'):")
        turn = chess.BLACK
