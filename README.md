# Go_project_AI
Proyecto dedicado para programar un agente inteligente capaz de resolver la busqueda del camino mas corto y en un laberinto utilizando el tablero del clasico juego Go para simular el laberinto.


## Content of this document

1. <a href="#installation">Installation</a>
2. <a href="#environments">Environments</a>
3. <a href="#Reporte_entrega">Reporte de entrega</a>
4. <a href="#resources">Resources</a>
5. <a href="#contributors">Contributors</a>
6. <a href="#contact">Contact</a>

<a href="#installation"><h2>Installation</h2></a>

You can install the Go_project_AI with:

```bash
git clone https://github.com/christiangfv/Go_project_AI
cd Go_project_AI
pip install -e .
``` 

You will be able to run the [examples](#examples) right away.

You can see the dependencies in the [setup.py](setup.py) file.


<a href="#environments"><h2>Environments</h2></a>

Se ha utilizado el entorno de trabajo GoGym simular el tablero de Go.

1. [[GymGo](https://github.com/aigagror/GymGo)]

<a href="#Reporte_entrega"><h2>Reporte de entrega</h2></a>

Utilizando un tablero de Go, se contruyeron diferentes laberintos los cuales fueron resueltos usando 2 algoritmos de búsqueda,
greedy y A-star, ambos son algoritmos de búsqueda bastante parecidos, con la diferencia que A* evaluar el costo de la distancia 
mas corta del nodo actual al destino y tambien evalua el costo del nodo siguiente 
con el nodo de inicio.

Por lo mismo ambos suelen llegar a caminos similares, con la diferencia del numero de iteraciones al ejecutarse, Greedy suele tener
mas iteraciones, ya que recorre mas camino antes de encontrar el indicado.

<a href="#resources"><h2>recursos</h2></a>

Nos basamos en los siguientes articulos:
[[Greedy/A*](https://es.slideshare.net/AndrewFerlitsch/ai-greedy-and-astar-search)]

Obtuvimos el entorno de este repositorio:
[[GymGo](https://github.com/aigagror/GymGo)]



<a href="#contributors"><h2>Contributors</h2></a>

Here is a list of people who have contributed to this project:

- Christian Fuentes [[GitHub](https://github.com/igormaraujo/)]
- Jorge fernandez [[GitHub](https://github.com/cafe-tera)]

PD: El codigo fue escrito en conjunto utilizando la extension de vscode live-share
