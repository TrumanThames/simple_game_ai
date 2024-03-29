import random
import sys
import copy
import pickle
from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation
import tictactoe as ttt


PLAYER = 1


class tictactoe_agent(Agent):
    lastAction = Action()  #
    lastObservation = Observation()  #
    randGenerator = random.Random()
    stepsize = 0.1
    epsilon = 0.1
    gamma = 1
    numStates = 0
    numActions = 0
    value_function = None
    player = PLAYER

    policyFrozen = False
    exploringFrozen = False

    def agent_init(self):
        self.lastAction = Action()
        self.lastObservation = Observation()

    def egreedy(self, state):
        numActions = len(state[0])
        if not self.exploringFrozen and self.randGenerator.random() < self.epsilon:
            return self.randGenerator.randint(0, numActions - 1)
        return self.value_function[state].index(max(self.value_function[state]))

    def agent_start(self, observation):
        moves = observation.intArray[2:]
        turn = observation.intArray[0]
        board = observation.intArray[1]
        assert self.player == turn, "It needs to be this agent's turn for it to make a move"
        theState = (moves, board, turn, self.player)
        thisIntAction: int = self.egreedy(theState)
        returnAction = Action()
        returnAction.intArray = [thisIntAction]

        self.lastAction = copy.deepcopy(returnAction)
        self.lastObservation = copy.deepcopy(observation)

        return returnAction

    def agent_step(self, reward, observation: Observation):
        moves = observation.intArray[2:]
        turn = observation.intArray[0]
        board = observation.intArray[1]
        newState = (tuple(moves), board, turn, self.player)
        lastState = (tuple(self.lastObservation.intArray[2:]), self.lastObservation.intArray[1],
                     self.lastObservation.intArray[0], self.player)
        lastAction = self.lastAction.intArray[0]
        newIntAction = self.egreedy(newState)
        Q_sa = self.value_function[lastState][lastAction]
        Q_sprime_aprime = self.value_function[newState][newIntAction]
        new_Q_sa = Q_sa + self.stepsize * (reward + self.gamma * Q_sprime_aprime - Q_sa)
        if not self.policyFrozen:
            self.value_function[lastState][lastAction] = new_Q_sa
        returnAction = Action()
        returnAction.intArray = [newIntAction]
        self.lastAction = copy.deepcopy(returnAction)
        self.lastObservation = copy.deepcopy(observation)

        return returnAction

    def agent_end(self, reward):
        moves = self.lastObservation.intArray[2:]
        turn = self.lastObservation.intArray[0]
        board = self.lastObservation.intArray[1]
        lastState = (moves, board,
                     turn, self.player)
        lastAction = self.lastAction.intArray[0]
        Q_sa = self.value_function[lastState][lastAction]
        new_Q_sa = Q_sa + self.stepsize * (reward - Q_sa)

        if not self.policyFrozen:
            self.value_function[lastState][lastAction] = new_Q_sa

    def agent_cleanup(self):
        pass

    def save_value_function(self, fileName):
        theFile = open(fileName, "w")
        pickle.dump(self.value_function, theFile)
        theFile.close()

    def load_value_function(self, fileName):
        theFile = open(fileName, "r")
        self.value_function = pickle.load(theFile)
        theFile.close()

    def agent_message(self, inMessage):

        #	Message Description
        # 'freeze learning'
        # Action: Set flag to stop updating policy
        #
        if inMessage.startswith("freeze learning"):
            self.policyFrozen = True
            return "message understood, policy frozen"

        #	Message Description
        # unfreeze learning
        # Action: Set flag to resume updating policy
        #
        if inMessage.startswith("unfreeze learning"):
            self.policyFrozen = False
            return "message understood, policy unfrozen"

        # Message Description
        # freeze exploring
        # Action: Set flag to stop exploring (greedy actions only)
        #
        if inMessage.startswith("freeze exploring"):
            self.exploringFrozen = True
            return "message understood, exploring frozen"

        # Message Description
        # unfreeze exploring
        # Action: Set flag to resume exploring (e-greedy actions)
        #
        if inMessage.startswith("unfreeze exploring"):
            self.exploringFrozen = False
            return "message understood, exploring frozen"


if __name__ == '__main__':
    AgentLoader.loadAgent(tictactoe_agent())
