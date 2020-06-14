from AgentDiversity import *
from Experiment import *
import numpy as np
import random


class ParameterSet:

    # constructor #######
    def __init__(self, size_blue, size_red, ndg):

        self.ndg = ndg                  # game matrix
        self.disagreement = 0.4         # disagreement point for Blue agents
        self.sig_dim = 2                # number of dimensions of signal
        self.sig_fid = 1                # signal fidelity, now deprecated
        self.typeSigCorr = 1.0          # probability of fixed trait to signal mapping
        self.plasticity = 1.0           # how fast you imitate tolerance
        self.tolerance = 1.0            # initial tolerance for everyone
        self.run_time = 500            # number of rounds in each iterated NDG
        self.num_experiments = 10        # number repetitions of each iterated NDG
        self.mutationRate = 0.0001      # mutation rate
        self.sizeBlue = size_blue       # number of Blue agents
        self.sizeRed = size_red         # number of Red agents
        self.results = []               # store each experiment in here in sequence
        # self.roundSize = (size_blue + size_red) * (size_blue + size_red - 1)
        self.redTolSeq = []
        self.resultsSummaryStats = []
        self.print_round_results = False

    # method list
    # def create_agents(self):
    # def imitate_mutate(self, agent, index, agents, experiment):
    # def simulate_round(self, current_round, agents, experiment, print_round_results=True):
    # def simulate(self):

    # initialise all the agents for this iterated game
    def create_agents(self):

        # create a population of agents with random strategies
        agents = []

        # build all the blue agents first
        for dummy in range(self.sizeBlue):
            # strat is the conditional strategy function
            strat = np.random.randint(0, 3, 2)

            # sig is a random vector in the unit cube of dimension sig_dim
            sig = np.random.rand(self.sig_dim)

            # except the first dimension is fixed, Blue = 0 , Red=1
            sig[0] = 0

            # blue agent is agent type, disagreement point, signal, list of strategies
            agents.append(Agent(0, self.disagreement, sig, self.sig_fid, self.sig_dim, strat, self.typeSigCorr, self.tolerance, self.plasticity))

        # now build all the red agents
        for dummy in range(self.sizeRed):
            # strat is the conditional strategy function
            strat = np.random.randint(0, 3, 2)

            # sig is a random vector in the unit cube of dimension sig_dim
            sig = np.random.rand(self.sig_dim)

            # except the first dimension is a prob of signalling to type
            sig[0] = 1

            # red agent is agent type, disagreement point (0), signal, list of strategies
            agents.append(Agent(1, 0.0, sig, self.sig_fid, self.sig_dim, strat, self.typeSigCorr, self.tolerance, self.plasticity))

        return agents

    # after having played all the agents can choose to mutate or imitate
    def imitate_mutate(self, agent, index, agents, experiment):

        if index < self.sizeBlue:
            op_agent = random.choice(agents[0:self.sizeBlue - 1])
        else:
            op_agent = random.choice(agents[self.sizeBlue:])

        # imitate the other agent if scored better with probability of score difference
        if op_agent.accumulated_utility > agent.accumulated_utility:

            # normaliser is 60% of the number of agents, not sure why
            diff = (op_agent.accumulated_utility - agent.accumulated_utility) / experiment.normalizer

            # with some chance that increases the larger the difference is in accumulated resources
            prob = random.random()
            if prob < diff:
                # copy the strategy and signal of the other agent
                agent.strategy = op_agent.strategy
                agent.sig[1:] = op_agent.sig[1:]
                # move your tolerance level closer to the tolerance level of the other agent
                agent.tol = agent.tol + agent.plasticity * (op_agent.tol - agent.tol)

    # simulate a single round of the NDG
    def simulate_round(self, current_round, agents, experiment, print_round_results=True):

        if print_round_results:
            print()
            print("ROUND", current_round)

        # resetting and mutation
        for agent in agents:

            # reset each agent
            agent.reset()

            # apply mutation
            if random.random() < self.mutationRate:
                agent.mutate()

        # so you can track the place of the agent in the sequence
        agent1Index = 0

        # increment the reward lists with another list
        experiment.rewardB.append([])
        experiment.rewardR.append([])
        experiment.bidsB.append([])
        experiment.bidsR.append([])

        # interaction
        # I have changed this so that we don't run all agent pairs twice, but only once
        for agent1 in agents:
            agent2Index = 0  # agent1Index+1
            # we only need to take the agents that are after agent 1
            for agent2 in agents:  # [agent1Index+1:]:
                if agent1 != agent2:
                    agent1.interact(agent2, self.ndg)

                    # record the bids and rewards
                    experiment.update(agent1, agent2, agent1Index, agent2Index, current_round, self.run_time)

                agent2Index += 1  # update the indices
            agent1Index += 1

        experiment.round_update(agents, self)

        # calculate and print the mean rewards for blue and red this round
        #blueRSeq = np.array(experiment.rewardB[-1])
        #bRunMean = np.mean(blueRSeq)
        #print("blue mean reward", bRunMean)
        #redRSeq = np.array(experiment.rewardR[-1])
        #rRunMean = np.mean(redRSeq)
        #print("red mean reward", rRunMean)

        # imitation
        for index in range(len(agents)):

            # pick current indexed agent and opponent of same type
            agent = agents[index]

            self.imitate_mutate(agent, index, agents, experiment)

    # run several experiments, each with several rounds according to the parameter settings in self
    def simulate(self):

        # start experiments
        for exp in range(self.num_experiments):

            # create a new experiment instance
            experiment = Experiment(self.run_time, self.sizeBlue, self.sizeRed)

            print("Experiment: ", exp, "\t")

            agents = self.create_agents()

            # normalizer for accumulated utility
            # why 0.6?
            experiment.normalizer = 0.6 * (len(agents) - 1)

            # run the algorithm
            # for each round from 1000
            for current_round in range(self.run_time):
                self.simulate_round(current_round, agents, experiment, self.print_round_results)

            self.results.append(experiment)

    # analysis method
    def analysis(self):

        stratDist = np.zeros([2, 3, self.num_experiments])

        for exp in range(0, self.num_experiments):

            # print("Final simulation step, signal vectors for all blue agents")
            # print(self.results[exp].blueSigSeq[-1])
            # print("Final simulation step, signal vectors for all red agents")
            # print(self.results[exp].redSigSeq[-1])

            # print("Final simulation step, conditional strategy, all blue agents")
            for agent in range(0, self.sizeBlue):
                # print("tolerance", self.results[exp].blueTolSeq[-1][agent], " t ", self.results[exp].blueStratSeq[-1][agent][0], ", not t ", self.results[exp].blueStratSeq[-1][agent][1])
                # recover the conditional strategy [0=L, 1=M, 3=H] for opponents within the tolerance threshold
                stratTol = self.results[exp].blueStratSeq[-1][agent, 0]
                # and for opponents beyond the tolerance threshold
                stratNotTol = self.results[exp].blueStratSeq[-1][agent, 1]
                # increment the right elements of strategy count matrix
                stratDist[0][stratTol][exp] += 1
                stratDist[1][stratNotTol][exp] += 1

            # print("Final simulation step, conditional strategy, all red agents")
            for agent in range(0, self.sizeRed):
                # print("tolerance", self.results[exp].redTolSeq[-1][agent], "t ", self.results[exp].redStratSeq[-1][agent][0], ", not t ", self.results[exp].redStratSeq[-1][agent][1])
                # same as above, but for red agents
                stratTol = self.results[exp].redStratSeq[-1][agent, 0]
                stratNotTol = self.results[exp].redStratSeq[-1][agent, 1]
                # all red and blue agents' strategies are counted together
                stratDist[0][stratTol][exp] += 1
                stratDist[1][stratNotTol][exp] += 1

            # print("strategy distribution ", stratDist[:, :, exp])

            # print("interaction history ", self.results[exp].InteractArray)
            # print("last interaction")
            # print(self.results[exp].InteractArray[-1, :, :])

            # we can test for ProBlue
            ProBlueB = np.ones([1, self.sizeBlue, self.sizeRed]) * 2        # this is a matrix of H bids
            ProBlueR = np.zeros([1, self.sizeRed, self.sizeBlue])           # this is a matrix of L bids

            testProBlueB = np.all(self.results[exp].InteractArray[-1, :self.sizeBlue, self.sizeBlue:] == ProBlueB)  # Blues all bid H against Reds
            testProBlueR = np.all(self.results[exp].InteractArray[-1, self.sizeBlue:, :self.sizeBlue] == ProBlueR)  # Reds all bid L against Blues
            # print("all blues bid H = ", testProBlueB, " all reds bid L = ", testProBlueR)

            # we can test for ProRed
            ProRedB = np.zeros([1, self.sizeBlue, self.sizeRed])   # this is a matrix of L bids
            ProRedR = np.ones([1, self.sizeRed, self.sizeBlue]) * 2 # this is a matrix of H bids

            testProRedB = np.all(self.results[exp].InteractArray[-1, :self.sizeBlue, self.sizeBlue:] == ProRedB)  # Blues all bid L against Reds
            testProRedR = np.all(self.results[exp].InteractArray[-1, self.sizeBlue:, :self.sizeBlue] == ProRedR)  # Reds all bid H against Blues
            # print("all blues bid L = ", testProRedB, " all reds bid H = ", testProRedR)

            # we can test for Fair
            FairB = np.ones([1, self.sizeBlue, self.sizeRed])   # this is a matrix of M bids
            FairR = np.ones([1, self.sizeRed, self.sizeBlue])   # this is a matrix of M bids

            testFairB = np.all(self.results[exp].InteractArray[-1, :self.sizeBlue, self.sizeBlue:] == FairB)  # Blues all bid M against Reds
            testFairR = np.all(self.results[exp].InteractArray[-1, self.sizeBlue:, :self.sizeBlue] == FairR)  # Reds all bid M against Blues
            # print("all blues bid M = ", testFairB, " all reds bid M = ", testFairR)

            if testProBlueB and testProBlueR:
                self.resultsSummaryStats.append("PB")
                print("PB")
            elif testProRedB and testProRedR:
                self.resultsSummaryStats.append("PR")
                print("PR")
            elif testFairB and testFairR:
                self.resultsSummaryStats.append("FA")
                print("FA")
            else:
                self.resultsSummaryStats.append("OT")
                print("OT")



