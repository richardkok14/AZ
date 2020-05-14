import numpy as np
import unittest
from .HexGame import HexGame
from .HexLogic import Board

class TestHexMethods(unittest.TestCase):

    def testInit(self):
        #all board positions should be zero
        self.assertEqual(sum(HexGame().getInitBoard().flatten()), 0)
    def testSize(self):
        n = HexGame().n
        #check state space and action space with last place equal to no action
        self.assertEqual(HexGame().getBoardSize(),(n,n))
        self.assertEqual(HexGame().getActionSize(),n*n+1)
    def testMoveActionConversion(self):
        game = HexGame()
        #check if conversion from acton to move and to action again equals identity function
        for action in range(game.n*game.n):
            self.assertEqual(game.getActionFromMove(game.getMoveFromAction(action)), action)
    def testNextState(self):
        game = HexGame()
        board = game.getInitBoard()
        for player in [-1, 1]:
            #make moves for actions [0,n*n), check if players alternate and boards gets filled
            for action in range(game.n*game.n):
                (y, x) = game.getMoveFromAction(action)
                board_next, player_next = game.getNextState(
                    board, player, action)
                self.assertEqual(player_next, -player)
                self.assertEqual(board[y][x]+board_next[y][x], player)
    def testValidMoves(self):
        game = HexGame()
        for player in [-1, 1]:
            for i in range(100):
                game = HexGame()
                board = game.getInitBoard()
                actions_rand = set(np.random.randint(0, game.n*game.n, np.random.randint(game.n*game.n)))
                #if no action, check if all actions are still available
                if len(actions_rand)==1 and game.getActionSize() in actions_rand:
                    (board, player) = game.getNextState(board, player, next(actions_rand))
                    self.assertEqual(len(game.getValidMoves(board)), game.n*game.n)
                #make moves, test if move is no longer valid for both players
                for action in actions_rand:
                    (board, player) = game.getNextState(board, player, action)
                    validMoves = game.getValidMoves(board)
                    self.assertEqual(game.getValidMoves(board)[action], 0)
                    self.assertEqual(game.getValidMoves(board)[action], 0)
                #if all possible actions taken, check if no valid moves left
                if len(actions_rand) == game.getActionSize():
                    self.assertEqual(game.getValidMoves(board)[-1], 1)
    def testGameEnded(self):
        game = HexGame()
        for player in [-1, 1]:
            for y in range(game.n):
                board = game.getInitBoard()
                for x in range(game.n):
                    #no connection yet
                    self.assertEqual(game.getGameEnded(board, player),0)
                    self.assertEqual(game.getGameEnded(board, -player),0)
                    (board, _) = game.getNextState(board, player, game.getActionFromMove((y,x)))
                if player == Board.BLUE:
                    #horizontal connection
                    self.assertEqual(game.getGameEnded(board, player),1)
                    self.assertEqual(game.getGameEnded(board, -player),-1)
            for x in range(game.n):
                board = game.getInitBoard()
                for y in range(game.n):
                    #no connection
                    self.assertEqual(game.getGameEnded(board, player),0)
                    self.assertEqual(game.getGameEnded(board, -player),0)
                    (board, _) = game.getNextState(board, player, game.getActionFromMove((y,x)))
                #vertical connection
                if player == Board.RED:
                    self.assertEqual(game.getGameEnded(board, player),1)
                    self.assertEqual(game.getGameEnded(board, -player),-1)
    # def testCanonical(self):
    #     for player in [-1, 1]:
    #         for i in range(100):
    #             game = HexGame()
    #             actions_rand = set(np.random.randint(0, game.n*game.n, np.random.randint(game.n*game.n)))
    #             board = game.getInitBoard()
    #             #test for diifferent board configurations
    #             for action in actions_rand:
    #                 (board, _) = game.getNextState(board, np.random.choice([-1,1]), action)
    #                 self.assertEqual(np.sum(game.getCanonicalForm(board, 1)),
    #                                   -np.sum(game.getCanonicalForm(board, -1)))
    def testSymmetries(self):
        for i in range(100):
            game = HexGame()
            actions_rand = set(np.random.randint(0, game.n*game.n, np.random.randint(game.n*game.n)))
            board = game.getInitBoard()
            for action in actions_rand:
                (board, _) = game.getNextState(board, np.random.choice([-1,1]), action)
                pi_board = np.random.randn(game.getActionSize())
                pi_board[game.getValidMoves(board)] = 0
                symms = np.array(game.getSymmetries(board, pi_board))
                #test if symmetries give boards and pi values flipped horizontally and vertically
                self.assertTrue(self.in_array(board,symms[:,0], game.n))
                self.assertTrue(self.in_array(board[::-1,:], symms[:,0],game.n))
                self.assertTrue(self.in_array(board[:,::-1], symms[:,0],game.n))

                pi_board = pi_board[:game.n*game.n].reshape(game.n, game.n)

                pi_boards = np.array([x[:game.n*game.n] for x in symms[:,1]])
                pi_boards = pi_boards.reshape(pi_boards.shape[0], game.n, game.n)
                self.assertTrue(self.in_array(pi_board,pi_boards, game.n))
                self.assertTrue(self.in_array(pi_board[::-1,:], pi_boards, game.n))
                self.assertTrue(self.in_array(pi_board[:,::-1], pi_boards,game.n))

    def in_array(self, array, array_of_array, n):
        return np.any([np.all([array[y][x] == array_[y][x]
                    for x in range(n) for y in range(n)])
                    for array_ in array_of_array])

if __name__ == '__main__':
    unittest.main()