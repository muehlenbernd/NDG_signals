
def running_mean(x, n):
    # pad with a zero at the start
    # then calculate the cumulative summation
    CumSum = np.cumsum(np.insert(x, 0, 0))
    # two arrays that remove the first n and the last n elements
    # now the array from the subtraction is the sum of the last n elements
    # divide by n to get the windowed average for window n
    return (CumSum[n:] - CumSum[:-n]) / n

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
        strat = np.random.randint(0, 3, 2)

        # sig is a random vector in the unit cube of dimension sig_dim
        sig = np.random.rand(sig_dim)

        # except the first dimension is fixed, Blue = 0 , Red=1
        sig[0] = 0

        # blue agent is agent type, disagreement point, signal, list of strategies
        agents.append(Agent(0, disagreement, sig, sig_fid, sig_dim, strat, typeSigCorr, tolerance, plasticity))

    # now build all the red agents
    for dummy in range(size_Red):

        # strat is the conditional strategy function
        strat = np.random.randint(0, 3, 2)

        # sig is a random vector in the unit cube of dimension sig_dim
        sig = np.random.rand(sig_dim)

        # except the first dimension is a prob of signalling to type
        sig[0] = 1

        # red agent is agent type, disagreement point (0), signal, list of strategies
        agents.append(Agent(1, 0.0, sig, sig_fid, sig_dim, strat, typeSigCorr, tolerance, plasticity))

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

        # calculate and print the mean rewards for blue and red this round
        start = (round_size * current_round+1) - 1
        blueRSeq = np.array(experiment.rewardB[start:])
        bRunMean = np.mean(blueRSeq)
        print("blue mean reward", bRunMean)
        redRSeq = np.array(experiment.rewardR[start:])
        rRunMean = np.mean(redRSeq)
        print("red mean reward", rRunMean)

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
                    agent.sig[1:] = op_agent.sig[1:]
                    # move your tolerance level closer to the tolerance level of the other agent
                    agent.tol = agent.tol + agent.plasticity * (op_agent.tol - agent.tol)

    results.append(experiment)

    print("Final simulation step, signal vectors for all blue agents")
    print(results[exp].blueSigSeq[-1])
    print("Final simulation step, signal vectors for all red agents")
    print(results[exp].redSigSeq[-1])

    print("Final simulation step, conditional strategy, all blue agents")
    for agent in range(0, size_Blue - 1):
        print("tolerance", results[exp].blueTolSeq[-1][agent], " t ", results[exp].blueStratSeq[-1][agent][0], ", not t ", results[exp].blueStratSeq[-1][agent][1])

    print("Final simulation step, conditional strategy, all red agents")
    for agent in range(0, size_Red - 1):
        print("tolerance", results[exp].redTolSeq[-1][agent], "t ", results[exp].redStratSeq[-1][agent][0], ", not t ", results[exp].redStratSeq[-1][agent][1])
