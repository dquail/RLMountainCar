from pylab import *
import matplotlib.pyplot as plt
import numpy
from Tilecoder import *

class DoubleQ:
    def __init__(self, alpha, eps):
        self.numberOfWeights = tilesPerTiling * tilesPerTiling * numTilings * 3
        self.alpha = alpha
        self.eps = eps
        
        self.theta1 = [np.random.uniform(-0.001, 0)]*self.numberOfWeights
        self.theta2 = [np.random.uniform(-0.001, 0)]*self.numberOfWeights
        
        """
        self.theta1 = [0]*self.numberOfWeights
        self.theta2 = [0]*self.numberOfWeights
        """
        
    def resetQ(self):
        self.theta1 = [np.random.uniform(-0.001, 0)]*self.numberOfWeights
        self.theta2 = [np.random.uniform(-0.001, 0)]*self.numberOfWeights
        """
        self.theta1 = [0]*self.numberOfWeights
        self.theta2 = [0]*self.numberOfWeights
        """

    def qHat(self, state, action, theta):
        #print("qHat with theta: " + str(theta))
        #Create the feature vector based on state, action using tile coding. Generate the value by inner product with weights (theta)
        tileIndices = tilecode(state[0], state[1], action)
        
        value = 0
        for indicie in tileIndices:
            value+=theta[indicie]
            
        return value
        
    def bestAction(self, state, theta):
        q = [self.qHat(state, 0, theta), self.qHat(state, 1, theta), self.qHat(state, 2, theta)]
        action = numpy.argmax(q)
        return action

        
    def policy(self, state):
        #Combine the average of the two weight vectors
        theta = np.add(self.theta1, self.theta2) / 2
        
        q = [self.qHat(state, 0, theta), self.qHat(state, 1, theta), self.qHat(state, 2, theta)]
        #print(q)
        action = numpy.argmax(q)
        #print("policy action: " + str(action) + " for " + str(state))
        return action
        
    def learn(self, state, action, nextState, reward):
        #determine which theta to update
        newStateValue = 0
        tileIndices = tilecode(state[0], state[1], action)
        
        if (random() > 0.5):
            #print("Using theta1")
            nextStateValue = 0
            if (nextState):
                #Non terminal
                #q1BestNextAction = argmax(Q1[newState])                    
                theta1BestNextAction = self.bestAction(state, self.theta1)
                #newStateValue = Q2[newState, q1BestNextAction]
                newStateValue = self.qHat(nextState, theta1BestNextAction, self.theta2)
        
            #Q1[currentState, action] = Q1[currentState, action] + alpha*(reward + newStateValue - Q1[currentState, action])
            #TODO - this is obviously going to fail. IT's trying to add a vector (currently an array) a scalar * another scalar
            learningError = self.alpha * (reward + newStateValue - self.qHat(state, action, self.theta1))
            for indicie in tileIndices:
                self.theta1[indicie]+= learningError
            #self.theta1 = self.theta1 + self.alpha * (reward + newStateValue - self.qHat(state, action, self.theta1)) 
        else:
            #print("Using theta2")
            nextStateValue = 0
            if (nextState):
                #Non terminal
                theta2BestNextAction = self.bestAction(state, self.theta2)
                newStateValue = self.qHat(nextState, theta2BestNextAction, self.theta1)
            
            learningError = self.alpha * (reward + newStateValue - self.qHat(state, action, self.theta2))                
            for indicie in tileIndices:
                self.theta2[indicie]+= learningError

            
            
