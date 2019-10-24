# Tic Tac Toe game in python

"""
    The program uses minimax tree algorithm to reduce the search
"""
import sys
import random
import copy

board = [' ' for x in range(17)]


class Intelligent_Player:
    def __init__(self):
        self.INFINITY = 100
        self.maxSearchDepth = 2
        self.marker = 'x'
        self.my_move = False
        return

    def heuristics(self, oldMove, newMove, board):
        curr_flag = 'x'

        own_flag = self.marker
        if self.my_move:
            curr_flag = own_flag
        else:
            curr_flag = self.marker

        # checking if own turn or opponents turn
        var_mm = 0
        if not self.my_move:
            var_mm = -1  # opponents turn
        else:
            var_mm = 1  # own turn

        tempBoard = copy.deepcopy(board)

        # bs = tempBoard.board_status
        status = tempBoard.find_terminal_state()
        # if game has already ended
        if status[1] == 'WON':
            return var_mm * 10000
        elif status[1] == 'DRAW':  # have to maximize score with draw
            x = 0
            o = 0
            for i in range(4):
                for j in range(4):
                    if tempBoard.block_status[i][j] == 'x':
                        x += 1
                    if tempBoard.block_status[i][j] == 'o':
                        o += 1
            if own_flag == 'x':
                return x - o
            else:
                return o - x

        # if the game is not yet over heuristics acc to current scenario
        heurVal = 0

        bs = tempBoard.block_status

        ##############################################################
        # checking for continuous blocks or cutting other blocks
        ##############################################################

        # checking rows
        for i in range(4):
            fl = 0
            count = 0
            for j in range(4):
                if bs[i][j] == self.marker:
                    fl = 1
                if bs[i][j] == own_flag:
                    count += 1
            if fl == 0 and count > 0:
                for j in range(4):
                    heurVal += (2 if bs[i][j] == own_flag else 0)
            if fl == 1 and count > 0:
                for j in range(4):
                    heurVal += (3 if bs[i][j] == self.marker else 0)

        # checking columns
        for j in range(4):
            fl = 0
            count = 0
            for i in range(4):
                if bs[i][j] == self.marker:
                    fl = 1
                if bs[i][j] == own_flag:
                    count += 1
            if fl == 0 and count > 0:
                for i in range(4):
                    heurVal += (2 if bs[i][j] == own_flag else 0)
            if fl == 1 and count > 0:
                for i in range(4):
                    heurVal += (3 if bs[i][j] == self.marker else 0)

        # checking forward diagonal
        fl = 0
        count = 0
        for i in range(4):
            if bs[i][i] == self.marker:
                fl = 1
            if bs[i][i] == own_flag:
                count += 1
        if fl == 0 and count > 0:
            for i in range(4):
                heurVal += (2 if bs[i][i] == own_flag else 0)
        if fl == 1 and count > 0:
            for i in range(4):
                heurVal += (3 if bs[i][i] == self.marker else 0)

        # checking back diagonal
        fl = 0
        count = 0
        for i in range(4):
            if bs[3 - i][i] == self.marker:
                fl = 1
            if bs[3 - i][i] == own_flag:
                count += 1
        if fl == 0 and count > 0:
            for i in range(4):
                heurVal += (2 if bs[3 - i][i] == own_flag else 0)
        if fl == 1 and count > 0:
            for i in range(4):
                heurVal += (3 if bs[3 - i][i] == self.marker else 0)
        _b = tempBoard.board_status
        for k in range(4):
            for l in range(4):

                # checking rows
                for i in range(4):
                    fl = 0
                    count = 0
                    for j in range(4):
                        if _b[4 * k + i][4 * l + j] == self.marker:
                            fl = 1
                        if _b[4 * k + i][4 * l + j] == own_flag:
                            count += 1
                    if fl == 0 and count > 0:
                        # print "continuous row"
                        for j in range(4):
                            heurVal += (2 if _b[4 * k + i][4 * l + j] == own_flag else 0)
                    if fl == 1 and count > 0:
                        # print "row"
                        for j in range(4):
                            heurVal += (3 if _b[4 * k + i][4 * l + j] == self.marker else 0)

                # checking columns
                for j in range(4):
                    fl = 0
                    count = 0
                    for i in range(4):
                        if _b[4 * k + i][4 * l + j] == self.marker:
                            fl = 1
                        if _b[4 * k + i][4 * l + j] == own_flag:
                            count += 1
                    if fl == 0 and count > 0:
                        # print "continuous columns"
                        for i in range(4):
                            heurVal += (2 if _b[4 * k + i][4 * l + j] == own_flag else 0)
                    if fl == 1 and count > 0:
                        # print "column kaata"
                        for i in range(4):
                            heurVal += (3 if _b[4 * k + i][4 * l + j] == self.marker else 0)

                # checking forward diagonal
                fl = 0
                count = 0
                for i in range(4):
                    if _b[4 * k + i][4 * l + i] == self.marker:
                        fl = 1
                    if _b[4 * k + i][4 * l + i] == own_flag:
                        count += 1
                if fl == 0 and count > 0:
                    # print "continous diagonal"
                    for i in range(4):
                        heurVal += (2 if _b[4 * k + i][4 * l + i] == own_flag else 0)
                if fl == 1 and count > 0:
                    # print "diagonal "
                    for i in range(4):
                        heurVal += (3 if _b[4 * k + i][4 * l + i] == self.marker else 0)

                # checking back diagonal
                fl = 0
                count = 0
                for i in range(4):
                    if _b[4 * k + 3 - i][4 * l + i] == self.marker:
                        fl = 1
                    if _b[4 * k + 3 - i][4 * l + i] == own_flag:
                        count += 1
                if fl == 0 and count > 0:
                    # print "continous backward diagonal"
                    for i in range(4):
                        heurVal += (2 if _b[4 * k + 3 - i][4 * l + i] == own_flag else 0)
                if fl == 1 and count > 0:
                    # print "back diagonal "
                    for i in range(4):
                        heurVal += (3 if _b[4 * k + 3 - i][4 * l + i] == self.marker else 0)

        for k in range(4):
            for l in range(4):

                # winning/losing centre block
                if (k == 1 or k == 2) and (k == 1 or k == 2):
                    if bs[k][l] == own_flag:
                        heurVal += 10
                    elif bs[k][l] == self.marker:
                        heurVal -= 10

                # winning/losing corner blocks
                if (k == 0 or k == 3) and (l == 0 or l == 3):
                    if bs[k][l] == own_flag:
                        heurVal += 10  # 3
                    elif bs[k][l] == self.marker:
                        heurVal -= 10  # 3

                # winning/losing blocks
                if bs[k][l] == own_flag:
                    heurVal += 10
                elif bs[k][l] == self.marker:
                    heurVal -= 10

                for i in range(4):
                    for j in range(4):

                        # getting centre squares in blocks
                        if (i == 1 or i == 2) and (j == 1 or j == 2):
                            if _b[4 * k + i][4 * l + j] == own_flag:
                                # print "centre square mila"
                                heurVal += 3
                            elif _b[4 * k + i][4 * l + j] == self.marker:
                                # print "centre square kata"
                                heurVal -= 3

                        # getting corner squares in blocks
                        if (i == 0 or i == 3) and (j == 0 or j == 3):
                            if _b[4 * k + i][4 * l + j] == own_flag:
                                # print "corner square mila"
                                heurVal += 3
                            elif _b[4 * k + i][4 * l + j] == self.marker:
                                # print "corner square kata"
                                heurVal -= 3

                        # getting square in centre block
                        if (k == 1 or k == 2) and (l == 1 or l == 2):
                            if _b[4 * k + i][4 * l + j] == own_flag:
                                # print "centre block me mila"
                                heurVal += 2
                            elif _b[4 * k + i][4 * l + j] == self.marker:
                                # print "centre block me kata"
                                heurVal -= 2

                        # getting square in corner block
                        if (k == 0 or k == 3) and (l == 0 or l == 3):
                            if _b[4 * k + i][4 * l + j] == own_flag:
                                # print "corner block me mila"
                                heurVal += 2
                            elif _b[4 * k + i][4 * l + j] == self.marker:
                                # print "corner block me kata"
                                heurVal -= 2

        del tempBoard

        return heurVal

    def marker(self, flag):
        if flag == 'x':
            return 'o'
        else:
            return 'x'

    def evaluate(self, old_move, node, board):
        # return random.randint(-100,101)
        return self.heuristics(old_move, node, board)

    def move(self, board, old_move, flag):
        self.marker = flag
        self.my_move = True

        # Find the list of valid cells allowed
        cells = board.find_valid_move_cells(old_move)
        init_moves = len(cells)

        # Make a copy of board for future use
        board_copy = copy.deepcopy(board)
        move = copy.deepcopy(old_move)

        answer_value = -self.INFINITY
        # answer_index = []

        for i in range(0, init_moves):
            temp_value, temp_index = self.IDS(cells[i], board_copy, move)
            if temp_value > answer_value:
                answer_value = copy.deepcopy(temp_value)
                answer_index = copy.deepcopy(temp_index)
            # answer_index = []
            # answer_index.append(temp_index)
        # elif (temp_value == answer_value):
        # answer_index.append(temp_index)

        # moveCell = random.randint(0, len(answer_index)-1)
        # print answer_value
        del board_copy
        return answer_index

    def _MTDf(self, root, f, d, board, old_move):
        g = f
        upper_bound = self.INFINITY
        lower_bound = -self.INFINITY

        while lower_bound < upper_bound:
            beta = max(g, lower_bound + 1)
            board_copy = copy.deepcopy(board)
            board_copy.update(old_move, root, self.marker)
            self.my_move = True

            g = self.node_beta(root, beta - 1, beta, d, board_copy, old_move)
            if g < beta:
                upper_bound = g
            else:
                lower_bound = g
        del board_copy
        return g

    def store(self):
        pass

    def retrieve(self):
        pass

    def get_children(self, board, blockIdentifier):
        cells = board.find_valid_move_cells(blockIdentifier)
        return cells

    def node_beta(self, node, alpha, beta, d, board, old_move):
        # Transposition table lookup
        # lowerbound = 2*self.INFINITY
        # lowerbound, upperbound = self.retrieve(node)
        #
        # if lowerbound != 2*self.INFINITY:
        # 	# Value exists in Transposition table i.e Node value has been determined earlier
        # 	if lowerbound >= beta:
        # 		return lowerbound
        #
        # 	if upperbound <= alpha:
        # 		return upperbound)
        # 	alpha = max(alpha, n.lowerbound);
        # 	beta = min(beta, node.upperbound)

        board_copy = copy.deepcopy(board)
        if self.my_move:
            board_copy.update(old_move, node, self.marker)
        else:
            board_copy.update(old_move, node, self.marker)

        # board_copy.print_board()
        # print
        children = self.get_children(board_copy, node)
        _nth_sibling = len(children)

        # Node is a leaf node
        if (d == 0) or (_nth_sibling == 0):
            g = self.evaluate(old_move, node, board_copy)
        # print g
        # board_copy.print_board()
        # print "hello"
        # g = random.randint(-100, 101)

        elif self.my_move:
            # Mark current node as taken by us for future reference
            g = -self.INFINITY

            # Save original alpha value
            a = alpha
            i = 0

            while (g < beta) and (i < _nth_sibling):
                self.my_move = False
                c = children[i]
                g = max(g, self.node_beta(c, a, beta, d - 1, board_copy, node))
                a = max(a, g)
                i = i + 1

        # Node is a min node
        else:
            # Mark current node as taken by opponent for future reference
            g = self.INFINITY

            # Save original beta value
            b = beta
            i = 0

            while (g > alpha) and (i < _nth_sibling):
                self.my_move = True
                c = children[i]
                g = min(g, self.node_beta(c, alpha, b, d - 1, board_copy, node))
                b = min(b, g)
                i = i + 1

        del board_copy
        return g

    def IDS(self, root, board, old_move):
        _first_guess = 0
        # for d in range(1, self.maxSearchDepth):
        boardCopy = copy.deepcopy(board)
        _first_guess = self._MTDf(root, _first_guess, self.maxSearchDepth, boardCopy, old_move)
        # if timeUp:
        #    break
        del boardCopy
        return _first_guess, root

    def selectRandom(self, li):
        """
        generate a random integer
        :param li:
        :return:
        """
        ln = len(li)
        r = random.randrange(0, ln)
        return li[r]

    def isWinner(self, bo, le):
        """
        check to determine  the  winner
        :param bo:
        :param le:
        :return:
        """
        return (bo[9] == le and bo[10] == le and bo[11] == le and bo[12] == le) or \
               (bo[5] == le and bo[6] == le and bo[7] == le and bo[8] == le) or \
               (bo[1] == le and bo[2] == le and bo[3] == le and bo[4] == le) or \
               (bo[13] == le and bo[14] == le and bo[15] == le and bo[16] == le) or \
               (bo[1] == le and bo[6] == le and bo[11] == le and bo[16] == le) or \
               (bo[1] == le and bo[5] == le and bo[9] == le and bo[13] == le) or \
               (bo[2] == le and bo[6] == le and bo[10] == le and bo[14] == le) or \
               (bo[4] == le and bo[8] == le and bo[12] == le and bo[16] == le) or \
               (bo[4] == le and bo[7] == le and bo[10] == le and bo[13] == le)

    def intelligent_agent(self):
        """
        Move made by the intelligent agent
        starts by checking for available moves
        :return:
        """
        possible_moves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
        move = 0

        # check for the available turns [X, O]
        for let in ['O', 'X']:
            for i in possible_moves:
                board_copy = board[:]
                board_copy[i] = let
                if self.isWinner(board_copy, let):
                    move = i
                    return move

        corners_open = []
        # loop through the available moves
        for i in possible_moves:
            if i in [1, 3, 7, 9]:
                corners_open.append(i)
            else:
                corners_open.append(i)

        if len(corners_open) > 0:
            move = self.selectRandom(corners_open)
            return move

        if 5 in possible_moves:
            move = 5
            return move

        # check for the open edges
        edges_open = []
        for i in possible_moves:
            if i in [2, 4, 6, 8]:
                edges_open.append(i)

        if len(edges_open) > 0:
            move = self.selectRandom(edges_open)

        return move


class Player(Intelligent_Player):
    """A player defines the interface needed to play a game.

    The only requirement is to be able to take a board and return
    a (legally) modified board.
    """

    def __init__(self):
        super().__init__()
        self.player = 0
        self.game_board_state = [' ' for _x in range(17)]

    def play(self, game_board_state, player_n):
        """
        update the board with the current state and the player of the game
        :param game_board_state:
        :param player_n:
        :return:
        """
        self.player = player_n
        self.game_board_state = game_board_state
        return self.intelligent_agent()

