import chess
import random
import os
import time

turn = chess.WHITE
gameover = False
board = chess.Board()


while board.is_game_over() is False:
    os.system('clear')
    print(board)
    # print(board.is_game_over())
    
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
            else:        
                p_move = input("type your move(just like 'a2a4'):")
                break
        turn = chess.BLACK
