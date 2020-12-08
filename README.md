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

### Descripción
Utilizando un tablero de Go, se desarrolló un agente inteligente que predice a un máximo de n jugadas en el futuro y juega su mejor opción en función de esta, teniendo diferentes estrategias, con diferentes probabilidades de ocurrir a la hora de predecir la jugada:
- Ofensiva (24.9%)
- Defensiva (24.9%)
- Mixta (50%)
- Pasar turno (0.2%)

### Desarrollo del programa
A la hora de iniciar el programa se le da bienvenida al usuario y se le pide que ingrese los siguientes datos para configurar el ambiente.
- ¿Qué quieres hacer?
    - IA vs IA
    - IA vs Human
- Elegir el nivel de la maquina (cuantas jugadas podrá ver en el futuro)
    - (Actualmente se tiene un maximo de 2 jugadas a futuro, por el nivel de tiempo que demora ver mas, pero este número puede ser cambiado dentro del código).

### Obtención del puntaje y algoritmo predictivo
Para la obtención del puntaje el agente evalua en base al área quitada o ganada en el tablero, dependiendo de la estrategía del momento,  por ejemplo, si la estrategia es agresiva entonces al agente se le premia más por quitar área al rival, en cambio una estrategia defensiva premia más por ganar territorio dentro del tablero.

![Algoritmo](images/Prediction_algorithm.png)

El algoritmo de predicción visto arriba, recibe el estado actual del tablero y analiza las jugadas válidas posibles. Una vez obtenidas estas jugadas solo guarda las que le darán el mayor puntaje. Desde este punto si la profundidad es `1`, el algoritmo guarda las jugadas de máximo puntaje y escoge al azar entre ellas. Para otro caso cuando el nivel de profundidad es `mayor a 1` el algoritmo se comporta como una mezcla entre ` DFS(Deep First Search) y Greedy` analizando las proximas jugadas desde las mejores jugadas obtenidas en el nivel de profundidad anterior, filtrando las más prometedoras(máximo puntaje obtenido en ese nivel) y repitiendo el análisis hasta el último nivel. Al llegar al último nivel, el algoritmo devuelve el valor máximo de puntaje que puede obtenerse dentro de las posibles jugadas, esto se reitera hasta analizar todos los niveles y jugadas, para luego devolver el puntaje máximo de cada uno de ellos, sobreescribiendo el puntaje máximo del nivel anterior si es mayor, en otro caso el puntaje del nivel anterior se mantiene. Al volver nuevamente al primer nivel de profundidad, el algoritmo devuelve una lista con las jugadas que prometen el puntaje más alto de todos los niveles explorados, en el caso de ser más de uno, la elección es aleatoria.

### Cadena de Markov

A continuación la representación de la cadena de Markov que describe el funcionamiento del sistema.

![Markov_Chain](images/cadena_markov_go.png)

En la cadena se encuentran dos estados que presentan incertidumbre, el estado de `elección de estrategia` para el agente y el siguiente estado, donde el agente intenta `predecir la estrategia del oponente`. Vale destacar que el estado de `predicción de estrategia oponente` se llama tantas veces como `n-1` niveles de profundidad analice nuestro algoritmo. Esto es ya que para ver las jugadas futuras también es necesario saber cual será la jugada de nuestro oponente, por lo que cada vez que nuestro agente baja un nivel de profundidad, debe predecir una jugada oponente para que vuelva a ser su turno y siga buscando su mejor o mejores jugadas. 

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
