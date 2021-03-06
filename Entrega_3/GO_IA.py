import gym
import argparse
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from gym_go.gogame import invalid_moves
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
    strategy = random.choices(strategy_list, weights=(249, 249, 500, 2))
    return strategy[0]

def countingPoints(strategy, prev_black_area, prev_white_area, black_area, white_area, player):

    if strategy == "M": # Mixto
        if player == "white":
            white_pts = white_area - prev_white_area # area ganada
            black_pts = prev_black_area - black_area # area quitada

        else:
            white_pts = prev_white_area - white_area # area quitada
            black_pts = black_area - prev_black_area # area ganada


    elif strategy == "A": # Agresivo       
        if player == "white":
            white_pts = white_area - prev_white_area # area ganada
            black_pts = (prev_black_area - black_area)*2 # area quitada

        else:
            white_pts = (prev_white_area - white_area)*2 # area quitada
            black_pts = black_area - prev_black_area # area ganada


    elif strategy == "D": # Defensivo
        if player == "white":
            white_pts = (white_area - prev_white_area)*2 # area ganada
            black_pts = prev_black_area - black_area # area quitada

        else:
            white_pts = prev_white_area - white_area # area quitada
            black_pts = (black_area - prev_black_area)*2 # area ganada

    elif strategy == "P": # Pasar
        white_pts = 0
        black_pts = 0

    pts = white_pts + black_pts # area ganada + area quitada
    return pts


def predict(go_env, info_env, level, player, n_plays, enemy = False, smart = False):
    
    go_env_pred = copy(go_env)
    info = info_env 

    strategy = choose_strategy()
    if(strategy == 'P'):
        return 49 # Pasar de turno

    invalid_moves = get_invalidMoves(info["invalid_moves"])

    nextPlays = seeInFurture(go_env_pred, invalid_moves, level, player, strategy, n_plays, smart)
    if not enemy and not smart:
        #Descomentar para obtener mas detalle de los movimientos y estrategias
        #print(nextPlays.flatten())
        #print("El jugador "+player+" ha usado la estrategia "+strategy)
        pass
    
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
        

