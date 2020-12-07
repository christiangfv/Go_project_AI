import gym
import argparse
from gym_go.gogame import invalid_moves
import numpy as np
import random
from gym_go import govars, gogame 
from copy import copy  ## Copia profunda de un objeto, no referencia al mismo!!

# Obtiene los movimientos invalidos desde el dict de info y las jugadas previas
def get_invalidMoves(invalid_moves):
    not_valid_moves = np.empty([0,0])
    
    for i in range(len(invalid_moves)):
        if invalid_moves[i] == 1:
            not_valid_moves = np.append(not_valid_moves, i)
    
    return not_valid_moves

def choose_strategy():
    strategy_list = ['A', 'D', 'M', 'P']
    strategy = random.choices(strategy_list, weights=(40, 40, 10, 10))
    return strategy[0]

def predict(go_env, info_env, level, player):
    
    go_env_pred = copy(go_env)
    info = info_env 

    strategy = choose_strategy()
    if(strategy == 'P'):
        print("{ Estrategia: pasar turno :c }")
        return 49

    nextPlays = []
    invalid_moves = get_invalidMoves(info["invalid_moves"])
    #playsinthefuture = np.count_nonzero(info["invalid_moves"] == 0) - 1

    nextPlays = seeInFurture(go_env_pred, invalid_moves, level, player)
    print(nextPlays.flatten())
    
    black_area, white_area = gogame.areas(go_env_pred.state_)
    
    if player == "white":
        if nextPlays.size != 0 and nextPlays[0, 1] > 0: # or nextPlays[0, 2] < black_area:
            
            play = random.randrange(len(nextPlays)) # Si hay más de una jugada que promete un mismo max ptj, se elige al azar
            return int(nextPlays[play, 0])
        else:
            return 49
    else:
        if nextPlays.size != 0 and nextPlays[0, 1] > 0: # or nextPlays[0, 2] < black_area:
            
            play = random.randrange(len(nextPlays)) # Si hay más de una jugada que promete un mismo max ptj, se elige al azar
            return int(nextPlays[play, 0])
        else:
            return 49
        

def seeInFurture(go_env_pred, invalidPlays, lvls, player, first = True):
    counter = 0
    playPoints = np.empty([0,2])
    maxPoints = 0
    tmpPoints = 0
    parentMove = np.empty([0,0])

    for counter in range(49):
        if counter not in invalidPlays:
            # Captura el puntaje de las jugadas de nivel n

            if len(invalidPlays) <= 1: # Primera jugada para ambos da 1 pt, no 49 >:c
                pts = 1.0

            else:
                tmp_env = copy(go_env_pred)
                prev_black_area, prev_white_area = gogame.areas(tmp_env.state_)
                tmp_env.step(counter)
                black_area, white_area = gogame.areas(tmp_env.state_)

                # Guarda mejores ptjs, si no es lvl == 1, crea una lista de movimientos prometedores.
                if player == "white":
                    white_pts = white_area - prev_white_area # area ganada
                    black_pts = prev_black_area - black_area # area quitada

                else:
                    white_pts = prev_white_area - white_area # area ganada
                    black_pts = black_area - prev_black_area # area quitada

                pts = white_pts + black_pts # area ganada + area quitada

            if lvls == 1: # Crea lista de jugadas prometedoras del nivel más profundo y setea el ptj maximo
                if pts > maxPoints:
                    maxPoints = pts  
                    playPoints = np.array([[counter, pts]])
                elif pts == maxPoints: 
                    playPoints = np.append(playPoints, [[counter, pts]], axis=0)
            else: # Si no es el lvl 1, crea lista con jugadas prometedoras a analizar y setea ptj maximo
                if pts > tmpPoints:
                    tmpPoints = pts
                    parentMove = np.array([counter])
                elif pts == tmpPoints:
                    parentMove = np.append(parentMove, counter)
            
    lvls = lvls - 1 # Bajamos un nivel en el arbol

    if first and tmpPoints == 0 and not lvls: # Si las jugadas inmediatamente futuras tienen ptj max 0, se cancela la prediccion
        parentMove = np.empty([0,0])

    if lvls: # Si llegamos al nivel 0, significa que ya pasamos el ultimo nivel, es decir el 1
        tmp_max = 0

        for i in parentMove: # Llama recursivamente a seeInFuture y obtiene el max ptj de esa rama
            tmp_env = copy(go_env_pred)
            state, reward, done, info = tmp_env.step(int(i)) # Turno jugador
            state, reward, done, info = tmp_env.step(49) # Enemigos pasan (Supuesto) <-- Incertidumbre!!! o.o
            tmp_plays = get_invalidMoves(info["invalid_moves"])
            tmp_max = seeInFurture(tmp_env, tmp_plays, lvls, player, False)

            if tmp_max > maxPoints and not first:
                maxPoints = tmp_max

            elif first: # si estamos en la rama principal, es decir, siguiente jugada, guardamos jugada y max pje de la rama
                if tmp_max == maxPoints: # Si tienen igual ptj se añade a la lista
                    if not maxPoints: # Si el ptj max(tmp_max) de 1 lvl mas abajo es 0, se asigna el ptj max del lvl actual
                        tmp_max = tmpPoints
                    playPoints = np.append(playPoints, [[i, tmp_max]], axis=0)

                elif tmp_max > maxPoints: # Si se encuentr un ptj mayor, se resetea la lista y setea el max
                    playPoints = np.array([[i, tmp_max]])
                    maxPoints = tmp_max

        if not maxPoints:
            maxPoints = tmpPoints

    if first: # Si es el primer nivel, devolvemos la jugada junto al pje max de sus hijos
        maxPoints = playPoints

    return maxPoints

