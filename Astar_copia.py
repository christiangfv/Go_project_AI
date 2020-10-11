import numpy as np

class Node:

    """
        - Representa una posicion en el tablero.
        - Parent: es el nodo perteneciente a la posicion previa
        - position: posicion actual, del nodo actual

        - g: costo desde el primer nodo hasta el nodo actual.
        - h: costo basado en la distancia heuclidiana entre el nodo actual y el final.
        - f: costo total de este nodo: f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

"""
    Esta funcion devuelve el camino que se ha recorrido desde el principio hasta un nodo actual.
"""
def return_path(current_node,maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    # Se inicializa el tablero con -1.
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node

    # current recorre desde el nodo actual, hasta el nodo inicial, agregando la lista
    # "path" el camino recorrido.
    while current is not None:
        path.append(current.position)
        current = current.parent

    # El camino debe invertirse, por lo explicado en el comentario anterior.
    path = path[::-1]
    start_value = 0
    # we update the path of start to end found by A-star serch with every step incremented by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result