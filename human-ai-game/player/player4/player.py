import numpy as np

POS_INFINITY = float('inf')
NEG_INFINITY = float('-inf')


class Player:
    def __init__(self):
        self.game_board_state = []
        self.player_n = 0

    def play(self, game_board_state, player_n):
        if player_n == 0:
            self.player = 0
            self.opponent = 1
        else:
            self.player = 1
            self.opponent = 0

        self.game_board_state = game_board_state
        self.possiblemoves = [i for i in range(len(game_board_state)) if game_board_state[i] < 0]
        bestmove = game_board_state.index(-1)

        # Make Win Move
        for free in self.possiblemoves:
            board = game_board_state[:]
            board[free] = self.player
            win_board = np.array(board)
            if self.GetWinLine(win_board, self.player):
                print("Here1")
                print(free)
                bestmove = free
                return bestmove
        # Block Opponent Winning Line
        for block in self.possiblemoves:
            board = game_board_state[:]
            board[block] = self.opponent
            win_board = np.array(board)
            if self.GetWinLine(win_board, self.opponent):
                print("Here2")
                print(block)
                bestmove = block
                return bestmove
        return bestmove

    def GetWinLine(self, win_board, player_n):
        return(
            list(win_board[[0, 1, 2, 3]]).count(player_n) == 4 or
            list(win_board[[4, 5, 6, 7]]).count(player_n) == 4 or
            list(win_board[[8, 9, 10, 11]]).count(player_n) == 4 or
            list(win_board[[12, 13, 14, 15]]).count(player_n) == 4 or
            list(win_board[[0, 4, 8, 12]]).count(player_n) == 4 or
            list(win_board[[1, 5, 9, 13]]).count(player_n) == 4 or
            list(win_board[[2, 6, 10, 14]]).count(player_n) == 4 or
            list(win_board[[3, 7, 11, 15]]).count(player_n) == 4 or
            list(win_board[[0, 5, 10, 15]]).count(player_n) == 4 or
            list(win_board[[3, 6, 9, 12]]).count(player_n) == 4)

    def alphabeta_search(state, game):

        player = game.to_move(state)

        # Functions used by alphabeta
        def max_value(state, alpha, beta):
            if game.terminal_test(state):
                return game.utility(state, player)
            v = NEG_INFINITY
            for a in game.actions(state):
                v = max(v, min_value(game.result(state, a), alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta):
            if game.terminal_test(state):
                return game.utility(state, player)
            v = POS_INFINITY
            for a in game.actions(state):
                v = min(v, max_value(game.result(state, a), alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        # Body of alphabeta_search:
        best_score = -NEG_INFINITY
        beta = POS_INFINITY
        best_action = None
        for a in game.actions(state):
            v = min_value(game.result(state, a), best_score, beta)
            if v > best_score:
                best_score = v
                best_action = a
        return best_action