def valid_action(action, invalid_moves):
    if action is None:
        return True  

    n = action[0]*7 + action[1]    
    return not invalid_moves[n]


if __name__ == "__main__":

    while True:
        #--------------------------------------------- 
        #           MAIN :v
        #--------------------------------------------- 
        print("\n--------------------------")
        print("     WELCOME TO IA GO")
        print("--------------------------\n")

        parser = argparse.ArgumentParser(description='Predictive Go')
        parser.add_argument('--boardsize', type=int, default=7)
        parser.add_argument('--komi', type=float, default=0)
        args = parser.parse_args()

        #--------------------------------------------- 
        #           SETUP 
        #--------------------------------------------- 
        play = False      # if the user wants to play
        while not play:
            n = input("What do You want to do?: \n[1] IA vs IA \n[2] Human vs IA \n[3] Exit\nSelect option: ")
            if n == '1':
                play = 1
            elif n == '2':
                play = 2
            elif n == "3":
                play = 3
                print("\nSee ya later!, please come back :D and be destroyed :3\n")
                exit(1)
            else:
                print("\n{ ERROR: invalid input >:C }\n")
                continue

        # Initialize environment
        go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)

        info = {"invalid_moves": np.zeros([49,1])}

        if(play == 2):
            print("\n-----------------------")
            print("     Human vs IA")
            print("-----------------------\n")
            while True: # Select IA lvl
                try:
                    ia_lvl = int(input("Elija nivel de la maquina [1-2]: "))
                    
                    if ia_lvl < 3 and ia_lvl > 0:
                        break 
                    else:
                        print("\nEsos niveles no estan disponibles por el momento :c\n")
                except:
                    print("\nIngrese un valor valido por favor\n")
            # First human action
            done = False
            invalid_moves = np.zeros([49,1])
            while not done:
                go_env.render(mode="terminal")
                while True:
                    # Human turn (B)
                    move = input("Input move '(row col)/p': ")
                    
                    if move == 'p':
                        action = None #49
                        break
                    else:
                        try:
                            action = int(move[0]), int(move[1])
                            if not valid_action(action, invalid_moves) or action[0] > 6 or action[1] > 6:
                                print("\nthat play is invalid, try again")
                                continue
                            break
                        except:
                            print("\nthat play is invalid, try again")
                            continue

                state, reward, done, info = go_env.step(action)
                print("Black: ", action)

                if go_env.game_ended():
                    break

                # IA turn (w)
                action = predict(go_env, info, ia_lvl, "white")
                state, reward, done, info = go_env.step(action)
                print("White: ", action)
                invalid_moves = info['invalid_moves']

            go_env.render("human")
            input("Presione cualquier botón para continuar...")



        elif(play == 1): 
            print("\n-----------------------") 
            print("     IA vs IA") 
            print("-----------------------\n")

            while True: # Select IAs lvl
                try:
                    ia1_lvl = int(input("Elija nivel de la maquina 1 [1-2]: "))

                    if ia1_lvl < 3 and ia1_lvl > 0:
                        print("IA 1 (Negro) --> lvl " + str(ia1_lvl)) 
                    else:
                        print("\nEsos niveles no estan disponibles por el momento :c\nIntente seleccionar los niveles nuevamente... \n")
                        continue

                    ia2_lvl = int(input("Elija nivel de la maquina 2 [1-2]: "))
                    
                    if ia2_lvl < 3 and ia2_lvl > 0:
                        print("IA 2 (Blanco) --> lvl " + str(ia2_lvl)) 
                        break 
                    else:
                        print("\nEsos niveles no estan disponibles por el momento :c\nIntente seleccionar los niveles nuevamente... \n")
                except:
                    print("\nIngrese un valor valido por favor\n")

            action = predict(go_env, info, ia1_lvl, "black")#go_env.uniform_random_action()
            print("Black: "+str(action))

            state, reward, done, info = go_env.step(action)

            while not done:   # el ciclo termina cuando acaba el juego!!
                            # mientras tanto se dedicará a guardar las jugadas actuales en actions

                #White turn
                action = predict(go_env, info, ia2_lvl, "white")

                print("White: "+str(action))
                state, reward, done, info = go_env.step(action)
                #End White turn

                go_env.render(mode="terminal")

                if done: # Si termina luego de la jugada blanca
                    break

                # Black turn
                action = predict(go_env, info, ia1_lvl, "black")
                print("Black: "+str(action))
                state, reward, done, info = go_env.step(action)
                #End Black turn
                go_env.render(mode="terminal")

            go_env.render("human")
            input("Presione cualquier botón para continuar...")




