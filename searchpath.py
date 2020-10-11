import argparse
import gym
import Astar
import Greedy
import numpy
from time import time

#Este programa busca marcar un punto de partida
#determinar un punto de final
#poner obtaculos en el camino
#buscar la ruta mas corta

# Arguments
parser = argparse.ArgumentParser(description='Demo Go Environment')
parser.add_argument('--boardsize', type=int, default=10)
parser.add_argument('--komi', type=float, default=0)
args = parser.parse_args()

# Initialize environment
go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)

# Game loop
done = False

partida = (1,1)
final = (8,8)
obstacles = 10

def startGo(partida, final):
    #go_env.render(mode="human")
    move = partida
    state, reward, done, info = go_env.step(move) 

    #go_env.render(mode="human")
    state, reward, done, info = go_env.step(None)

    #go_env.render(mode="human")
    action = final
    state, reward, done, info = go_env.step(action)

    i = 1
    while i < obstacles:
        #go_env.render(mode="human")
        state, reward, done, info = go_env.step(go_env.uniform_random_action())
        if i == obstacles-1:
            i += 1
            continue
        state, reward, done, info = go_env.step(None)
        i += 1

    print(state[1][1])

    go_env.render(mode="human")

    tiempo_inicial_Astar = time() 
    path = Astar.search(state[1],1, list(partida), list(final))
    tiempo_final_Astar = time() 
    tiempo_ejecucion_Astar = tiempo_final_Astar - tiempo_inicial_Astar
    print('Tiempo de ejecucion de Astar: '+ tiempo_ejecucion_Astar)



    tiempo_inicial_greedy = time() 
    path = Greedy.search(state[1],1, list(partida), list(final))
    tiempo_final_greedy = time() 
    tiempo_ejecucion_greedy = tiempo_final_greedy - tiempo_inicial_greedy
    print('Tiempo de ejecucion de Greedy: '+ tiempo_ejecucion_greedy)
    ar = numpy.array(path)
    end = numpy.amax(ar)

    for i in range(1,end):
        location = numpy.where(ar == i)

        state, reward, done, info = go_env.step((int(location[0]),int(location[1])))
        state, reward, done, info = go_env.step(None)
        go_env.render(mode="human")
        print((int(location[0]),int(location[1])))


try:
    startGo(partida,final)
    print('Success!!')
except:
    print('try Again plz')
    

