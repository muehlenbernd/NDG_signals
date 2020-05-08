import random

class Agent:

    ####### constructor #######
    def __init__(self, type, dap, sigA_prob, initial_strategy = [-1,-1], signal_costs = [0.0,0.0]):

        # agent's type and agent's disagreement point (dap)
        self.type = type
        self.dap = dap

        # conditional strategy what to do when receive signal 1 or signal 2
        self.strategy = initial_strategy
        if initial_strategy == [-1,-1]:
            self.strategy = [random.randint(0,2), random.randint(0,2)]

        # the agent's last choice (L:0, M:1, H:2) and last plays's utility
        self.current_utility = 0.0
        self.current_choice = -1

        # an agent's accumulated utility for a number of plays
        self.accumulated_utility = 0.0

        # an agent's accumulated utility for a number of plays without dap score
        self.accumulated_bargain = 0.0

        # an agent's accumulated utility for a number of plays of only dap score
        self.accumulated_dap = 0.0

        # an agent's probability to send signal A
        self.sigA_prob = sigA_prob

        # signal costs for different signals
        self.signal_costs = signal_costs


    def interact(self, opponent, game):

        # produce my signal
        my_sigA = random.random()
        if my_sigA < self.sigA_prob:
            my_signal = 0
        else:
            my_signal = 1

        # produce opponent signal
        op_sigA = random.random()
        if op_sigA < opponent.sigA_prob:
            op_signal = 0
        else:
            op_signal = 1


        # play conditional strategy based on the signal of the opponent
        self.current_choice = self.strategy[op_signal]
        opponent.current_choice = opponent.strategy[my_signal]

        # compute current utility
        self.current_utility = max(game.utility[self.current_choice][opponent.current_choice],self.dap)

        # reduce utility by signal costs
        self.current_utility = self.current_utility - self.signal_costs[my_signal]

        # update accumulated reward values
        self.accumulated_utility += self.current_utility
        self.accumulated_bargain += game.utility[self.current_choice][opponent.current_choice]
        if game.utility[self.current_choice][opponent.current_choice] == 0:
            self.accumulated_dap += self.dap



    def reset(self):

        # reset accumulated reward values
        self.accumulated_utility = 0.0
        self.accumulated_bargain = 0.0
        self.accumulated_dap = 0.0

