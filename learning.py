import mountaincar
from Tilecoder import tilecode, numTilings, numTiles, tilecode
from pylab import *  # includes numpy
from DoubleQ import *

from pylab import *
import matplotlib.pyplot as plt
import numpy
from Tilecoder import *



#Additional code here to write average performance data to files for plotting...
#You will first need to add an array in which to collect the data
def writeF(theta1, theta2):
    doubleQ = DoubleQ(0.1/4, 0)
    doubleQ.theta1 = theta1
    doubleQ.theta2 = theta2
    
    
    fout = open('value', 'w')
    steps = 50
    for i in range(steps):
        for j in range(steps):
            #F = tilecode(-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps)
            state = (-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps)
            state = tilecode(state[0], state[1])
            bestAction = doubleQ.policy(state)
            #height = -max(Qs(F, theta1, theta2))
            #def qHat(self, state, action, theta):            
            height = -doubleQ.qHat(state, bestAction, np.add(theta1,theta2)/2)
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()

def learn(alpha=.1/numTilings, epsilon=0, numEpisodes=1000, numRuns=1):

    returnSum = 0.0
    avgEpisodeReturns = [0]*numEpisodes
    doubleQ = DoubleQ(alpha, epsilon)

    for run in range(numRuns):
        doubleQ.resetQ()
        for episodeNum in range(numEpisodes):
            print("Run: " + str(run) + ", Episode: " + str(episodeNum) + " ....")
            G = 0
            isTerminal = False
            #initialize the mountain car
            stateTuple = mountaincar.init()
            state = tilecode(stateTuple[0], stateTuple[1])

            while (not isTerminal):
                action = doubleQ.policy(state)
                reward, stateTuple = mountaincar.sample(stateTuple, action)
                G+=reward
                if stateTuple:
                    nextState = tilecode(stateTuple[0], stateTuple[1])
                else:
                    nextState = None
                    
                doubleQ.learn(state, action, nextState, reward)           

                if not stateTuple:
                    isTerminal = True
                else:
                    state = nextState

            print("Run: ",  run+1, " Episode: ", episodeNum, " Steps:", step, " Return: ", G)
            returnSum = returnSum + G
            avgEpisodeReturns[episodeNum] = avgEpisodeReturns[episodeNum] +  (1/(run+1))*(G - avgEpisodeReturns[episodeNum])

    return avgEpisodeReturns, doubleQ.theta1, doubleQ.theta2

def plot(avgEpisodeReturns):
    avgEpisodeReturns = np.multiply(avgEpisodeReturns, -1)
    fig = plt.figure(1)
    fig.suptitle('Mountain car', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(211)
    titleLabel = "Steps per learning episode to reach top of hill"
    ax.set_title(titleLabel)
    ax.set_xlabel('Episode')
    ax.set_ylabel('Steps')

    ax.plot(avgEpisodeReturns)
    plt.show()
    
if __name__ == '__main__':
    runSum = 0.0
    for run in range(numRuns):
        returnSum, theta1, theta2 = learn()
        runSum += returnSum
    #print("Overall performance: Average sum of return per run:", runSum/numRuns)
