from learning import *

doubleQ = DoubleQ(0.1, 0)
state = mountaincar.init()
action = doubleQ.policy(state)
reward, nextState = mountaincar.sample(state, action)
doubleQ.learn(state, action, nextState, reward)

