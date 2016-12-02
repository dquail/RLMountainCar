import mountaincar
from Tilecoder import tilecode, numTilings, numTiles, tilecode
from pylab import *  # includes numpy
#from DoubleQ import *

from pylab import *
import matplotlib.pyplot as plt
import numpy
from Tilecoder import *

actionOffset = numTiles*numTiles*numTilings

class DoubleQ:
    def __init__(self, alpha, eps):
        self.numberOfWeights = tilesPerTiling * tilesPerTiling * numTilings * 3
        self.alpha = alpha
        self.eps = eps

        self.theta1 = -0.001*rand(self.numberOfWeights)
        self.theta2 = -0.001*rand(self.numberOfWeights)
        
    def resetQ(self):
        self.theta1 = -0.001*rand(self.numberOfWeights)
        self.theta2 = -0.001*rand(self.numberOfWeights)

    def qHat(self, state, action, theta):
        value = 0
        for indicie in state:
            value+=theta[indicie + action*actionOffset]
        return value
        
    def bestAction(self, state, theta):
        return numpy.argmax([self.qHat(state, 0, theta), self.qHat(state, 1, theta), self.qHat(state, 2, theta)])

    def policy(self, state):
        #Combine the average of the two weight vectors
        theta = np.add(self.theta1, self.theta2) / 2
        return numpy.argmax([self.qHat(state, 0, theta), self.qHat(state, 1, theta), self.qHat(state, 2, theta)])
        
    def learn(self, state, action, nextState, reward):
        #determine which theta to update
        newStateValue = 0
        #tileIndices = state
        
        if (random() > 0.5):
            #print("Using theta1")
            nextStateValue = 0
            if (nextState):
                #Non terminal
                theta1BestNextAction = self.bestAction(nextState, self.theta1)
                newStateValue = self.qHat(nextState, theta1BestNextAction, self.theta2)
        
            learningError = self.alpha * (reward + newStateValue - self.qHat(state, action, self.theta1))
            for indicie in state:
                self.theta1[indicie + action*actionOffset]+= learningError
        else:
            #print("Using theta2")
            nextStateValue = 0
            if (nextState):
                #Non terminal
                theta2BestNextAction = self.bestAction(nextState, self.theta2)
                newStateValue = self.qHat(nextState, theta2BestNextAction, self.theta1)
            
            learningError = self.alpha * (reward + newStateValue - self.qHat(state, action, self.theta2))                
            for indicie in state:
                self.theta2[indicie+action*actionOffset]+= learningError

    
numRuns = 1
n = 9 * 9 * 4 * 3 

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


    
def learn(alpha=.1/numTilings, epsilon=0, numEpisodes=200):
    return learnOverRuns(alpha, epsilon, numEpisodes)
    
def learnOverEpisodes(alpha=.1/numTilings, epsilon=0, numEpisodes=1000):
    theta1 = -0.001*rand(n)
    theta2 = -0.001*rand(n)
    returnSum = 0.0

    doubleQ = DoubleQ(alpha, epsilon)
    for episodeNum in range(numEpisodes):
        #print("Episode " + str(episodeNum) + " ....")
        G = 0
        isTerminal = False
        #initialize the mountain car
        stateTuple = mountaincar.init()
        state = tilecode(stateTuple[0], stateTuple[1])
        while (not isTerminal):
            action = doubleQ.policy(state)
            #print("state: " + str(state))
            #print("action: " + str(action))
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
                state = tilecode(stateTuple[0], stateTuple[1])

        #print("Episode: ", episodeNum, "Steps:", step, "Return: ", G)
        returnSum = returnSum + G
    print("Average return:", returnSum / numEpisodes)
    theta1 = doubleQ.theta1
    theta2 = doubleQ.theta2
    return returnSum, theta1, theta2

def learnOverRuns(alpha=.1/numTilings, epsilon=0, numEpisodes=200, numRuns=1):
    theta1 = -0.001*rand(n)
    theta2 = -0.001*rand(n)
    returnSum = 0.0
    avgEpisodeReturns = [0]*numEpisodes
    doubleQ = DoubleQ(alpha, epsilon)

    for run in range(numRuns):
        doubleQ.resetQ()
        for episodeNum in range(numEpisodes):
            #print("Episode " + str(episodeNum) + " ....")
            G = 0
            isTerminal = False
            #initialize the mountain car
            stateTuple = mountaincar.init()
            state = tilecode(stateTuple[0], stateTuple[1])

            while (not isTerminal):
                action = doubleQ.policy(state)
                #print("state: " + str(state))
                #print("action: " + str(action))
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
                    state = tilecode(stateTuple[0], stateTuple[1])

            #print("Run: ",  run+1, " Episode: ", episodeNum, " Steps:", step, " Return: ", G)
            returnSum = returnSum + G
            """
            print("===========")
            print("Updating average Episode " + str(episodeNum) + " array")
            print("Original value: " + str(avgEpisodeReturns[episodeNum]))
            print("G: " + str(G))
            print("episodeNum: " + str(episodeNum))
            """
            avgEpisodeReturns[episodeNum] = avgEpisodeReturns[episodeNum] +  (1/(run+1))*(G - avgEpisodeReturns[episodeNum])
            """
            print("Updated value: " + str(avgEpisodeReturns[episodeNum]))
            print("")
            """
        #print("Average return:", returnSum / (numEpisodes * numRuns))

    theta1 = doubleQ.theta1
    theta2 = doubleQ.theta2
    #sumOfRewards = np.sum(avgEpisodeReturns)
    #return avgEpisodeReturns, theta1, theta2
    return returnSum, theta1, theta2


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
