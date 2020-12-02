import gym
import argparse
from gym_go.gogame import invalid_moves
import numpy as np
import random
from gym_go import govars, gogame 
from copy import copy  ## Copia profunda de un objeto, no referencia al mismo!!

# Obtiene los movimientos invalidos desde el dict de info y las jugadas previas
def get_invalidMoves(played, invalid_moves):
    not_valid_moves = copy(played)
    for i in range(len(invalid_moves)):
        if invalid_moves[i] == 1:
            not_valid_moves.append(i)
    return not_valid_moves

def predict(jugadas, level):
    
    go_env_pred = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)
    #print(jugadas)

    info = {"invalid_moves": np.zeros([49,1])}

    for i in jugadas:
        state, reward, done, info = go_env_pred.step(i) # Actualiza nuevo entorno

    nextPlays = []
    invalid_moves = get_invalidMoves(jugadas, info["invalid_moves"])
    #playsinthefuture = np.count_nonzero(info["invalid_moves"] == 0) - 1

    nextPlays = seeInFurture(go_env_pred, invalid_moves, level)
    print(nextPlays)
    black_area, white_area = gogame.areas(go_env_pred.state_)
    if nextPlays != [] and nextPlays[0][1] >= white_area:
        play = random.randrange(len(nextPlays)) # Si hay más de una jugada que promete un mismo max ptj, se elige al azar
        return nextPlays[play][0]
    else:
        return 49 # Esta jugada es equivalente a pasar, PASS!!!
    
    #black_area, white_area = gogame.areas(go_env_pred.state_)
    #print(black_area, white_area)
    #print('Con la jugada '+str(nextPlays[0])+' se consiguen '+str(black_area)+' puntos en '+str(playsinthefuture)+' jugadas')


def seeInFurture(go_env_pred, invalidPlays, lvls, first = True):
    counter = 0
    playPoints = []
    maxPoints = 0
    parentMove = []
    for counter in range(49):
        if counter not in invalidPlays:
            if lvls == 1: ## Captura el puntaje de las jugadas de nivel n
                tmp_env = copy(go_env_pred)
                tmp_env.step(counter)
                black_area, white_area = gogame.areas(tmp_env.state_)
                playPoints.append([counter, white_area]) # Si solo se visualiza 1 partida, esto guardara los ptjs 
                if white_area > maxPoints:
                    maxPoints = white_area
            else:
                parentMove.append(counter) # Si no estamos en el nivel n, guarda todas las jugadas posibles del nivel actual

    lvls = lvls - 1 # Bajamos un nivel en el arbol

    if lvls: # Si llegamos al nivel 0, significa que ya pasamos el ultimo nivel, es decir el 1
        tmp_max = 0
        for i in parentMove: # Llama recursivamente a seeInFuture y obtiene el max ptj de esa rama
            tmp_env = copy(go_env_pred)
            state, reward, done, info = tmp_env.step(i)
            tmp_plays = copy(invalidPlays)
            tmp_plays.append(i)
            tmp_plays = get_invalidMoves(tmp_plays, info["invalid_moves"])
            black_area, white_area = gogame.areas(tmp_env.state_)
            if white_area > maxPoints:
                tmp_max = white_area
            tmp_max = seeInFurture(tmp_env, tmp_plays, lvls, False)
            if tmp_max > maxPoints and not first:
                maxPoints = tmp_max
            elif first: # si estamos en la rama principal, es decir, siguiente jugada, guardamos jugada y max pje de la rama
                if tmp_max == maxPoints: # Si tienen igual ptj se añade a la lista
                    playPoints.append([i, tmp_max])
                elif tmp_max > maxPoints: # Si se encuentr un ptj mayor, se resetea la lista y setea el max
                    playPoints = [[i, tmp_max]]
                    maxPoints = tmp_max

    #if maxPoints == 0: # Si no hay suficientes jugadas al futuro se queda con el ptj actual de este nivel
    #    black_area, white_area = gogame.areas(go_env_pred.state_)
    #    maxPoints = white_area

    if first: # Si es el primer nivel, devolvemos la jugada junto al pje max de sus hijos
        maxPoints = playPoints

    return maxPoints

def valid_action(action, invalid_moves):
    if action is None:
        return True
    
    n = action[0]*7 + action[1]
    #print(n, invalid_moves[n])
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
        n = input("You want to do: \n[1] IA vs IA \n[2] Human vs IA \n")
        if n == '1':
            play = False
        elif n == '2':
            play = True
        else:
            print("{ ERROR: invalid input >:C }")
            exit(1)


        #List of actions
        actions = []

        # Initialize environment
        go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)

        if(play):
            print("\n-----------------------")
            print("     Human vs IA")
            print("-----------------------\n")
            
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
                            if not valid_action(action, invalid_moves) and action[0] <= 6 and action[1] <= 6:
                                print("\nthat play is invalid, try again")
                                continue
                            break
                        except:
                            continue

                state, reward, done, info = go_env.step(action)
                actions.append(action)
                print("Black: ", action)

                if go_env.game_ended():
                    break

                # IA turn (w)
                action = predict(actions,2)
                actions.append(action)
                state, reward, done, info = go_env.step(action)
                print("White: ", action)
                invalid_moves = info['invalid_moves']

                if go_env.game_ended():
                    break



        else: 
            print("\n-----------------------") 
            print("     IA vs IA") 
            print("-----------------------\n") 
            action = predict(actions,1)#go_env.uniform_random_action()
            print("Black: "+str(action))

            actions.append(action)
            state, reward, done, info = go_env.step(action)
            #go_env.render(mode="terminal")

            while not done:   # el ciclo termina cuando acaba el juego!!
                            # mientras tanto se dedicará a guardar las jugadas actuales en actions

                #White turn
                action = predict(actions,2)

                print("White: "+str(action))
                actions.append(action)
                state, reward, done, info = go_env.step(action)
                #End White turn

                go_env.render(mode="terminal")

                if done: # Si termina luego de la jugada blanca
                    break

                # Black turn
                action = predict(actions,1)
                print("Black: "+str(action))
                actions.append(action)
                state, reward, done, info = go_env.step(action)
                #End Black turn
                go_env.render(mode="terminal")

            # go_env.render("terminal")
            go_env.render("human")
            input("Presione cualquier botón para continuar...")





