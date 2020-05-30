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

    # method for appending rewards and bids to experimental results
    def update(self, agent1, agent2, agents):

        if agent1.type == 0:
            self.rewardB.append(agent1.current_utility)
            self.bidsB.append(agent1.current_choice)
        else:
            self.rewardR.append(agent1.current_utility)
            self.bidsR.append(agent1.current_choice)

        if agent2.type == 0:
            self.rewardB.append(agent2.current_utility)
            self.bidsB.append(agent2.current_choice)
        else:
            self.rewardR.append(agent2.current_utility)
            self.bidsR.append(agent2.current_choice)

        blue_sig = np.zeros(shape=(self.size_Blue, agent1.sig_dim))
        red_sig = np.zeros(shape=(self.size_Blue, agent1.sig_dim))

        CounterBlue = 0
        CounterRed = 0

        self.blueStratSeq.append([])
        self.redStratSeq.append([])
        self.blueTolSeq.append([])
        self.redTolSeq.append([])

        for agent in agents:
            if agent.type == 0:
                blue_sig[CounterBlue, :] = agent.sig
                self.blueStratSeq[-1].append(agent.strategy)
                self.blueTolSeq[-1].append(agent.tol)
                CounterBlue += 1
            else:
                red_sig[CounterRed, :] = agent.sig
                self.redStratSeq[-1].append(agent.strategy)
                self.redTolSeq[-1].append(agent.tol)
                CounterRed += 1

        self.blueSigSeq.append(blue_sig)
        self.redSigSeq.append(red_sig)
