# Go_project_AI
Proyecto dedicado para programar un agente inteligente capaz de resolver la busqueda del camino mas corto y en un laberinto utilizando el tablero del clasico juego Go para simular el laberinto.


## Content of this document

1. <a href="#installation">Installation</a>
2. <a href="#environments">Environments</a>
3. <a href="#Reporte_entrega">Reporte de entrega</a>
4. <a href="#Reporte_entrega_2">Reporte de entrega 2</a>
5. <a href="#resources">Resources</a>
6. <a href="#contributors">Contributors</a>
7. <a href="#contact">Contact</a>

<a href="#installation"><h2>Installation</h2></a>

Para instalar Go_project_AI primero será necesario instalar el entorno que nos proporciona [[GymGo](https://github.com/aigagror/GymGo)] con los siguientes comandos:
```bash
git clone https://github.com/aigagror/GymGo.git
cd GymGo
pip install -e .
```

La biblioteca de [[GymGo](https://github.com/aigagror/GymGo)] tambien depende de la la biblioteca sklearn, la que se puede instalar con el siguiente comando:
```bash
pip install sklearn
```

Luego instalaremos el proyecto con los siguientes comandos:
```bash
git clone https://github.com/christiangfv/Go_project_AI
cd Go_project_AI
pip install -e .
``` 


<a href="#Ejecucion"><h2>Environments</h2></a>

Para ejecutar el proyecto es necesario correr el programa mazeGo.py el cual busca del archivo maze.py los laberintos a recorrer, los cuales se pueden editar desde el mismo archivo maze.py.
El programa nos mostrará por terminal el algoritmo utilizado para encontrar el camino mas corto, junto con su tiempo de ejecucion y itereaciones realizadas por el algoritmo y el costo del camino encontrado.

Uno de los resultados que se pueden obtener del laberinto 5 es el siguiente:

![Resultados de laberinto 5](images/terminal.png)
![laberinto 5](images/lab5.png)


1. [[GymGo](https://github.com/aigagror/GymGo)]

<a href="#Reporte_entrega"><h2>Reporte de entrega</h2></a>

Utilizando un tablero de Go, se contruyeron diferentes laberintos los cuales fueron resueltos usando 2 algoritmos de búsqueda,
greedy y A-star, ambos son algoritmos de búsqueda bastante parecidos, con la diferencia que A* evaluar el costo de la distancia 
mas corta del nodo actual al destino y tambien evalua el costo del nodo siguiente 
con el nodo de inicio.

Por lo mismo ambos suelen llegar a caminos similares, con la diferencia del numero de iteraciones al ejecutarse, Greedy suele tener
mas iteraciones, ya que recorre mas camino antes de encontrar el indicado.

<a href="#Reporte_entrega_2"><h2>Reporte de entrega 2</h2></a>

#### Descripción
Utilizando un tablero de Go, se desarrolló un agente inteligente que predice a un máximo de n jugadas en el futuro y juega su mejor opción en función de esta, teniendo diferentes estrategias, con diferentes probabilidades de ocurrir a la hora de predecir la jugada:
- Ofensiva (24.9%)
- Defensiva (24.9%)
- Mixta (50%)
- Pasar turno (0.2%)

#### Desarrollo del programa
A la hora de iniciar el programa se le da bienvenida al usuario y se le pide que ingrese los siguientes datos para configurar el ambiente.
- ¿Qué quieres hacer?
    - IA vs IA
    - IA vs Human
- Elegir el nivel de la maquina (cuantas jugadas podrá ver en el futuro)
    - (Actualmente se tiene un maximo de 2 jugadas a futuro, por el nivel de tiempo que demora ver mas, pero este número puede ser cambiado dentro del código).

#### Obtención del puntaje
Para la obtención del puntaje el agente evalua en base al área quitada o ganada en el tablero, dependiendo de la estrategía del momento,  por ejemplo, si la estrategia es agresiva entonces al agente se le premia más por quitar área al rival, en cambio una estrategia defensiva premia más por ganar territorio dentro del tablero.

![Algoritmo](images/prediction_DFS.png)

<a href="#resources"><h2>recursos</h2></a>

Nos basamos en los siguientes articulos:
[[Greedy/A*](https://es.slideshare.net/AndrewFerlitsch/ai-greedy-and-astar-search)]

Obtuvimos el entorno de este repositorio:
[[GymGo](https://github.com/aigagror/GymGo)]


<a href="#contributors"><h2>Contributors</h2></a>


- Christian Fuentes [[GitHub](https://github.com/igormaraujo/)]
- Jorge fernandez [[GitHub](https://github.com/cafe-tera)]
- Mario Araya F. [[GitHub](https://github.com/k1ltr0h) (Entrega 2)

PD: El codigo fue escrito en conjunto utilizando la extension de vscode live-share