def seeInFurture(go_env_pred, invalidPlays, lvls, player, strategy, n_plays, smart, first = True):
    counter = 0
    playPoints = np.empty([0,2])
    maxPoints = 0
    tmpPoints = 0
    parentMove = np.empty([0,0])

    if player == "white":
        enemy = "black"
    else:
        enemy = "white"
    
    valid_Plays = np.empty([0,0])

    #Obtener jugadas validas
    for counter in range(49):
        if counter not in invalidPlays:
            valid_Plays = np.append(valid_Plays, counter)

    #Elegir jugadas al azar entre las jugadas validas disponibles
    for iter in range(n_plays):
        if n_plays > len(valid_Plays):
            break
        rnd = random.randrange(0, len(valid_Plays)-1)
        counter = int(valid_Plays[rnd])
        np.delete(valid_Plays, rnd)

        if len(invalidPlays) <= 1: # Primera jugada para ambos da 1 pt, no 49 >:c
            pts = 1.0

        else:
            if (smart == True):
                tmp_env = copy(go_env_pred)
                tmp_env.step(counter)

                blk = tmp_env.state_[0].flatten()
                wht = tmp_env.state_[1].flatten()

                tablero = blk

                tablero = np.where(tablero == 1, -1, 0)

                for i in range(len(wht)):
                    if int(wht[i]) == 1:
                        np.put(tablero, i, 1)
                
                tablero = tablero.reshape(1,7,7,1)
                
                #Calcular prob de ganar haciendo esta jugada
                if player == "white":
                    pts = model.predict(tf.convert_to_tensor(tablero))[0][0]
                else:
                    pts = model.predict(tf.convert_to_tensor(tablero))[0][1]

                if pts < 0.25:# Ganar
                    pts = model.predict(tf.convert_to_tensor(tablero))[0][2]
                    if pts < 0.3: # Empatar
                        pts = 0 # Si la prob de ganar y empatar es muy baja pasa de turno

            else:
                tmp_env = copy(go_env_pred)
                prev_black_area, prev_white_area = gogame.areas(tmp_env.state_)
                tmp_env.step(counter)
                black_area, white_area = gogame.areas(tmp_env.state_)

                # Guarda mejores ptjs, si no es lvl == 1, crea una lista de movimientos prometedores.
                pts = countingPoints(strategy, prev_black_area, prev_white_area, black_area, white_area, player) # area ganada + area quitada

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

    if first and tmpPoints == 0: # Si las jugadas inmediatamente futuras tienen ptj max 0, se cancela la prediccion
        parentMove = np.empty([0,0])
    if lvls: # Si llegamos al nivel 0, significa que ya pasamos el ultimo nivel, es decir el 1
        tmp_max = 0
        for i in parentMove: # Llama recursivamente a seeInFuture y obtiene el max ptj de esa rama
            tmp_env = copy(go_env_pred)
            state, reward, done, info = tmp_env.step(int(i)) # Turno jugador
            #print(state, "-", reward, "-", done, "-", info)
            enemy_action = predict(tmp_env, info, 1, enemy, 3, True) # Predecir estrategia y movimiento de adversario
            state, reward, done, info = tmp_env.step(enemy_action) # Enemigos pasan (Supuesto) <-- Incertidumbre!!! o.o
            tmp_plays = get_invalidMoves(info["invalid_moves"])
            tmp_max = seeInFurture(tmp_env, tmp_plays, lvls, player, strategy, 3, smart, False)# Max Ptj lvl inferior

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

    model = None

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
            n = input("What do You want to do?: \n[1] IA vs IA \n[2] Human vs IA \n\
[3] Data Generator\n[4] Train IA\n[5] Exit\nSelect option: ")
            if n == '1' and model != None:
                play = 1
            elif n == '2' and model != None:
                play = 2
            elif n == "3":
                play = 3
            elif n == "4":
                play = 4
            elif n == "5":
                play = 5
                print("\nSee ya later!, please come back :D and be destroyed :3\n")
                exit(1)
            else:
                print("\nInvalid input or may be you need create a model(Select Train IA), this is for options 1 and 2\n")
                continue

        # Initialize environment
        go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)

        info = {"invalid_moves": np.zeros([49,1])}
        if play == 4:
            print("\n-----------------------")
            print("        Train IA")
            print("-----------------------\n")
            while True: # Select IA lvl
                try:
                    epocas = int(input("N° de epocas al entrenar[1-inf]: "))
                    
                    if epocas > 0:
                        print("N° de epocas --> ", epocas) 
                        break
                    else:
                        print("\nNo puede ser 0 ni un valor negativo >:c\n")
                        continue
                except:
                    print("\nIngrese un valor valido por favor\n")
            
            try:
                #Abriendo datos de entrenamiento
                df = pd.read_csv('dataset.csv')
                df_f = df
                count = 0

                for i in df['tablero'].values:
                    df_f['tablero'][count] = np.fromstring(i, dtype="float64", sep=' ').reshape((7, 7, 1))
                    count+=1

                #Crear modelo
                model = models.Sequential()
                model.add(layers.Conv2D(7, (4, 4), activation='relu', input_shape=(7, 7, 1))) #data_format='channels_first'
                model.add(layers.MaxPooling2D(2,2))
                model.add(layers.Flatten())
                model.add(layers.Dense(49, activation='sigmoid'))
                model.add(layers.Dense(3, activation='softmax'))
                model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
                
                table_train = tf.convert_to_tensor(df_f['tablero'].tolist())
                res_train = tf.convert_to_tensor(df_f['resultado'].tolist())

                history = model.fit(table_train, res_train, epochs = epocas)

                model.summary()
                print("\nEntrenamiento concluído con exito")
            except:
                print("\nEl proceso a fallado, quizá no tiene los datos o simplemente no satisface las dependencias.")

        elif play == 3:
            print("\n-----------------------")
            print("     Generar Datos")
            print("-----------------------\n")
            while True: # Select IA lvl
                try:
                    ia_lvl = int(input("Elija nivel de la maquina contrincante [1-3]: "))
                    
                    if ia_lvl < 4 and ia_lvl > 0:
                        print("Maquinas nivel --> ", ia_lvl) 
                    else:
                        print("\nEsos niveles no estan disponibles por el momento :c\n")
                        continue

                    t_cap = int(input("Ingrese el tiempo de captura[10-20-30-40]: "))
                    
                    if t_cap <= 40 and t_cap > 0:
                        print("Se capturará la jugada N° --> ", t_cap) 
                    else:
                        print("\nEsas jugadas no estan disponibles :c\n")
                        continue

                    n_montecarlo = int(input("Elija numero de jugadas en TreeSearch MonteCarlo[1-10]: "))
                    
                    if n_montecarlo <= 10 and n_montecarlo > 0:
                        print("Jugadas aleatorias por nivel de profundidad --> ", n_montecarlo)
                    else:
                        print("\nEse numero de jugadas no está disponible :c\n")
                        continue

                    n_stages = int(input("Elija numero de juegos a simular [1-inf]: "))
                    if n_stages > 0:
                        break 
                    else:
                        print("\nEl numero de juegos no puede ser cero ni negativo >:c\n")
                        continue
                except:
                    print("\nIngrese un valor valido por favor\n")

            initial_n_stages = n_stages

            for iter in range(t_cap,60):
                n_stages = initial_n_stages
                go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)
                action = predict(go_env, info, ia_lvl, "black", n_montecarlo)#go_env.uniform_random_action()
                #print("Black: "+str(action))

                state, reward, done, info = go_env.step(action)

                while n_stages:
                    cont = 1
                    print(iter) # Imprime la jugada que se está capturando

                    while not done:   # el ciclo termina cuando acaba el juego!!
                                    # mientras tanto se dedicará a guardar las jugadas actuales en actions

                        #White turn
                        action = predict(go_env, info, ia_lvl, "white", n_montecarlo)
                        #print("White: "+str(action))
                        state, reward, done, info = go_env.step(action)
                        #End White turn
                        
                        cont += 1
                        #go_env.render(mode="terminal")

                        if cont == iter:
                            blk = go_env.state_[0].flatten()
                            wht = go_env.state_[1].flatten()

                        if done: # Si termina luego de la jugada blanca
                            break

                        # Black turn
                        action = predict(go_env, info, ia_lvl,"black", n_montecarlo)
                        #print("Black: "+str(action))
                        state, reward, done, info = go_env.step(action)
                        #End Black turn
                        #go_env.render(mode="terminal")
                        cont += 1

                        if cont == iter:

                            blk = go_env.state_[0].flatten()
                            wht = go_env.state_[1].flatten()

                    n_stages = n_stages -1

                    if cont < iter:
                        blk = go_env.state_[0].flatten()
                        wht = go_env.state_[1].flatten()

                    tablero = blk

                    tablero = np.where(tablero == 1, "-1", 0)

                    for i in range(len(wht)):
                        if int(wht[i]) == 1:
                            np.put(tablero, i, "1")

                    tablero = ' '.join(tablero)

                    print(tablero)

                    black_area, white_area = gogame.areas(go_env.state_)

                    if white_area > black_area:
                        out = 0 # Blanco gana

                    elif white_area < black_area:
                        out = 1 # Negro gana
                    
                    else:
                        out = 2 #Empate

                    dataset = open("dataset.csv", "a")
                    dataset.write(str(out)+","+tablero+"\n")
                    dataset.close()


                    if n_stages != 0:
                        print("Iniciando nuevo tablero")
                        go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)
                        action = predict(go_env, info, ia_lvl, "black", n_montecarlo)

                        state, reward, done, info = go_env.step(action)
                    else:
                        print("Fin de la generación de datos.")
            

        elif(play == 2):
            print("\n-----------------------")
            print("     Human vs IA")
            print("-----------------------\n")
            while True: # Select IA lvl
                try:
                    ia_lvl = int(input("Elija nivel de la maquina [1-3]: "))
                    
                    if ia_lvl < 4 and ia_lvl > 0:
                        pass
                    else:
                        print("\nEsos niveles no estan disponibles por el momento :c\n")
                        continue

                    n_montecarlo = int(input("Elija numero de jugadas en TreeSearch MonteCarlo[1-10]: "))
                    
                    if n_montecarlo <= 10 and n_montecarlo > 0:
                        print("Jugadas aleatorias por nivel de profundidad --> ", n_montecarlo)
                    else:
                        print("\nEse numero de jugadas no está disponible :c\n")
                        continue

                    smart = int(input("Maquina smart? [0 No - 1 Si]: "))
                    
                    if smart == 0:
                        print("Maquina normal seleccionada")
                        break
                    elif smart == 1:
                        print("Maquina smart seleccionada")
                        break 
                    else:
                        print("\nDebes responder 0[Si] o 1[No] o.o\n")
                        continue
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
                action = predict(go_env, info, ia_lvl, "white", n_montecarlo, smart = smart)
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
                    ia1_lvl = int(input("Elija nivel de la maquina 1 [1-3]: "))

                    if ia1_lvl < 4 and ia1_lvl > 0:
                        print("IA 1 (Negro) --> lvl " + str(ia1_lvl)) 
                    else:
                        print("\nEsos niveles no estan disponibles por el momento :c\nIntente seleccionar los niveles nuevamente... \n")
                        continue

                    ia2_lvl = int(input("Elija nivel de la maquina 2 [1-3]: "))
                    
                    if ia2_lvl < 4 and ia2_lvl > 0:
                        print("IA 2 (Blanco) --> lvl " + str(ia2_lvl))  
                    else:
                        print("\nEsos niveles no estan disponibles por el momento :c\nIntente seleccionar los niveles nuevamente... \n")

                    n_montecarlo = int(input("Elija numero de jugadas en TreeSearch MonteCarlo[1-10]: "))
                    
                    if n_montecarlo <= 10 and n_montecarlo > 0:
                        print("Jugadas aleatorias por nivel de profundidad --> ", n_montecarlo)
                    else:
                        print("\nEse numero de jugadas no está disponible :c\n")
                        continue

                    smart1 = int(input("Maquina 1(Negro) smart? [0 No - 1 Si]: "))
                    
                    if smart1 == 0:
                        print("Maquina normal seleccionada")
                    elif smart1 == 1:
                        print("Maquina smart seleccionada") 
                    else:
                        print("\nDebes responder 0[Si] o 1[No] o.o\n")
                        continue

                    smart2 = int(input("Maquina 2(Blanco) smart? [0 No - 1 Si]: "))
                    
                    if smart2 == 0:
                        print("Maquina normal seleccionada")
                        break
                    elif smart2 == 1:
                        print("Maquina smart seleccionada")
                        break 
                    else:
                        print("\nDebes responder 0[Si] o 1[No] o.o\n")
                        continue
                except:
                    print("\nIngrese un valor valido por favor\n")

            action = predict(go_env, info, ia1_lvl, "black", n_montecarlo, smart = smart1)#go_env.uniform_random_action()
            print("Black: "+str(action))

            state, reward, done, info = go_env.step(action)

            while not done:   # el ciclo termina cuando acaba el juego!!
                            # mientras tanto se dedicará a guardar las jugadas actuales en actions

                #White turn
                action = predict(go_env, info, ia2_lvl, "white", n_montecarlo, smart = smart2)

                print("White: "+str(action))
                state, reward, done, info = go_env.step(action)
                #End White turn

                go_env.render(mode="terminal")

                if done: # Si termina luego de la jugada blanca
                    break

                # Black turn
                action = predict(go_env, info, ia1_lvl,"black", n_montecarlo, smart = smart1)
                print("Black: "+str(action))
                state, reward, done, info = go_env.step(action)
                #End Black turn
                go_env.render(mode="terminal")

            go_env.render("human")
            input("Presione cualquier botón para continuar...")




