import blackjack
from pylab import *
import matplotlib.pyplot as plt
import numpy
from TileCoder import *

class DoubleQ:
    def __init__(self, numberOfWeights, alpha, eps):
        self.numberOfWeights = numberOfWeights
        self.initialWeights = initialWeights
        self.alpha = alpha
        self.eps = eps
        self.theta1 = [np.random.uniform(-0.001, 0)]*numberOfWeights
        self.theta2 = [np.random.uniform(-0.001, 0)]*numberOfWeights
        
    def resetQ():
        self.theta1 = [np.random.uniform(-0.001, 0)]*numberOfWeights
        self.theta2 = [np.random.uniform(-0.001, 0)]*numberOfWeights

    def vHat(state, action, theta):
        #TODO - return the actual value here using 
        #Create the feature vector based on state, action using tile coding. Generate the value by inner product with weights (theta)
        tileIndices = tilecode(state[0], state[1], action)
        
        value = 0
        for indicie in tileIndices:
            value+=theta[indicie]
            
        return value
        
    def policy(state):
        #Combine the average of the two weight vectors
        theta = (self.theta1 + self.theta2) / 2
        
        q = [self.vHat(state, 0, theta), self.vHat(state, 1, theta), self.vHat(state, 2, theta)]
        action = numpy.argmax(q)
        return action
        
def learn(state, action, nextState, reward):
    returnSum = 0.0
    totalStay = 0
    totalHit = 0
    evalSteps = []
    
    for episodeNum in range(numTrainingEpisodes):
        G = 0

        # Fill in Q1 and Q2
        currentState = blackjack.init()
        
        terminated = False
        
        while(not terminated):
            action = -1
            
            #Choose A from S using policy derived from Q1 and Q2 (epsilon greedy in Q1+Q2)
            
            #Decide to explore vs. Exploit
            randomE = random()                
            if (randomE < eps):
                #explore
                action = randint(0,2)    
            else:
                #Exploit / Choose the best current action
                action= policy(currentState)

            if (action ==0):
                totalStay = totalStay+1
            else:
                totalHit = totalHit + 1
            
            #Take action A, observe R, S'
            transitionTuple = blackjack.sample(currentState, action)
            newState = transitionTuple[1]
            reward = transitionTuple[0]
            newStateValue = 0
            
            #Do learning - updating Q values
            randomQ = random()
            if (randomQ > 0.5):
                nextStateValue = 0
                if (newState):
                    #Non terminal
                    q1BestNextAction = argmax(Q1[newState])                    
                    newStateValue = Q2[newState, q1BestNextAction]
            
                Q1[currentState, action] = Q1[currentState, action] + alpha*(reward + newStateValue - Q1[currentState, action])
            else:
                if (newState):
                    #Non terminal
                    q2BestNextAction = argmax(Q2[newState])                    
                    newStateValue = Q1[newState, q2BestNextAction]        
                Q2[currentState, action] = Q2[currentState, action] + alpha*(reward + newStateValue - Q2[currentState, action])                

            currentState = newState
            if (currentState == False):
                G = reward
                terminated = True

        returnSum = returnSum + G
   
        if episodeNum % 10000 == 0 and episodeNum != 0:
            #print("Average return so far: ", returnSum/episodeNum)
            evalSteps.append(returnSum/episodeNum)
            #blackjack.printPolicy(policy)

    
    print("Average total return so far: ", returnSum/numTrainingEpisodes)
    
    fig = plt.figure()
    fig.suptitle('Learning rate for blackjack', fontsize = 14, fontweight = 'bold')
    ax = fig.add_subplot(111)
    
    titleLabel = "alpha:" + str(alpha) + ", eps:" + str(eps) + ", runs:" + str(numTrainingEpisodes)
    ax.set_title(titleLabel)
    ax.set_xlabel('episode')
    ax.set_ylabel('cumulative avg. return')
    ax.plot(evalSteps)
    plt.show()
    
    return returnSum/numTrainingEpisodes

def simpleEvaluate(numEvaluationEpisodes):
    learn(0.0, 0.0, numEvaluationEpisodes)
    
def evaluate(numEvaluationEpisodes):
    returnSum = 0.0

    for episodeNum in range(numEvaluationEpisodes):
        G = 0

        # Fill in Q1 and Q2
        currentState = blackjack.init()
        
        terminated = False
        
        while(not terminated):
            action= policy(currentState)

            #Take action A, observe R, S'
            transitionTuple = blackjack.sample(currentState, action)
            newState = transitionTuple[1]
            reward = transitionTuple[0]
            newStateValue = 0
            currentState = newState
            if (currentState == False):
                G = reward
                terminated = True
            
        returnSum = returnSum + G
        
        if episodeNum % 10000 == 0 and episodeNum != 0:
            print("Average return so far: ", returnSum/episodeNum)
        
    print("Average total return so far: ", returnSum/numEvaluationEpisodes)
    return returnSum/numEvaluationEpisodes

def runTests(numberOfTrainingRuns):
    alpha = 0.01
    while (alpha < 0.1):
        eps = 0.01
        while (eps < 0.1):
            resetQs()
            avg = learn(alpha, eps, numberOfTrainingRuns)
            print("==== Alpha: " + str(alpha) + ", eps: " + str(eps) + ", Avg: " + str(avg))
            eps = eps + 0.01
        alpha = alpha + 0.01
            
            
def resetQs():
    Q1 = numpy.random.uniform(low = 0, high = 0.0001, size=(181,2))
    Q2 = numpy.random.uniform(low = 0, high = 0.0001, size=(181,2))    
    
def policy(state):
    q1 = Q1[state]
    q2 = Q2[state]
    q = [q1[0] + q2[0], q1[1] + q2[1]]
    action = numpy.argmax(q)
    return action
    
    
def printStateActionValues():
    for index in range(len(Q1)):
        print("===========")
        blackjack.printState(index)
        print("Stay: " + str(Q1[index, 0]))
        print("Hold: " + str(Q1[index, 1]))
        print("==========")
        print("")

