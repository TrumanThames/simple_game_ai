import numpy as np
import time


def rec_make_board(dim: int, n: int):
    return np.zeros([n]*dim, dtype=int)


def compose(M, dim, n):
    compost = [0]*dim
    move = M
    for i in range(dim):
        compost[i] = move % n
        move = int(move/n)
    return tuple(compost)


def winsfrom(start, dim, n):
    wins = set()
    zeros = {i if start[i] == 0 or start[i] == n-1 else None for i in range(dim)}
    zeros.discard(None)
    Z = list(zeros)
    dictZ = {Z[i]: i for i in range(len(Z))}
    delta_start = [0]*len(zeros)
    end = [-1]*dim
    if len(zeros) == 0:
        return set()
    for i in range(1, 2**len(zeros)):
        config = i
        for k in range(len(zeros)):
            delta_start[k] = config % 2
            config = config >> 1
        for j in range(dim):
            if start[j] == 0:
                if delta_start[dictZ[j]] == 1:
                    end[j] = n-1
                else:
                    end[j] = start[j]
            elif start[j] == n-1:
                if delta_start[dictZ[j]] == 1:
                    end[j] = 0
                else:
                    end[j] = start[j]
            else:
                end[j] = start[j]
        win = tuple(start), tuple(end)
        if win[0] < win[1]:
            wins.add((win[0], win[1]))
        else:
            wins.add((win[1], win[0]))
    return wins


def winning_sets(dim, n):
    # how many ways are there to have
    # at least one zero in an n-tuple
    win_sets = set()
    startmove = np.array([5]*dim)
    for firstzero in range(dim):
        startmove[firstzero] = 0
        for i in range((n-1)**firstzero):
            bef = i
            for j in range(n**(dim - firstzero - 1)):
                aft = j
                for k in range(dim):
                    if k < firstzero:
                        startmove[k] = (bef % (n-1))+1
                        bef = int(bef/(n-1))
                    elif k > firstzero:
                        startmove[k] = aft % n
                        aft = int(aft/n)
                    #print(bef) # should always be zero here
                #print(aft) # should always be zero here
                win_sets.update(winsfrom(startmove, dim, n))
    return win_sets


def isgood(direction, move, n):
    #print(direction)
    movers = {i if direction[i] != 0 else None for i in range(len(direction))}
    movers.discard(None)
    oob = 0
    for ind in movers:
        if move[ind] >= n or move[ind] < 0:
            oob += 1
    if oob % len(movers) != 0:
        return False
    return True


def did_won(board, dim, n, move):
    plyr = board[move]
    npmove = np.array(move)
    direction = np.array([0]*dim)
    for i in range(1, 3**dim):
        config = i
        for j in range(dim):
            direction[j] = -1 if (config % 3) == 2 else config % 3
            config = int(config/3)
        #print(direction)
        for j in range(n):
            if not isgood(direction, npmove+(direction*j), n):
                #print(move, direction, npmove+(direction*j))
                break
            if board[tuple((npmove+(direction*j)) % n)] != plyr:
                break
            elif j == n-1:
                return True
    return False


def flatten_board(board, dim, n):
    iboard = 0
    indx = [0]*dim
    for i in range(n**dim):
        j = i
        for d in range(dim):
            indx[d] = j % n
            j = int(j/n)
        iboard += board[tuple(indx)] * (3 ** i)
    return iboard


def expand_board(iboard, dim, n):
    board = np.zeros([n]*dim, dtype=int)
    indx = [0]*dim
    for i in range(n**dim):
        j = i
        for d in range(dim):
            indx[d] = j % n
            j = int(j/n)
        board[tuple(indx)] = int(iboard / (3 ** i)) % 3
    return board


def index(i, dim, n):
    indx = [0]*dim
    j = i
    for d in range(dim):
        indx[d] = j % n
        j = int(j / n)
    return indx


def inv_index(indx, dim, n):
    i = 0
    for d in range(dim):
        i += indx[d]*(n**d)
    return i


def imove(m0, dim, n, turn):
    return turn*(3**inv_index(m0, dim, n))


class GameBoard:
    def __init__(self, dim, n):
        self.dim = dim
        self.n = n
        self.board = rec_make_board(dim, n)
        self.turn = 1
        self.moves = {compose(i, dim, n) for i in range(n**dim)}
        self.iboard = 0
        self.winner = 0
        self.over = False
        self.winning_sets = winning_sets(dim, n)

    def flatten_obs(self):
        [self.turn, self.iboard]+sorted(list(self.moves))

    def show_board(self, silly=True):
        if self.dim == 1:
            print(self.board)
        if self.dim == 2:
            for i in range(self.n):
                print(self.board[i])
        if self.dim > 2:
            if silly:
                print("Oh Gosh, you want me to show you a high dimensional tictactoe board? Well, I'll try, "
                      "hhhnnnnnnnggghghgggggg, *pants* *pants* (where are your pants, did you forget to put them on "
                      "this morning?) HNNNNNNNNNNGGHGHGGGGGGHGGNNNNGGGHG, Oh no, I can't. I'm sorry, I tried my "
                      "darnedest")
                time.sleep(2)
                print("WAIT, WAIT! Don't let me die just yet! Let me give it another go")
                time.sleep(1)
            for i in range(self.n):
                print(self.board[i])
            if silly:
                time.sleep(1)
                print("\n\nWell, that's the best I've got")
        print("It is player "+str(self.turn)+"'s turn")
        return

    def move(self, m0, shush=False):
        if m0 == None:
            self.turn = 3-self.turn
        if isinstance(m0, type(42)):
            m0 = index(m0, self.dim, self.n)
        if not shush:
            print("Player "+str(self.turn)+" is making a move, the result of that move is")
        assert (len(m0) == self.dim), "INVALID MOVE: dimension mismatch"
        assert (self.board[m0] == 0), "INVALID MOVE: not a free space"
        self.board[m0] = self.turn
        self.iboard += imove(m0, self.dim, self.n, self.turn)
        if self.winner == 0:  # One can only win, when nobody has won yet
            if did_won(self.board, self.dim, self.n, m0):
                if not shush:
                    print("Player "+str(self.turn)+" has won the game!!!!!!!")
                self.over = True
                self.winner = self.turn
        self.moves.remove(m0)
        self.turn = 3-self.turn
        if len(self.moves) == 0:
            self.over = True
            if not shush:
                print("It's game over man, it's game over")
        self.show_board(silly=False)
        return


def configurate(config, dim, n):
    board = np.zeros([n]*dim, dtype=int)
    return


class Q_Matrix:
    def __init__(self, dim, n, player):
        self.dim = dim
        self.n = n
        self.player = player

    def val_state(self, GB: GameBoard):
        if GB.winner == self.player:
            return 10000
        if GB.winner == 0:
            return 0


def win_player(board, player):
    pass
