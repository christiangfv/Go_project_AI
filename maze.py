import numpy

maze = [[1,1,1,1,1,1,0,0,0,'f'],
[1,0,1,0,1,1,0,1,1,0],
[1,1,1,1,0,0,0,0,0,0],
[1,0,0,0,0,1,0,1,0,0],
[1,0,1,1,0,0,0,1,1,0],
[1,0,1,1,0,1,1,1,0,0],
[1,0,1,0,0,1,1,1,1,0],
[1,0,1,1,0,0,0,1,0,0],
[1,'i',0,0,0,1,1,0,1,1],
[1,0,1,0,1,1,0,1,0,1]]

arMaze = numpy.array(maze)

def defmMovements(arMaze):
    inicio = tuple()
    final = tuple()
    obstacle = list()
    for idx, x in numpy.ndenumerate(arMaze):
        if (x=='1'):
            obstacle.append(idx)
        elif (x=='i'):
            inicio = idx
        elif (x=='f'):
            final = idx
    
    return(inicio,final,obstacle)
