import tictactoe
import random




class RandomAI:
    def __init__(self, seed):
        self.seed = seed

    def make_move(self, GB : tictactoe.GameBoard):
        if GB.over:
            print("It's game over man, game over")
            return
        return (random.sample(GB.moves, 1))[0]


def play_a_game(agent1, agent2, dim, n):
    GB = tictactoe.GameBoard(dim, n)
    while GB.winner == 0 and not GB.over:
        GB.move(agent1.make_move(GB), shush=False)
        if GB.winner != 0 or GB.over:
            break
        GB.move(agent2.make_move(GB), shush=False)
    GB.show_board(silly=False)
    if GB.winner == 0:
        print("It's game over man, game over...")
    else:
        print("The winner was "+str(GB.winner))
    print(GB.iboard)
    return GB.iboard
