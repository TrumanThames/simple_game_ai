import random
import sys
from rlglue.environment.Environment import Environment
from rlglue.environment import EnvironmentLoader as EnvironmentLoader
from rlglue.types import Observation
from rlglue.types import Action
from rlglue.types import Reward_observation_terminal
import tictactoe

class tictacttoe_environment(Environment):
    randGenerator = random.Random()

    def env_init(self, dim, n):
        self.GameBoard = tictactoe.GameBoard(dim, n)
        return "VERSION RL-Glue-3.0"

    def env_start(self):
        returnObs = Observation()
        returnObs.intArray = [self.GameBoard.flatten_obs()]

        return returnObs

    def env_step(self, thisAction):
        assert len(thisAction.intArray) == 1, "Expected 1 action"

        self.updateBoard(thisAction.intArray[0])

        theObs = Observation()
        theObs.intArray = [self.GameBoard.flatten_obs()]
        returnRO = Reward_observation_terminal()
        returnRO.r = self.calculateReward()
        returnRO.o = theObs
        returnRO.terminal = self.checkCurrentTerminal()

        return returnRO

    def env_cleanup(self):
        pass

    def env_message(self, inMessage):
        #	Message Description
        #	'print-state'
        #	Action: Print the map and the current agent location
        if inMessage.startswith("print-state"):
            self.printState()
            return "Message understood.  Printed the state."

        return "SamplesMinesEnvironment(Python) does not respond to that message."

    def updateBoard(self, move):
        self.GameBoard.move(move, shush=True)

    def calculateReward(self):
        if self.GameBoard.over:
            if self.GameBoard.winner == 0:
                return 0
            if self.GameBoard.winner == 1:
                return 1000
            if self.GameBoard.winner == 2:
                return -1000
        return -.2

    def printState(self):
        self.GameBoard.show_board(silly=False)
        return


if __name__ == '__main__':
    EnvironmentLoader.loadEnvironment(tictacttoe_environment())

