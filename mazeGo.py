import argparse

import gym

import numpy
import maze
import Astar
import Greedy
from time import time


done = False
maze = maze.maze

arMaze = numpy.array(maze)

def defMovements(arMaze):
    inicio = tuple()
    final = tuple()
    obstacle = list()
    for idx, x in numpy.ndenumerate(arMaze):
        if (x=='1'):
            obstacle.append(idx)
        elif (x=='i'):
            inicio = idx
        elif (x=='f'):
            final = idx
    
    return(inicio,final,obstacle)

def startGo(inicio, final, obstaculos, size):
    # Arguments
    parser = argparse.ArgumentParser(description='Demo Go Environment')
    parser.add_argument('--boardsize', type=int, default=size)
    parser.add_argument('--komi', type=float, default=0)
    args = parser.parse_args()

    # Initialize environment
    go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)

    state, reward, done, info = go_env.step(inicio) 
    state, reward, done, info = go_env.step(None) #skip turn
    state, reward, done, info = go_env.step(final)
    for i in obstaculos:
        state, reward, done, info = go_env.step(i)
        state, reward, done, info = go_env.step(None)

    print(state[1][1])
    go_env.render(mode="human")

    tiempo_inicial_Astar = time() 
    path1 = Astar.search(state[1],1, list(inicio), list(final))
    tiempo_final_Astar = time() 
    tiempo_ejecucion_Astar = tiempo_final_Astar - tiempo_inicial_Astar
    print('Tiempo de ejecucion de Astar: '+ str(tiempo_ejecucion_Astar))



    tiempo_inicial_greedy = time() 
    path = Greedy.search(state[1],1, list(inicio), list(final))
    tiempo_final_greedy = time() 
    tiempo_ejecucion_greedy = tiempo_final_greedy - tiempo_inicial_greedy
    print('Tiempo de ejecucion de Greedy: '+ str(tiempo_ejecucion_greedy))
    ar = numpy.array(path)
    end = numpy.amax(ar)

    for i in range(1,end):
        location = numpy.where(ar == i)

        state, reward, done, info = go_env.step((int(location[0]),int(location[1])))
        state, reward, done, info = go_env.step(None)
        go_env.render(mode="human")
        print((int(location[0]),int(location[1])))


inicio,final,obstacle = defMovements(arMaze)

startGo(inicio, final, obstacle,len(arMaze))