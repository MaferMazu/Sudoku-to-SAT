# Sudoku to SAT 🌎️ 🚀️

Los ciudadanos de un planeta llamado Titán han conservado una reliquia indescifrable conocida como tablero de Sudoku. Los científicos de ese planeta han tratado de resolver el misterio escondido en ese problema, sin embargo ellos sólo saben resolver problemas SAT (Problema de Satisfacibilidad Booleana). Es por eso que se asignó como primer proyecto de diseño de algoritmos I convertir el tablero de Sudoku en un problema SAT y resolverlo.

## Sudoku to SAT

Un tablero de Sudoku de orden N es una matriz de N² filas y N²  columnas. La matriz está dividida en N² secciones disjuntas, cada una una matriz de tamaño N × N . Cada celda puede contener a lo sumo un número entre 1 y N².

El siguiente es un ejemplo para un tablero de Sudoku de orden 3

|   |   |   |   4|   |   |   |   | 9  |
| :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: |
|   | 2  |   |9   |  8 |   |   | 3  |   |
|   | 9  | 3  |   |   |   | 8  | 4  |   |
|   |   |   |   |   |   |   |   |   |
|  2 |   |   |   |   | 8  |   | 6  |  7 |
|  1 | 6  |   | 3  |   |   |   |   |  2 |
|   |  4 |   |   |   |   |  6 |5   |   |
| 6  |   |   |   |   |   |  3 |   |   |
|   |   |   |   |  5 |   9|   |  1 | _  |


Como entrada tenemos:

`3 000400009020980030093000840000000000200008067160300002049000650600003000000059010`

Que es la representación del tablero del ejemplo. (donde 0 significa casilla vacía)

Para pasar este majestuoso problema a SAT

Primero vamos a definir p(d,f,c) en donde -1 < d < N² y representa el dígito que esta en la fila f 0 < f < N² y en la columna c  0 < c < N²

A partir de esta notación si queremos representar el 4 que se encuentra en la primera fila del ejemplo tendríamos: p(4,1,4)

Con esto en mente se pueden crear las siguientes proposiciones, que usaremos para SAT:

Para asegurarnos de que en cada fila se tendrá sólo un número por casilla y que estos sean del 1 al  N²
X1 = para todo p(d1,fi,c3) y p(d2,fi,c4) con d != 0 y 0<i<N² y 0<d1,d2,c3,c4 < N² => d1!= d2 y c3!=c4

Para asegurarnos de que en cada columna se tendrá sólo un número por casilla y que estos sean del 1 al  N²

X2 = para todo p(d1,f3,ci) y p(d2,f4,ci) con d != 0 y 0<i<N² y 0<d1,d2,f3,f4 < N² => d1!= d2 y f3!=f4 

Para asegurarnos de que por región existan los número del 1 al N²
Primera región

X3 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² 0<i,j<N => d1!=d2

Segunda región
X4 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² 0<i<N N+1<j<N+(N+1)  => d1!=d2

Tercera región
X5 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² 0<i<N N+(N+1)<j<N+N+(N+1)  => d1!=d2

Y así con las demás secciones:
(De momento se usará N=3 y a fuerza bruta, luego se buscará unificar variables)

Primera región a partir de la 4ta fila
X6 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² N<i,j<N+(N+1) => d1!=d2

Segunda región a partir de la 4ta fila
X7 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² N<i<N+(N+1) N+1<j<N+(N+1)  => d1!=d2

Tercera región a partir de la 4ta fila
X8 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² N<i<N+(N+1) N+(N+1)<j<N+N+(N+1)  => d1!=d2

Primera región a partir de la 7ma fila
X9 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² 2N<i,j<2N+(N+1) => d1!=d2

Segunda región a partir de la 7ma fila
X10 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² 2N<i<2N+(N+1) N+1<j<N+(N+1)  => d1!=d2

Tercera región a partir de la 7ma fila
X11 = para todo p(d1,fi,cj) y p(d2,fi,cj) con 0<d1,d2<N² 2N<i<2N+(N+1) N+(N+1)<j<N+N+(N+1)  => d1!=d2
