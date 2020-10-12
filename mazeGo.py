import argparse
import gym
import numpy
import maze
import Astar_copia
import Greedy
from time import time

done = False

def defMovements(arMaze):
    inicio = tuple()
    final = tuple()
    obstacle = list()
    for idx, x in numpy.ndenumerate(arMaze):
        if (x=='0'):
            obstacle.append(idx)
        elif (x=='i'):
            inicio = idx
        elif (x=='f'):
            final = idx
    
    return(inicio,final,obstacle)

def startGo(inicio, final, obstaculos, size, findpath):
    # Arguments
    parser = argparse.ArgumentParser(description='Go Maze Solver')
    parser.add_argument('--boardsize', type=int, default=size)
    parser.add_argument('--komi', type=float, default=0)
    args = parser.parse_args()

    # Initialize environment
    go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)

    state, reward, done, info = go_env.step(inicio) 
    state, reward, done, info = go_env.step(None) #skip turn
    state, reward, done, info = go_env.step(final)

    count = 0
    for i in obstaculos:
        state, reward, done, info = go_env.step(i)
        if len(obstaculos) - 1 == count:
            continue
        state, reward, done, info = go_env.step(None)
        count += 1

    tiempo_inicial = time() 
    path = findpath.search(state[1],1, list(inicio), list(final))
    tiempo_final= time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('Tiempo de ejecucion de '+findpath.__name__+': '+ str(tiempo_ejecucion))

    ar = numpy.array(path)
    end = numpy.amax(ar)
    print('Costo del camino con '+findpath.__name__+': '+str(end))

    for i in range(1,end):
        location = numpy.where(ar == i)
        state, reward, done, info = go_env.step((int(location[0]),int(location[1])))
        state, reward, done, info = go_env.step(None)

    #go_env.render(mode="human")



for i in maze.mazes:
    print(i)
    
    arMaze = numpy.array(maze.mazes[i])
    inicio,final,obstacle = defMovements(arMaze)
    startGo(inicio, final, obstacle,len(arMaze),Astar_copia)
    startGo(inicio, final, obstacle,len(arMaze),Greedy)