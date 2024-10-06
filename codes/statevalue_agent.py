import csv
from peaceful_pie.unity_comms import UnityComms

uc = UnityComms(8080)

filename = "state_values.csv"

with open(filename, mode="r", newline="") as file:
    reader = csv.DictReader(file)
    state_values = {int(row['State']) : float(row['Value']) for row in reader}

print(state_values)

done = 0
state_list = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]

def takeAction(state, state_value_dict, state_x, state_y):
    states = [(state_x, state_y+2), (state_x+2, state_y), (state_x, state_y-2), (state_x-2, state_y)]
    possible_states = [state+2, state+8, state-2, state-8]
    possible_values = [0,0,0,0]
    for i in range(4):
        if ((states[i][0] in [0,2,4,6]) and (states[i][1] in [0,2,4,6])):
            possible_values[i] = state_value_dict[possible_states[i]]
        else:
            possible_values[i] = float('-inf')
        
    action = int(possible_values.index(max(possible_values)))
    return action

state_info = uc.resetGame()

state_info = state_info.split(',')

state_x_info = state_info[0].split(':')
state_x = int(state_x_info[1])

state_y_info = state_info[1].split(':')
state_y = int(state_y_info[1])

prev_state_info = state_info[2].split(':')
prev_state = int(prev_state_info[1])

print("Game began")
while done == 0:
    action = takeAction(prev_state, state_values, state_x, state_y)

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

    prev_state = state
    state_x = x
    state_y = y

    if reward == 1:
        print(f"Won the game")
    elif reward == -1:
        print("Lost the game")

print("Game Completed")