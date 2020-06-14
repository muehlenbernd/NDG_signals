import numpy as np


class Experiment:

    # constructor #######
    # (runtime, size_Blue, size_Red)
    def __init__(self, runtime, size_Blue, size_Red):

        self.runtime = runtime
        self.size_Blue = size_Blue
        self.size_Red = size_Red
        self.rewardB = []
        self.rewardR = []
        self.bidsB = []
        self.bidsR = []
        self.blueSigSeq = []
        self.redSigSeq = []
        self.blueStratSeq = []
        self.redStratSeq = []
        self.blueTolSeq = []
        self.redTolSeq = []
        self.InteractArray = np.zeros([runtime, size_Blue + size_Red, size_Blue + size_Red])
        self.normalizer = 0

    # method for appending rewards and bids to experimental results
    def update(self, agent1, agent2, agent1Index, agent2Index, current_round, num_rounds):

        if current_round == num_rounds-1:
            # print("agent ", agent1Index, " choice is ", agent1.current_choice)
            # print("agent ", agent1Index, " choice is ", agent1.current_choice)
            self.InteractArray[current_round, agent1Index, agent2Index] = agent1.current_choice
            self.InteractArray[current_round, agent2Index, agent1Index] = agent2.current_choice

        if agent1.type == 0:                                            # if agent1 is Blue
            self.rewardB[-1].append(agent1.current_utility)                 # append reward to Blue rewards
            self.bidsB[-1].append(int(agent1.current_choice))                    # append bids to list of blue bids
        else:                                                           # if agent1 is Red
            self.rewardR[-1].append(agent1.current_utility)                 # append reward to list of Red rewards
            self.bidsR[-1].append(int(agent1.current_choice))                    # append bid to list of red bids

        if agent2.type == 0:
            self.rewardB[-1].append(agent2.current_utility)
            self.bidsB[-1].append(int(agent2.current_choice))
        else:
            self.rewardR[-1].append(agent2.current_utility)
            self.bidsR[-1].append(int(agent2.current_choice))



    def round_update(self, agents, setup):

        blue_sig = np.zeros(shape=(self.size_Blue, setup.sig_dim))       # store blue signals
        red_sig = np.zeros(shape=(self.size_Red, setup.sig_dim))         # store red signals

        blue_strat = np.zeros([self.size_Blue, 2])                      # store blue strategies
        red_strat = np.zeros([self.size_Red, 2])

        blue_tol = np.zeros([self.size_Blue])                           # store blue tolerances
        red_tol = np.zeros([self.size_Red])

        CounterBlue = 0
        CounterRed = 0

        for agent in agents:
            if agent.type == 0:
                blue_sig[CounterBlue, :] = agent.sig                    # record the signal
                blue_strat[CounterBlue, :] = agent.strategy
                # self.blueStratSeq[-1].append(agent.strategy)            # record the blue strategy
                blue_tol[CounterBlue] = agent.tol
                # self.blueTolSeq[-1].append(agent.tol)                   # record the blue tolerance
                CounterBlue += 1
            else:
                red_sig[CounterRed, :] = agent.sig
                # self.redStratSeq[-1].append(agent.strategy)
                red_strat[CounterRed, :] = agent.strategy
                # self.redTolSeq[-1].append(agent.tol)
                red_tol[CounterRed] = agent.tol
                CounterRed += 1

        self.blueStratSeq.append(blue_strat.astype(int))
        self.redStratSeq.append(red_strat.astype(int))
        self.blueTolSeq.append(blue_tol)
        self.redTolSeq.append(red_tol)
        self.blueSigSeq.append(blue_sig)
        self.redSigSeq.append(red_sig)
