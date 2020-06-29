# Sudoku to SAT 🌎️ 🚀️

Los ciudadanos de un planeta llamado Titán han conservado una reliquia indescifrable conocida como tablero de Sudoku. Los científicos de ese planeta han tratado de resolver el misterio escondido en ese problema, sin embargo ellos sólo saben resolver problemas SAT (Problema de Satisfacibilidad Booleana). Es por eso que se asignó como primer proyecto de diseño de algoritmos I convertir el tablero de Sudoku en un problema SAT y resolverlo.

## Estado actual del proyecto:

dom, jun 28 23:59

Se encuentran operativos los programas SudokuToSat y SolutionToSudoku, la parte del resolvedor aún está en pruebas.

## Para correr el programa:

Se necesita python3

• Traductor de instancias de Sudoku a instancias de SAT

`> python3 SudokuToSat.py`

• Traductor de soluciones de SAT a soluciones de Sudoku

`> python3 SolutionToSudoku.py`

## Para la entrega de este proyecto hay 3 partes esenciales:

• Traductor de instancias de Sudoku a instancias de SAT
El cual se encuentra en el archivo SudokuToSat.py y consta de todas las condiciones escritas en formato SAT que debe cumplir un problema sudoku para encontrar su solución.

• Resolvedor propio de SAT

• Traductor de soluciones de SAT a soluciones de Sudoku
El cual se encuentra en SolutionToSudoku.py y transforma la salida especificada en el resolvedor de zChaff a una salida tanto lineal como en forma matricial.

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

Para pasar este problema a SAT

Primero vamos a definir p(d,f,c) en donde -1 < d < N² y representa el dígito que esta en la fila f 0 < f < N² y en la columna c  0 < c < N²

A partir de esta notación si queremos representar el 4 que se encuentra en la primera fila del ejemplo tendríamos: p(4,1,4)

## El programa translateSat.txt

Al usar:
`> python3 translateSat.txt`

Se puede visualizar el output del SudokuToSat en forma de p(d,f,c)


