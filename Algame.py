

def evaluate(board):
    # Simple heuristic: difference in piece count
    return np.sum(board)

def minimax(game, depth, maximizing_player, alpha, beta):
    if depth == 0:
        return evaluate(game.board)
    piece = 1 if maximizing_player else -1
    legal_moves = [(i, j) for i in range(8) for j in range(8) if game.step(i, j, piece,False) > 0]

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            game_copy = game
            game_copy.step(*move, 1)
            eval = minimax(game_copy, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            game_copy = game
            game_copy.step(*move, -1)
            eval = minimax(game_copy, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

import numpy as np
import socket, pickle
from reversi import reversi

def main():
    game_socket = socket.socket()
    game_socket.connect(('127.0.0.1', 33333))
    game = reversi()

    while True:

        #Receive play request from the server
        #turn : 1 --> you are playing as white | -1 --> you are playing as black
        #board : 8*8 numpy array
        data = game_socket.recv(4096)
        turn, board = pickle.loads(data)

        #Turn = 0 indicates game ended
        if turn == 0:
            game_socket.close()
            return
        
        #Debug info
        print(turn)
        print(board)

        #Local Greedy - Replace with your algorithm
        x = -1
        y = -1
        max_eval = 0
        game.board = board
        for i in range(8):
            for j in range(8):
                cur = game.step(i, j, turn, True)
                if cur > 0:
                    max_player = True if turn == 1 else False
                    eval = minimax(game,depth=3, maximizing_player=max_player,alpha=float('-inf'), beta=float('inf'))
                    if eval > max_eval:
                        max_eval = eval
                        x,y=i,j

        #Send your move to the server. Send (x,y) = (-1,-1) to tell the server you have no hand to play
        game_socket.send(pickle.dumps([x,y]))
        
if __name__ == '__main__':
    main()
