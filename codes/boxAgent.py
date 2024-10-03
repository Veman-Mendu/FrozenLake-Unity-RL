from peaceful_pie.unity_comms import UnityComms
import random
import numpy as np

uc = UnityComms(8080)

#Testing the connection
uc.sendTest(message="Hello Unity")
mes = uc.recieveTest()
print(f'Message Recieved is : {mes}')

#Let's start the actual code
episodes = 1000

state_list = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
state_value_dict = {}
for i in state_list:
    state_value_dict[i] = 0

#actionAlgo defines the action to be taken.
def actionAlgo(episode, episodes, state, state_value_dict, state_x, state_y):
    #print("Select Action here")
    epsilon = episode/episodes
    r = random.random()

    if epsilon > r:
        
        states = [(state_x, state_y+2), (state_x+2, state_y), (state_x, state_y-2), (state_x-2, state_y)]
        possible_states = [state+2, state+8, state-2, state-8]
        possible_values = [0,0,0,0]
        for i in range(4):
            if ((states[i][0] in [0,2,4,6]) and (states[i][1] in [0,2,4,6])):
                possible_values[i] = state_value_dict[possible_states[i]]
            else:
                possible_values[i] = float('-inf')
        
        action = int(possible_values.index(max(possible_values)))
        print(f"algo action: {action} for states : {possible_states}, {possible_values}")
        return action
    else:
        action = random.choice([0,1,2,3])
        print(f'random action: {action}')
        return action


    
#Here we run the iterations for the game episodes
for episode in range(episodes):
    print(f"Episode number is : {episode}")
    state_info = uc.resetGame()

    state_info = state_info.split(',')

    state_x_info = state_info[0].split(':')
    state_x = int(state_x_info[1])

    state_y_info = state_info[1].split(':')
    state_y = int(state_y_info[1])

    prev_state_info = state_info[2].split(':')
    prev_state = int(prev_state_info[1])
    #print(f"first state is : {prev_state}")
    done = 0

    while (done == 0):
        print(f"Episode {episode} begins now")

        action = actionAlgo(episode, episodes, prev_state, state_value_dict, state_x, state_y)
        #action = int(input("Enter Action"))
        results = uc.takeAction(action=action)
        
        results = results.split(',')
        
        observation = results[0].split(':')
        state = int(observation[1])

        reward_list = results[1].split(':')
        reward = int(reward_list[1])

        done_list = results[2].split(':')
        done = int(done_list[1])

        x_list = results[3].split(':')
        x = int(x_list[1])

        y_list = results[4].split(':')
        y = int(y_list[1])

        #print(f'state is:{state}, reward is:{reward}, done is: {done}, targetPos is: {24}')

        if (reward == 1):
            print(f"state values are : {state_value_dict}")

        if state in state_list:
            state_value_dict[prev_state] = state_value_dict[prev_state] + (0.1*(reward + 0.5*(state_value_dict[state] - state_value_dict[prev_state])))
            prev_state = state
            state_x = x
            state_y = y
        else:
            state_value_dict[prev_state] = state_value_dict[prev_state] + (0.1*(reward + 0.5*(0 - state_value_dict[prev_state])))
            prev_state = state
            state_x = x
            state_y = y

    print(state_list)
    print(state_value_dict)