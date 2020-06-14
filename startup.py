from Game import *
from ParameterSet import *
import pickle

# number precision for printing
np.set_printoptions(precision=3)

# set the game by defining the L value
NDG = Game(0.4)

# we need to know how many Blue and Red
sizeBlue = 50
sizeRed = 50


# utility for running means
def running_mean(x, n):
    # pad with a zero at the start
    # then calculate the cumulative summation
    CumSum = np.cumsum(np.insert(x, 0, 0))
    # two arrays that remove the first n and the last n elements
    # now the array from the subtraction is the sum of the last n elements
    # divide by n to get the windowed average for window n
    return (CumSum[n:] - CumSum[:-n]) / n


# complete parameter set to run one experimental condition
setup = ParameterSet(sizeBlue, sizeRed, NDG)

# now run the experiments
setup.simulate()

# now analyse them
setup.analysis()

with open('ndg_data', 'wb') as f:
    pickle.dump(setup, f)