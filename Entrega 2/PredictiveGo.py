import gym
import argparse
import numpy as np
from gym_go import govars, gogame    

def predict(jugadas):
    go_env_pred = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)
    
    playsinthefuture = 15

    for i in jugadas:
        state, reward, done, info = go_env_pred.step(i)
    
    nextPlays = []
    for i in range(playsinthefuture):
        nextPlays = seeInFurture(go_env_pred, nextPlays)
    for i in nextPlays:
        state, reward, done, info = go_env_pred.step(i)
    
    #go_env_pred.render(mode="terminal")
    black_area, white_area = gogame.areas(go_env_pred.state_)
    #print(black_area, white_area)
    print('Con la jugada '+str(nextPlays[0])+' se consiguen '+str(black_area)+' puntos en '+str(playsinthefuture)+' jugadas')

    return None

def seeInFurture(go_env_pred, plays):
    while True:
        action = go_env_pred.uniform_random_action()
        if action not in plays:
            plays.append(action)
            break
    return plays


parser = argparse.ArgumentParser(description='Predictive Go')
parser.add_argument('--boardsize', type=int, default=7)
parser.add_argument('--komi', type=float, default=0)
args = parser.parse_args()


#List of actions
actions = []

# Initialize environment
go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)

action = go_env.uniform_random_action()

actions.append(action)
state, reward, done, info = go_env.step(action)
#go_env.render(mode="terminal")

for i in range(5):
    predict(actions)



