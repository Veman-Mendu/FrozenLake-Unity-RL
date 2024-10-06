# FrozenLake-Unity-RL
This project is about implementing TD Prediction method on Frozen Lake environment on Unity. The Temporal Prediction (TD) Prediction is implemented using python

# TD Prediction

The TD Prediction method focuses on updating the state values for every step. This project when implemented on your local machine and verified will prove that updating the state values alone is not enough to reach the goal. The code for TD Predictions is available at boxAgent.py

**The observation of TD Prediction is**:
 The algorithm never reached the goal in the second half of the total episodes. 

 # TD Control

 The TD Control method focuses on updating the q values. The code for Q learning implementation is available at boxAgentControl.py

 **The observation of TD Control is**:
The algorithm was able to learn the direction to go in order to reach the goal and was able to reach the goal around 60 % of the time in the second half of the total run. 

The reason for mentioning **Second Half of the total run** is I have tried to implement the algorithms in a On-policy approach making the run move from complete random actions at the start of the game to complete algorithm based actions at the end of the game.

The Unity Editor used for this project is 2022.3.47f1.

# Special Mentions
1. https://github.com/ivankunyankin/ml_agents_frozen_lake -- For the environment

2. https://www.youtube.com/playlist?list=PLdBvOJzNTtDWbz8hl-HJ6pWF0Hu9Em2n4 -- For showing an easy approach to communicate between python and Unity.
