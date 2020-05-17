import random as rand
import math


class Agent:

    # constructor #######
    def __init__(self, type, dap, initial_sig, sig_fid, sig_dim, initial_strategy, signal_costs=[0.0, 0.0]):

        # agent's type and agent's disagreement point (dap)
        self.type = type
        self.dap = dap

        # conditional strategy what to do when receive signal 1 or signal 2
        self.strategy = initial_strategy

        # the agent's last choice (L:0, M:1, H:2) and last play's utility
        self.current_utility = 0.0
        self.current_choice = -1

        # an agent's accumulated utility for a number of plays
        self.accumulated_utility = 0.0

        # an agent's accumulated utility for a number of plays without dap score
        self.accumulated_bargain = 0.0

        # an agent's accumulated utility for a number of plays of only dap score
        self.accumulated_dap = 0.0

        # an agent's probability to send signal A
        self.sig = initial_sig
        self.sig_dim = sig_dim
        self.sig_fid = sig_fid

        # signal costs for different signals
        self.signal_costs = signal_costs

    # play against an opponent
    def interact(self, opponent, game):

        # play conditional strategy based on the signal of the opponent
        self.choose(opponent.sig)

        # opponent plays conditional strategy based on your signal
        opponent.choose(self.sig)

        # compute current utility
        self.current_utility = max(game.utility[self.current_choice][opponent.current_choice], self.dap)

        # update accumulated reward values
        self.accumulated_utility += self.current_utility
        self.accumulated_bargain += game.utility[self.current_choice][opponent.current_choice]
        if game.utility[self.current_choice][opponent.current_choice] == 0:
            self.accumulated_dap += self.dap

    # agent reset
    def reset(self):

        # reset accumulated reward values
        self.accumulated_utility = 0.0
        self.accumulated_bargain = 0.0
        self.accumulated_dap = 0.0

    # agent chooses strategy based on opponent signal
    def choose(self, op_signal):

        # strong assumption about the number of dimensions being two
        # the first index into the strategy array (fixed trait)
        # determined by the opponent signal
        # we simply use the index (0 or 1)
        index0 = int(op_signal[0])

        # the second index into the strategy array (plastic trait)
        index1 = int(math.floor(op_signal[1]) * self.sig_fid)

        # the choice is the strategy in that cell.
        self.current_choice = self.strategy[index0, index1]

    # mutate the strategy of the agent
    def mutate(self):

        # pick a random int for dim0
        index0 = rand.randint(0, 1)

        # pick a random int for dim1
        index1 = rand.randint(0, self.sig_fid - 1)

        # randomise that cell in the strategy array
        self.strategy[index0, index1] = rand.randint(0, 2)

        # don't include the fixed trait
        # when selecting a random trait to mutate
        index_sig = rand.randint(1, self.sig_dim - 1)

        # add uniform random noise between +/-0.1
        # keep the signal bounded between 0 and 1
        self.sig[index_sig] = min(1, max(0, self.sig[index_sig] + rand.uniform(-0.1, 0.1)))

