import csv
from peaceful_pie.unity_comms import UnityComms

uc = UnityComms(8080)

filename = "action_values.csv"

with open(filename, mode="r", newline="") as file:
    reader = csv.DictReader(file)
    action_values = {int(row['State']) : [float(row['0']), float(row['1']), float(row['2']), float(row['3'])] for row in reader}

print(action_values)

done = 0

state_info = uc.resetGame()

state_info = state_info.split(',')

prev_state_info = state_info[2].split(':')
prev_state = int(prev_state_info[1])

def takeAction(q_list, state):
    actions = q_list[state]
    action = int(actions.index(max(actions)))

    print(f"Algo Action : {action}")
    return action

print("Game began")
while done == 0:
    action = takeAction(action_values, prev_state)

    results = uc.takeAction(action=action)
        
    results = results.split(',')
        
    observation = results[0].split(':')
    state = int(observation[1])

    reward_list = results[1].split(':')
    reward = int(reward_list[1])

    done_list = results[2].split(':')
    done = int(done_list[1])

    prev_state = state

    if reward == 1:
        print(f"Won the game")
    elif reward == -1:
        print("Lost the game")

print("Game Completed")