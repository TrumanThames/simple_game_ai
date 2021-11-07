import sys
import rlglue.RLGlue as RLGlue

whichEpisode = 0


def runEpisode(stepLimit):
    global whichEpisode
    terminal = RLGlue.RL_episode(stepLimit)
    totalSteps = RLGlue.RL_num_steps()
    totalReward = RLGlue.RL_return()

    print("Episode " + str(whichEpisode) + "\t " + str(totalSteps) + " steps \t" + str(
        totalReward) + " total reward\t " + str(terminal) + " natural end")

    whichEpisode = whichEpisode + 1


print("\n\nExperiment starting up!")
taskSpec = RLGlue.RL_init()

print("RL_init called, the environment sent task spec: " + taskSpec)

print("\n\n----------Sending some sample messages----------")

#Talk to the agent and environment a bit...*/
responseMessage = RLGlue.RL_agent_message("what is your name?")
print("Agent responded to \"what is your name?\" with: " + responseMessage)

responseMessage = RLGlue.RL_agent_message("If at first you don't succeed; call it version 1.0")
print("Agent responded to \"If at first you don't succeed; call it version 1.0  \" with: " + responseMessage + "\n")

responseMessage = RLGlue.RL_env_message("what is your name?")
print("Environment responded to \"what is your name?\" with: " + responseMessage)
responseMessage = RLGlue.RL_env_message("If at first you don't succeed; call it version 1.0")
print("Environment responded to \"If at first you don't succeed; call it version 1.0  \" with: " + responseMessage)

print("\n\n----------Running a few episodes----------")
runEpisode(100)
runEpisode(100)
runEpisode(100)
runEpisode(100)
runEpisode(100)
