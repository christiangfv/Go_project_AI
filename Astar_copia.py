import numpy as np

class Node:
    """
        - Representa una posicion en el tablero.
        - position: posicion actual, del nodo actual
        - previusPosition: es el nodo perteneciente a la posicion previa

        - g: costo desde el primer nodo hasta el nodo actual.
        - h: costo basado en la distancia heuclidiana entre el nodo actual y el final.
        - f: costo total de este nodo: f = g + h
    """
    def __init__(self, previusPosition=None, position=None):
        self.position = position
        self.previusPosition = previusPosition

        self.g = 0
        self.h = 0
        self.f = 0
    
    # Funcion equals, para comparar la posicion entre dos nodos
    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node,maze):
    """
        Esta funcion devuelve el camino que se ha recorrido desde el principio hasta un nodo actual.
        Se inicializa el tablero con -1, para luego escribir el camino encontrado y devolverlo
    """
    path = []
    rows, columns = np.shape(maze)
    result = [[-1 for i in range(columns)] for j in range(rows)]
    current = current_node

    # current recorre desde el nodo actual, hasta el nodo inicial, agregando la lista
    # "path" el camino recorrido.
    while current is not None:
        path.append(current.position)
        current = current.previusPosition

    # El camino debe invertirse, por lo explicado en el comentario anterior.
    path = path[::-1]
    start_value = 0

    # Se le agregan valores al camino encontrado, donde cada paso incrementa su valor en 1.
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(maze, cost, start, end):
    """
        Realiza una busqueda del camino mas corto utilizando el algoritmo A*
        - Se crea tanto el nodo de inicio como el de término, además se inicializa el costo en 0
    """
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    """
        Se inicializan las listas yet_to_visit_list y visited_list.

        - visited_list: guarda los nodos ya visitados y que no necesitarán ser visitados
                        otra vez.

        - yet_to_visit_list: guarda los nodos a visitar en cada iteración y luego se evalua
                            cual es el mejor movimiento.
    """
    yet_to_visit_list = []  
    visited_list = [] 
    
    # Agregamos el nodo de inicio
    yet_to_visit_list.append(start_node)
    
    # Para evitar un loop infinito agregamos una condición de termino, luego de 
    # un razonable numero de movimientos.
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # Lista de movimientos posibles cuando estamos en una posicion
    # como se ve solo existen 4.
    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right

    # Obtenemos el numero de filas y columnas de nuestro tablero
    rows, columns = np.shape(maze)
    
    # Loop hasta que no hayan nodos por visitar.
    while len(yet_to_visit_list) > 0:
        
        # Cada vez que se toma un nodo el contador de operaciones incrementa
        outer_iterations += 1    
        
        # Se evalua cual es la mejor nodo proximo
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # Si entra a este if, significa que no hay solucion
        # o el costo computacional es muy alto
        if outer_iterations > max_iterations:
            print ("me rindo no lo encontré ;c")
            return return_path(current_node,maze)

        # Habiendo elegido la mejor se agrega el mejor nodo a los nodos visitados.
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # Si el nodo actual es == al nodo de termino, entonces encontramos el camino.
        if current_node == end_node:
            return return_path(current_node,maze)

        # Lista de posiciones hijos, para almacenar los nodos futuros con su costo asociado
        children = []
        for new_position in move: 

            # Creamos una posicion
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Nos aseguramos que este dentro de los limites del tablero.
            if (node_position[0] > (rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (columns -1) or 
                node_position[1] < 0):
                continue

            # Nos aseguramos que sea una posicion "caminable"
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Creamos un nuevo nodo con la posicion obtenida y previamente validada
            new_node = Node(current_node, node_position)

            # Agregamos el nodo a la lista de posiciones futuras
            children.append(new_node)

        # Loop a los hijos para añadirles el costo asociado.
        for child in children:
            
            # Si el nodo ya ha sido visitado antes entonces se ignora
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # Se crean los costos de f, g y h.
            child.g = current_node.g + cost

            # Se calcula el valor "h" usando la distancia euclidiana
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h

            # Si el nodo ya esta en la lista de de nodos por visitar y ademas el costo
            # que esta en la lista es menor, entonces esta opción se ignora.
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # En caso que este nodo cumpla con todos los requerimientos anteriores
            # es añadido a la lista por visitar :3
            yet_to_visit_list.append(child)