import mountaincar
from Tilecoder import numTilings, numTiles, tilecode
from pylab import *  # includes numpy
from DoubleQ import *

numRuns = 1
n = numTiles * 3

def learn(alpha=.1/numTilings, epsilon=0, numEpisodes=200):
    theta1 = -0.001*rand(n)
    theta2 = -0.001*rand(n)
    returnSum = 0.0
    
    doubleQ = DoubleQ(alpha, epsilon)
    for episodeNum in range(numEpisodes):
        G = 0
        isTerminal = false
        #initialize the mountain car
        state = mountaincar.init()
        while (not isTerminal):
            action = doubleQ.policy(state)
            reward, nextState = sample(state, action)
            G+=reward
            doubleQ.learn(self, state, action, nextState, reward)           
            state = nextState
            if not nextState:
                isTerminated = True
                
        print("Episode: ", episodeNum, "Steps:", step, "Return: ", G)
        returnSum = returnSum + G
    print("Average return:", returnSum / numEpisodes)
    return returnSum, theta1, theta2


#Additional code here to write average performance data to files for plotting...
#You will first need to add an array in which to collect the data

def writeF(theta1, theta2):
    fout = open('value', 'w')
    steps = 50
    for i in range(steps):
        for j in range(steps):
            F = tilecode(-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps)
            height = -max(Qs(F, theta1, theta2))
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()


if __name__ == '__main__':
    runSum = 0.0
    for run in range(numRuns):
        returnSum, theta1, theta2 = learn()
        runSum += returnSum
    print("Overall performance: Average sum of return per run:", runSum/numRuns)
