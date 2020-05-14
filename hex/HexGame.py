from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .HexLogic import Board
import numpy as np
np.random.seed(0)

"""
Game class implementation for the game of TicTacToe.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""
class HexGame(Game):
    def __init__(self, n=6):
        super().__init__()
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n + 1

    def getActionFromMove(self, move):
        (y,x) = move
        return y*self.n + x

    def getMoveFromAction(self, action):
        return (action//self.n, action%self.n)

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = self.getMoveFromAction(action)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves()
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        if b.has_legal_moves():
            return 0
        # draw has a very little value 
        return 1e-4

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        for ud in [True, False]:
            for lr in [True, False]:
                newB, newPi = board, pi_board
                if ud:
                    newB = np.flipud(newB)
                    newPi = np.flipud(pi_board)
                if lr:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def print(self):
        print("   ",end="")
        for x in range(self.size):
            print(chr(x+ord('a')),"",end="")
        print("")
        print(" -----------------------")
        for y in range(self.size):
            print(y, "|",end="")
            for z in range(y):
                print(" ", end="")
            for x in range(self.size):
                piece = self.board[y,x]
                if piece == Board.BLUE: print("b ",end="")
                elif piece == Board.RED: print("r ",end="")
                else:
                    if x==self.size:
                        print("-",end="")
                    else:
                        print("- ",end="")
            print("|")
        print("   -----------------------")
