from Game import *
from Agent_old import *
import random

# import Ext_functions as ext

# set the game by defining the L value
NDG = Game(0.4)

# set the disagreement point
disagreement = 0.3

# set the fixed type who cannot change signal:
# 0: only Blues are fixed, 1: only Reds are fixed, 2: both are fixed, 3: none are fixed
fixed_type = 3

# set the mutation rate
mutation_rate = 0.0001

# set the maximum runtime
run_time = 1000

# set the number of experiments
num_experiments = 10

# set the population size
size_Blue = 50
size_Red = 50

# set if the round results shall be shown
print_round_results = False

# set the probabilities of signal use for both signals
signal_set = [0.0, 1.0]
# signal_set = [0.0, 0.25, 0.5, 0.75, 1.0]


# some lists for counting things
# this is a list of the strategy pairs from across the experiments
strategy_pair_list_total = []
# this is a count matrix for those strategy pairs
counter_pair_list_total = []
counter_type = [0, 0, 0, 0, 0]


print("EXP_ID \tRT \tCONV \tSTR_blue \tSIG_blue \tSTR_red \tSIG_red")

# start experiments
for exp in range(num_experiments):

    print("Experiment: ", exp, "\t")

    # create a population of agents with random strategies
    agents = []

    # build all the blue agents first
    for dummy in range(size_Blue):

        # s0 is the strategy conditional on receiving signal 0
        s0 = random.randint(0, 2)
        # s1 is the strategy conditional on receiving signal 1
        s1 = random.randint(0, 2)

        # prob_A is either 0.0 or 1.0, randomly selected from the list signal set
        prob_A = random.choice(signal_set)

        # if Blues have a fixed signal the blue signal is 1
        if fixed_type == 0 or fixed_type == 2:
    

        # blue agent is agent type, disagreement point, signal, list of strategies
        agents.append(Agent(0, disagreement, prob_A, [s0, s1]))

    # now build all the red agents
    for dummy in range(size_Red):
        s0 = random.randint(0, 2)
        s1 = random.randint(0, 2)
        prob_A = random.choice(signal_set)

        # if Reds have a fixed signal the red signal is 0
        if fixed_type == 1 or fixed_type == 2:
            prob_A = 0.0

        # red agent is agent type, disagreement point (0), signal, list of strategies
        agents.append(Agent(1, 0.0, prob_A, [s0, s1]))

    # normalizer for accumulated utility
    # why 0.6?
    normalizer = 0.6*(len(agents)-1)

    # run the algorithm
    # for each round from 1000
    for current_round in range(run_time):

        # some more lists for counting things
        # list and counts of strategies of blue agents
        strategy0_list = []
        counter0_list = []
        # list and counts of strategies of red agents
        strategy1_list = []
        counter1_list = []

        if print_round_results:
            print()
            print("ROUND", current_round)

        # resetting and mutation
        for agent in agents:

            # reset each agent
            agent.reset()

            # apply mutation
            if random.random() < mutation_rate:
                agent.strategy[0] = random.randint(0, 2)
                agent.strategy[1] = random.randint(0, 2)
                agent.sigA_prob = random.choice(signal_set)

                # de-randomise signal if we are in a fixed signal game
                # if it's a blue agent
                if agent.type == 0:
                    if fixed_type == 0 or fixed_type == 2:
                        agent.sigA_prob = 1.0
                # if it's a red agent
                elif agent.type == 1:
                    if fixed_type == 1 or fixed_type == 2:
                        agent.sigA_prob = 0.0

        # interaction
        # looks like all pairs of agents are run against each other in some way
        for agent1 in agents:
            for agent2 in agents:
                if agent1 != agent2:
                    agent1.interact(agent2, NDG)

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
                    agent.strategy[0] = op_agent.strategy[0]
                    agent.strategy[1] = op_agent.strategy[1]
                    agent.sigA_prob = op_agent.sigA_prob

            # recording the strategies played and how many of them are played
            # if it's a blue agent
            if index < len(agents)/2:
                # print(agent.strategy)
                # if the strategy is new
                if agent.strategy not in strategy0_list:
                    # add it to the list
                    strategy0_list.append(agent.strategy)
                    # add one instance of this strategy to your count
                    counter0_list.append(1)
                else:
                    # increment the count for the duplicate strategy
                    this_index = strategy0_list.index(agent.strategy)
                    # increment its count by one
                    counter0_list[this_index] += 1

            # if it's a red agent
            else:
                if agent.strategy not in strategy1_list:
                    strategy1_list.append(agent.strategy)
                    counter1_list.append(1)
                else:
                    this_index = strategy1_list.index(agent.strategy)
                    counter1_list[this_index] += 1

        # after a round: print the round results
        if print_round_results:

            # strategy0_list is the set of conditional strategies [2 item list]
            # played by blue agents
            print("Blue agent strategies")
            for entry in strategy0_list:
                print(entry, "\t")
            print("- \t")
            # strategy1_list is the set of conditional strategies [2 item list]
            # played by red agents
            print("Red agent strategies")
            for entry in strategy1_list:
                print(entry, "\t")
            print()

            # this is how many agents are playing each strategy
            # blue agents
            print('Blue, # of agents following conditional strategies')
            for entry in counter0_list:
                print(entry, "\t")
            print("- \t")
            # red agents
            print('Red, # of agents following conditional strategies')
            for entry in counter1_list:
                print(entry, "\t")
            print()

            # for index in range(round(len(agents)/2)):
            #    print(agents[index].strategy)  # round(agents[index].accumulated_utility,1))
            # print()
            # for index in range(round(len(agents)/2), len(agents)):
            #    print(agents[index].strategy)  # round(agents[index].accumulated_utility,1))
            # print()

        # after a round
        # record all the signals of blue agents
        new0_signals = []
        # all signals of red agents
        new1_signals = []
        for agent in agents:
            if agent.type == 0:
                new0_signals.append(agent.sigA_prob)
            else:
                new1_signals.append(agent.sigA_prob)

        # all the agents have the same signal
        same_sig = False
        # same_strategyF is true if all agents play M (fair convention)
        same_strategyF = False
        # same_strategyB is true if all Blues play H and all Reds play L (unconditional pro-Blue convention)
        same_strategyB = False

        # if the signals are all 0 for both blue and red
        if sum(new0_signals)/len(new0_signals) == 0.0 and sum(new1_signals)/len(new1_signals) == 0.0:
            same_sig = True
            same_strategyF = True
            same_strategyB = True
            # for each novel set of conditional strategies
            # for blue agents
            for entry in strategy0_list:
                # since everyone is signalling 1 we only have to analyse the conditional
                # conditional strategy with respect to those who signal 1
                # same_strategyF becomes false if the conditional
                # strategy is unfair (!=1 ie either L or H) when bidding against agents who signal 1
                if entry[1] != 1:
                    same_strategyF = False
                # and same_strategyB becomes false if the conditional strategy
                # of the blue agents is not 2 (H)
                if entry[1] != 2:
                    same_strategyB = False

            # for red agents
            # same_strategyF becomes false if the conditional
            # strategy is unfair (!=1, ie. L or H) when bidding against agents who signal 1
            for entry in strategy1_list:
                if entry[1] != 1:
                    same_strategyF = False
                # and same_strategyB becomes false if the conditional strategy
                # of the red agents is not 0 (L)
                if entry[1] != 0:
                    same_strategyB = False

        # if the signals are all 1 for blue and red
        elif sum(new0_signals) / len(new0_signals) == 1.0 and sum(new1_signals) / len(new1_signals) == 1.0:
            same_sig = True
            same_strategyF = True
            same_strategyB = True
            # same analysis as above
            # since everyone is signalling 0 we only have to analyse the conditional
            # conditional strategy with respect to those who signal 0, hence entry[0]
            for entry in strategy0_list:
                if entry[0] != 1:
                    same_strategyF = False
                if entry[0] != 2:
                    same_strategyB = False
            for entry in strategy1_list:
                if entry[0] != 1:
                    same_strategyF = False
                if entry[0] != 0:
                    same_strategyB = False

        # after a round: if one of the break conditions is fulfilled, break and print results
        if (len(strategy0_list) == 1 and len(strategy1_list) == 1) or current_round == run_time-1 or (same_sig and (same_strategyF or same_strategyB)):

            print("Break condition fulfilled round: ", current_round, "\t")

            # strategies played by Blues
            new0_list = []
            # strategies played by Reds
            new1_list = []

            # find all the unique strategies for blue agents
            for entry in strategy0_list:
                if entry not in new0_list:
                    new0_list.append(entry)

            # find all the unique strategies for red agents
            for entry in strategy1_list:
                if entry not in new1_list:
                    new1_list.append(entry)

            # different bidding strategies converged too
            print("CB: conditional pro-Blue convention (Blues play M with each other, H with Reds)")
            print("CR: conditional pro-Red convention")
            print("F: fair convention")
            print("B: unconditional pro-Blue convention (Blues play H with themselves and with Reds)")
            print("X: some other state")
            print()

            if (new0_list == [[2, 1]] and new1_list == [[1, 0]]) or (new0_list == [[1, 2]] and new1_list == [[0, 1]]):

                print("Game converged to: CB", "\t")
                counter_type[2] += 1

            elif (new0_list == [[1, 0]] and new1_list == [[2, 1]]) or (new0_list == [[0, 1]] and new1_list == [[1, 2]]):

                print("Game converged to: CR", "\t")
                counter_type[3] += 1

            elif (new0_list == [[1, 1]] and new1_list == [[1, 1]]) or (same_sig and (same_strategyF or same_strategyB)):

                if same_strategyF or (new0_list == [[1, 1]] and new1_list == [[1, 1]]):
                    print("Game converged to: F", "\t")
                    counter_type[0] += 1
                elif same_strategyB:
                    print("Game converged to: B", "\t")
                    counter_type[1] += 1
            else:
                print("Game converged to: X", "\t")
                counter_type[4] += 1

            print("Blue strategies", new0_list, "\t", "proportion of blue signalling 1 ", round(sum(new0_signals) / len(new0_signals), 2), "\t- \t")

            print("Red strategies", new1_list, "\t", "proportion of red signalling 1 ", round(sum(new1_signals) / len(new1_signals), 2))

            # the final blue strategies and then final red strategies
            final_pair = [strategy0_list[0], strategy1_list[0]]

            # check whether this final strategy pair has appeared at the
            # end of a previous experiment
            if final_pair not in strategy_pair_list_total:
                # if it hasn't append it and create a count of 1 for it
                strategy_pair_list_total.append(final_pair)
                counter_pair_list_total.append(1)
            else:
                # if it has just increment the count
                this_index = strategy_pair_list_total.index(final_pair)
                counter_pair_list_total[this_index] += 1

            break

# print final results over all experimental runs
print()
print("Final Result")
print()

# for each final strategy pair
for index in range(len(strategy_pair_list_total)):
    print("proportion of experiments ending in this strategy pair ", round(counter_pair_list_total[index]*1.0/sum(counter_pair_list_total), 3), "\t")
    print("number of experiments ending in this strategy pair", counter_pair_list_total[index], "\t")
    print("this strategy pair", strategy_pair_list_total[index])

#print()

#for entry in strategy_pair_list_total:
#    print(entry, "\t")
#print()
#for entry in counter_pair_list_total:
#    print(entry, "\t")
#print()


print("count of experiment outcomes (F, B, CB, CR, X): ", counter_type)
