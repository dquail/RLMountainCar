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
