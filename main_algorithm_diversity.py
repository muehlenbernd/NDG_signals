import numpy as np
from AgentDiversity import *
from Game import *
from Experiment import *
import random

# import Ext_functions as ext

# set the game by defining the L value
NDG = Game(0.4)

# set the disagreement point
disagreement = 0.3

# signal dimension
# first dimension is always fixed
# other dimensions are between 0,1
sig_dim = 2
# number of quantised values with which the strategy matrix tracks the signal
sig_fid = 10

# set the mutation rate
mutation_rate = 0.0001

# set the maximum runtime
run_time = 100

# set the number of experiments
num_experiments = 1

print_round_results = True

# set the population size
size_Blue = 50
size_Red = 50

# store the results here
results = []

# start experiments
for exp in range(num_experiments):

    # create a new experiment instance
    experiment = Experiment(run_time, size_Blue, size_Red)

    print("Experiment: ", exp, "\t")

    # create a population of agents with random strategies
    agents = []

    # build all the blue agents first
    for dummy in range(size_Blue):

        # strat is the conditional strategy function
        strat = np.random.randint(0, 3, (2, sig_fid))

        # sig is a random vector in the unit cube of dimension sig_dim
        sig = np.random.rand(sig_dim)

        # except the first dimension is fixed, Blue = 0 , Red=1
        sig[0] = 0

        # blue agent is agent type, disagreement point, signal, list of strategies
        agents.append(Agent(0, disagreement, sig, sig_fid, sig_dim, strat))

    # now build all the red agents
    for dummy in range(size_Red):

        # strat is the conditional strategy function
        strat = np.random.randint(0, 3, (2, sig_fid))

        # sig is a random vector in the unit cube of dimension sig_dim
        sig = np.random.rand(sig_dim)

        # except the first dimension is fixed, Blue = 0 , Red=1
        sig[0] = 1

        # red agent is agent type, disagreement point (0), signal, list of strategies
        agents.append(Agent(1, 0.0, sig, sig_fid, sig_dim, strat))

    # normalizer for accumulated utility
    # why 0.6?
    normalizer = 0.6 * (len(agents) - 1)

    # run the algorithm
    # for each round from 1000
    for current_round in range(run_time):

        if print_round_results:
            print()
            print("ROUND", current_round)

        # resetting and mutation
        for agent in agents:

            # reset each agent
            agent.reset()

            # apply mutation
            if random.random() < mutation_rate:
                agent.mutate()

        # interaction
        # looks like all pairs of agents are run against each other in some way
        for agent1 in agents:
            for agent2 in agents:
                if agent1 != agent2:
                    agent1.interact(agent2, NDG)

                    # record the bids and rewards
                    experiment.update(agent1, agent2, agents)

        # imitation
        for index in range(len(agents)):

            # pick current indexed agent and opponent of same type
            agent = agents[index]
            if index < size_Blue:
                op_agent = random.choice(agents[0:size_Blue-1])
            else:
                op_agent = random.choice(agents[size_Blue:])

            # imitate the other agent if scored better with probability of score difference
            if op_agent.accumulated_utility > agent.accumulated_utility:

                # normaliser is 60% of the number of agents, not sure why
                diff = (op_agent.accumulated_utility-agent.accumulated_utility)/normalizer

                # with some chance that increases the larger the difference is in accumulated resources
                prob = random.random()
                if prob < diff:
                    # copy the strategy and signal of the other agent
                    agent.strategy = op_agent.strategy
                    agent.sig = op_agent.sig

    results.append(experiment)
    print("Blue rewards", results[exp].rewardB)
    print("Red rewards", results[exp].rewardR)

    print(results[exp].blueSigSeq[-1])
    print(results[exp].redSigSeq[-1])

    print(results[exp].blueStratSeq[-1][-1])

