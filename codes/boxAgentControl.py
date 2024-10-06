from peaceful_pie.unity_comms import UnityComms
import random

uc = UnityComms(8080)

#Testing the connection
uc.sendTest(message="Hello Unity")
mes = uc.recieveTest()
print(f'Message Recieved is : {mes}')

episodes = 10000
state_list = []
action_list = [0,1,2,3]
games_won = 0
gw_epn = []

q_list = {}
def update_q(state_list):
    for s in state_list:
        q_list[s] = [0,0,0,0]
        for a in action_list:
            q_list[s][a] = random.random()
            #q_list[s][a] = 0

def actionAlgo(epsilon, state, q_list):
    r = random.random()

    if epsilon > r:
        actions = q_list[state]
        action = int(actions.index(max(actions)))

        print(f"Algo Action : {action}")
        return action
    else:
        action = int(random.choice([0,1,2,3]))
        print(f'random action: {action}')
        return action

for episode in range(episodes):
    print(f"Episode {episode} begins now")
    state_info = uc.resetGame()

    state_info = state_info.split(',')

    state_x_info = state_info[0].split(':')
    state_x = int(state_x_info[1])

    state_y_info = state_info[1].split(':')
    state_y = int(state_y_info[1])

    prev_state_info = state_info[2].split(':')
    prev_state = int(prev_state_info[1])

    done = 0

    while (done == 0):
        #Check for the state in state_list
        if prev_state in state_list:
            print(f"{prev_state} state already exists")
        else:
            print(f"adding state {prev_state} to the list")
            state_list.append(prev_state)
            update_q(state_list)

        epsilon = episode/episodes
        action = actionAlgo(epsilon, prev_state, q_list)
        #action = int(input("Enter Action"))
        results = uc.takeAction(action=action)

        results = results.split(',')
        
        observation = results[0].split(':')
        nextstate = int(observation[1])

        if nextstate in state_list:
            print(f"state {nextstate} already exists")
        else:
            print(f"adding state {nextstate} to the list")
            state_list.append(nextstate)
            update_q(state_list)

        reward_list = results[1].split(':')
        reward = int(reward_list[1])

        done_list = results[2].split(':')
        done = int(done_list[1])

        q_prevstate = q_list[prev_state]
        print(f"{q_list[nextstate]} and {max(q_list[nextstate])}")
        q_prevstate[action] += 0.1*(reward+(0.5*max(q_list[nextstate]))-q_prevstate[action])

        prev_state = nextstate

        if done == 1:
            if reward == 1:
                games_won += 1
                gw_epn.append(episode)
            break


print(f"no.of games won are : {games_won}")
print(f"games won at episodes : {gw_epn}")