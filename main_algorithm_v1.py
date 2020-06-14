from Game import *
from Agent_old import *
import random
#import Ext_functions as ext

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
#signal_set = [0.0, 0.25, 0.5, 0.75, 1.0]


# some lists for counting things
strategy_pair_list_total = []
counter_pair_list_total = []
counter_type = [0,0,0,0,0]


print "EXP_ID \tRT \tCONV \tSTR_blue \tSIG_blue \tSTR_red \tSIG_red"

# start experiments
for exp in range(num_experiments):

    print exp, "\t",


    # create a population of agents with random strategies
    agents = []

    for dummy in range(size_Blue):

        s0 = random.randint(0, 2)
        s1 = random.randint(0, 2)
        prob_A = random.choice(signal_set)

        if fixed_type == 0 or fixed_type == 2:
            prob_A = 1.0

        agents.append(Agent(0, disagreement, prob_A, [s0,s1]))

    for dummy in range(size_Red):
        s0 = random.randint(0, 2)
        s1 = random.randint(0, 2)
        prob_A = random.choice(signal_set)

        if fixed_type == 1 or fixed_type == 2:
            prob_A = 0.0

        agents.append(Agent(1, 0.0, prob_A, [s0, s1]))


    # normalizer for accumulated utility
    normalizer = 0.6*(len(agents)-1)


    ### run the algorithm ###
    for current_round in range(run_time):

        # some more lists for counting things
        strategy0_list = []
        counter0_list = []
        strategy1_list = []
        counter1_list = []

        if print_round_results:
            print
            print "ROUND", current_round

        ### resetting and mutation ###
        for agent in agents:

            # reset each agent
            agent.reset()

            # apply mutation
            if random.random() < mutation_rate:
                agent.strategy[0] = random.randint(0, 2)
                agent.strategy[1] = random.randint(0, 2)
                agent.sigA_prob = random.choice(signal_set)

                if agent.type == 0:
                    if fixed_type == 0 or fixed_type == 2:
                        agent.sigA_prob = 1.0
                elif agent.type == 1:
                    if fixed_type == 1 or fixed_type == 2:
                        agent.sigA_prob = 0.0


        ### interaction ###
        for agent1 in agents:
            for agent2 in agents:
                if agent1 != agent2:
                    agent1.interact(agent2, NDG)


        ### imitation ###
        for index in range(len(agents)):

            # pick current index' agent and opponent of same type
            agent = agents[index]
            if index < size_Blue:
                op_agent = random.choice(agents[0:size_Blue-1])
            else:
                op_agent = random.choice(agents[size_Blue:])


            # imitate the other agent if scored better with probability of score difference
            if op_agent.accumulated_utility > agent.accumulated_utility:

                diff = (op_agent.accumulated_utility-agent.accumulated_utility)/normalizer
                prob = random.random()
                if prob < diff:
                    agent.strategy[0] = op_agent.strategy[0]
                    agent.strategy[1] = op_agent.strategy[1]
                    agent.sigA_prob = op_agent.sigA_prob


            ### recording ###
            if index < len(agents)/2:
                if agent.strategy not in strategy0_list:
                    strategy0_list.append(agent.strategy)
                    counter0_list.append(1)
                else:
                    this_index = strategy0_list.index(agent.strategy)
                    counter0_list[this_index]+=1

            else:
                if agent.strategy not in strategy1_list:
                    strategy1_list.append(agent.strategy)
                    counter1_list.append(1)
                else:
                    this_index = strategy1_list.index(agent.strategy)
                    counter1_list[this_index] += 1

        ### after a round: print the round results ###
        if print_round_results:

            for entry in strategy0_list:
                print entry, "\t",
            print "- \t",
            for entry in strategy1_list:
                print entry, "\t",
            print

            for entry in counter0_list:
                print entry, "\t",
            print "- \t",
            for entry in counter1_list:
                print entry, "\t",
            print

            for index in range(len(agents)/2):
                print agents[index].strategy, #round(agents[index].accumulated_utility,1),
            print
            for index in range(len(agents)/2, len(agents)):
                print agents[index].strategy, #round(agents[index].accumulated_utility,1),
            print


        ### after a round: check if all agent's play teh same strategy ###
        new0_sigs = []
        new1_sigs = []
        for agent in agents:
            if agent.type == 0:
                new0_sigs.append(agent.sigA_prob)
            else:
                new1_sigs.append(agent.sigA_prob)

        same_sig = False
        same_stratF = False
        same_stratB = False

        if sum(new0_sigs)/len(new0_sigs) == 0.0 and sum(new1_sigs)/len(new1_sigs) == 0.0:
            same_sig = True
            same_stratF = True
            same_stratB = True
            for entry in strategy0_list:
                if entry[1] != 1:
                    same_stratF = False
                if entry[1] != 2:
                    same_stratB = False

            for entry in strategy1_list:
                if entry[1] != 1:
                    same_stratF = False
                if entry[1] != 0:
                    same_stratB = False


        elif sum(new0_sigs) / len(new0_sigs) == 1.0 and sum(new1_sigs) / len(new1_sigs) == 1.0:
            same_sig = True
            same_stratF = True
            same_stratB = True
            for entry in strategy0_list:
                if entry[0] != 1:
                    same_stratF = False
                if entry[0] != 2:
                    same_stratB = False
            for entry in strategy1_list:
                if entry[0] != 1:
                    same_stratF = False
                if entry[0] != 0:
                    same_stratB = False




        ### after a round: if one of the break conditions is fulfilled, break and print results ###
        if (len(strategy0_list) == 1 and len(strategy1_list) == 1) or current_round == run_time-1 or (same_sig and (same_stratF or same_stratB)):

            print current_round, "\t",


            # print Blue group strategy and add to total list
            new0_list = []
            new1_list = []
            for entry in strategy0_list:
                if entry not in new0_list:
                    new0_list.append(entry)

            for entry in strategy1_list:
                if entry not in new1_list:
                    new1_list.append(entry)

            if (new0_list == [[2, 1]] and new1_list == [[1, 0]]) or (new0_list == [[1, 2]] and new1_list == [[0, 1]]):


                print "CB", "\t",
                counter_type[2] += 1



            elif (new0_list == [[1, 0]] and new1_list == [[2, 1]]) or (new0_list == [[0, 1]] and new1_list == [[1, 2]]):

                print "CR", "\t",
                counter_type[3] += 1



            elif (new0_list == [[1,1]] and new1_list == [[1,1]]) or (same_sig and (same_stratF or same_stratB)):

                if same_stratF or (new0_list == [[1,1]] and new1_list == [[1,1]]):
                    print "F", "\t",
                    counter_type[0] += 1
                elif same_stratB:
                    print "B", "\t",
                    counter_type[1] += 1
            else:
                print "X", "\t",
                counter_type[4] += 1

            print new0_list, "\t", round(sum(new0_sigs)/len(new0_sigs),2),"\t- \t",

            print new1_list, "\t", round(sum(new1_sigs)/len(new1_sigs),2)


            final_pair = [strategy0_list[0],strategy1_list[0]]

            if final_pair not in strategy_pair_list_total:
                strategy_pair_list_total.append(final_pair)
                counter_pair_list_total.append(1)
            else:
                this_index = strategy_pair_list_total.index(final_pair)
                counter_pair_list_total[this_index] += 1

            break


### print final results over all experimenta runs ###
print
print "Final Result"
print

for index in range(len(strategy_pair_list_total)):
    print round(counter_pair_list_total[index]*1.0/sum(counter_pair_list_total),3), "\t",
    print counter_pair_list_total[index], "\t",
    print strategy_pair_list_total[index]

print

for entry in strategy_pair_list_total:
    print entry, "\t",
print
for entry in counter_pair_list_total:
    print entry, "\t",
print

print counter_type
