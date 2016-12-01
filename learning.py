import mountaincar
from Tilecoder import numTilings, numTiles, tilecode
from pylab import *  # includes numpy
from DoubleQ import *

numRuns = 1
n = numTiles * 3

def learn(alpha=.1/numTilings, epsilon=0, numEpisodes=1000):
    theta1 = -0.001*rand(n)
    theta2 = -0.001*rand(n)
    returnSum = 0.0
    
    doubleQ = DoubleQ(alpha, epsilon)
    for episodeNum in range(numEpisodes):
        print("Episode " + str(episodeNum) + " ....")
        G = 0
        isTerminal = False
        #initialize the mountain car
        state = mountaincar.init()
        while (not isTerminal):
            action = doubleQ.policy(state)
            #print("state: " + str(state))
            #print("action: " + str(action))
            reward, nextState = mountaincar.sample(state, action)
            G+=reward
            doubleQ.learn(state, action, nextState, reward)           
            state = nextState
            if not nextState:
                isTerminal = True
                
        print("Episode: ", episodeNum, "Steps:", step, "Return: ", G)
        returnSum = returnSum + G
    print("Average return:", returnSum / numEpisodes)
    theta1 = doubleQ.theta1
    theta2 = doubleQ.theta2
    return returnSum, theta1, theta2


#Additional code here to write average performance data to files for plotting...
#You will first need to add an array in which to collect the data
def writeFile(theta1, theta2):
    doubleQ = DoubleQ(0.1/4, 0)
    doubleQ.theta1 = theta1
    doubleQ.theta2 = theta2
    
    
    fout = open('value', 'w')
    steps = 50
    for i in range(steps):
        for j in range(steps):
            #F = tilecode(-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps)
            state = (-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps)
            bestAction = doubleQ.policy(state)
            #height = -max(Qs(F, theta1, theta2))
            #def qHat(self, state, action, theta):            
            height = -doubleQ.qHat(state, bestAction, np.add(theta1,theta2)/2)
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()


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
