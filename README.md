# Sudoku to SAT 🌎️ 🚀️

Los ciudadanos de un planeta llamado Titan han conservado una reliquia indescifrable conocida como tablero de Sudoku. Los científicos de ese planeta han tratado de resolver el misterio escondido en ese problema, sin embargo ellos sólo saben resolver problemas SAT (Problema de Satisfacibilidad Booleana). Es por eso que se asignó como primer proyecto de diseño de algoritmos I convertir el tablero de Sudoku en un problema SAT y resolverlo.

**Proyecto por:**
[@rosanag24](https://github.com/rosanag24)
[@MaferMazu](https://github.com/MaferMazu)

## Links de acceso rápido

  * [Requerimientos:](#requerimientos-)
  * [Para correr el programa:](#para-correr-el-programa-)
  * [Forma correcta para correr cualquier input](#forma-correcta-para-correr-cualquier-input)
  * [El proyecto por partes](#el-proyecto-por-partes)
  * [Sobre la implementación](#sobre-la-implementaci-n)
    + [Implementación SudokuToSat](#implementaci-n-sudokutosat)
    + [Implementación SatSolver](#implementaci-n-satsolver)
    + [Implementacion SolutionToSudoku](#implementacion-solutiontosudoku)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Estado actual del proyecto:

dom, jun 28 23:59

Se encuentran operativos los programas SudokuToSat y SolutionToSudoku, la parte del resolvedor aún está en pruebas.

vie, jul 17 23:55

Se encuentran las 3 etapas del proyecto operativas, los scripts de corridas se encuentran operativos. Sólo falta el análisis de las gráficas de las comparaciones de las corridas.

## Requerimientos:

- Se necesita python3

- Descargar el repositorio en una carpeta que tenga un nombre sin espacios.

`Carpeta1` `Carpeta-1` Esto funciona

`Carpeta 1` Va a generar errores en los scripts

De hecho ninguna carpeta en la ruta debería tener espacios.

Para verificar que puedes usa `> pwd` en la terminal.

- Y se debe tener en la misma carpeta donde se encuentre el repositorio el archivo zChaff.

El zChaff un resolvedor de problemas SAT creado por la universidad de Princeton.

Este se puede conseguir aquí: [https://www.princeton.edu/~chaff/zchaff.html](https://www.princeton.edu/~chaff/zchaff.html)

Los scripts están diseñados para el zChaff de 64 bits sin embargo puede entrar en los scripts y modificar el nombre del archivo si hace falta.

## Para correr el programa:

En estas corridas podrá observar los resultados de nuestro algoritmo "SatSolver.py" y el de zChaff

Resuelve input2.txt con T=4100
`> ./script1.sh`

Resuelve input3.txt con T=35000
`> ./script2.sh`

Siendo T el tiempo en mili segundos.

Puede que sea necesario cambiar los permisos de ejecución de los scripts, de ser así puede hacerlo con:

`> sudo chmod 777 script1.sh`
`> sudo chmod 777 script2.sh`

Y luego intente ejecutar con el ./ como se mencionó antes.

## Forma correcta para correr cualquier input

`> python3 SudokuToSat.py <direcciondeinput>`

`> python3 SatSolver.py <T>`

Con T en mili segundos. (puede dejar T vacío y usar el tiempo por defecto de 40mil mili segundos. (40 segundos))

`> python3 SolutionToSudoku.py`

### Ejemplo

`> python3 SudokuToSat.py inputs/input2.txt`
`> python3 SatSolver.py 100`
`> python3 SolutionToSudoku.py`

## El proyecto por partes

### Traductor de instancias de Sudoku a instancias de SAT

Un tablero de Sudoku de orden N es una matriz de N² filas y N² columnas.

La matriz está dividida en N² secciones disjuntas, cada una una matriz de tamaño N × N. Cada celda puede contener a lo sumo un número entre 1 y N².

El siguiente es un ejemplo para un tablero de Sudoku de orden 3

| | | | 4| | | | | 9 |
| :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: | :------------: |
| | 2 | |9 | 8 | | | 3 | |
| | 9 | 3 | | | | 8 | 4 | |
| | | | | | | | | |
| 2 | | | | | 8 | | 6 | 7 |
| 1 | 6 | | 3 | | | | | 2 |
| | 4 | | | | | 6 |5 | |
| 6 | | | | | | 3 | | |
| | | | | 5 | 9| | 1 | _ |

El programa SudokuToSat a partir de un input con esta forma:

Input ejemplo:
`3 000400009020980030093000840000000000200008067160300002049000650600003000000059010`
(Es el mismo de la tabla de arriba)

Crea un archivo que modela las reglas de sudoku a instancias de SAT en forma normal conjuntiva (cnf)

Output ejemplo:
c Este es el tablero en CNF
p cnf 63 12
5 0 12 0 22 0 33 0 43 0
1 2 3 4 5 6 7 8 9 0 
10 11 12 13 14 15 16 17 18 0 
19 20 21 22 23 24 25 26 27 0 
28 29 30 31 32 33 34 35 36 0 
37 38 39 40 41 42 43 44 45 0 
46 47 48 49 50 51 52 53 54 0 
55 56 57 58 59 60 61 62 63 

(Este output es un ejemplo reducido)

En donde las líneas con c son comentarios, la línea con p tiene el formato, en este caso cnf, seguido del cantidad de variables, y luego la cantidad de cláusulas.

En lógica las primeras dos líneas se pueden traducir en:
5 0 12 0 22 0 33 0 43 0
1 2 3 4 5 6 7 8 9 0 

5 ^ 12 ^ 22 ^ 33 ^ 43 ^
(1 v 2 v 3 v 4 v 5 v 6 v 7 v 8 v 9) 

#### Para correr el SudokuToSat

`> python3 SudokuToSat.py <inputs/input<numero>.txt>`

Si se omite el input tomará por defecto a inputs/input1.txt

##### Más legible SudokuToSat (traslateSat.py)

Si se quiere ver más legible se creo un programa llamado traslateSat.py

Eso retorna algo de la forma:
p(1, 3, 8) -p(9, 7, 8) ^ -p(4, 1, 8) -p(7, 5, 6) ^ -p(9, 8, 8) p(9, 8, 7)

En donde:
El - representa la negación booleana.
El ^ representa el y booleano.
El espacio entre p's representa el "o" booleano "v"
La variable que antes era un número ahora es un p(a,b,c), con "a" el dígito en la celda que se encuentra en la fila "b" y en la columna "c".

`> python3 translateSat.py`

Este programa toma por defecto el outputSudokuToSat.txt

### Resolvedor de problemas SAT (SatSolver.py)

Este programa se encarga de transformar la salida de SudokuToSat.py

Input de Ejemplo:
c Este es el tablero en CNF
p cnf 63 12
5 0 12 0 22 0 33 0 43 0
1 2 3 4 5 6 7 8 9 0 
10 11 12 13 14 15 16 17 18 0 
19 20 21 22 23 24 25 26 27 0 
28 29 30 31 32 33 34 35 36 0 
37 38 39 40 41 42 43 44 45 0 
46 47 48 49 50 51 52 53 54 0 
55 56 57 58 59 60 61 62 63 
(Esta es una salida de SudokuToSat)

A algo de la forma:

Output de Ejemplo:
c Este es el tablero en CNF 
s cnf 1 4
v -1
v 2
v -3
v -4

En donde c es una línea de comentario, y en la línea de s se encuentra "cnf" que es la forma que tenía nuestro problema en Sat, seguido tenemos un número [-1,1](-1 significa que no se logró resolver el problema en el tiempo dado, 0 significa que el tablero es insatisfacible y el 1 significa que el sudoku es satisfacible y se encontró respuesta), seguido se encuentra la cantidad de variables que se tiene.
Luego las líneas con v representan el valor, si la variable tiene - significa que su valor es falso, sino significa que su valor es verdadero.

#### Para correr el SatSolver

`> python3 SatSolver.py <T>`

Este programa toma como entrada (input) el archivo: outputs/outputSudokuToSat.txt
Y T es el tiempo el mili segundos. que estará corriendo el programa.
Si no se coloca valor para T tendrá por defecto 40000 mili segundos.

### Traductor de soluciones de SAT a soluciones de Sudoku

A partir de la salida obtenida en zChaff y en SatSolver, el SolutionToSudoku.py y el SolutionzChaffToSudoku.py devuelven el tiempo de ejecución y una visión gráfica de una solución (si el tablero de Sudoku es satisfacible)

#### Para correr los SolutionToSudoku

`> python3 SolutionToSudoku.py`

Este comando toma por defecto input: outputs/outputSatSolver.txt

`> python3 SolutionzChaffToSudoku.py`

Este comando toma por defecto input: outputs/outputszchaff.txt

## Sobre la implementación

### Implementación SudokuToSat

Para la implementación de este programa se crearon 6 métodos principales:

**initialToTrue():**
Que toma la entrada y le asigna a las variables correspondientes el valor de verdad.
Esto lo hace en O(n)

**everyCell():**
Es el método que se encarga de asegurarse de que en cada celda del sudoku exista un dígito.
Esto se hace en O(n²)

**uniqueInCell():**
Se encarga de asegurar que si se asigna true a un dígito en una celda, que no exista otro dígito en esa misma celda.
Esto se hace en O(n³)

**rowVerification():**
Se encarga de que haya un dígito de 1 a N² por cada fila.
Esto se hace en O(n⁴)

**columnVerification():**
Se encarga de que haya un dígito de 1 a N² por cada columna.
Esto se hace en O(n⁴)

**squareVerification():**
Se encarga de que en cada cuadrícula un dígito de NxN estén los números de 1 a N².
Esto se hace en O(n⁴)

Todo el procedimiento es O(n⁴). Siendo n el tamaño del tablero de sudoku y N es la raíz cuadrada de n.

### Implementación SatSolver

Se crearon 4 procedimientos importantes:

**propUnitary(elemento[0],cláusulas,valores):**
Que se encarga de agarrar el elemento[0] dentro del cláusulas arreglo de cláusulas y asignarle el valor de verdad y luego propagar ese valor eliminando sus incidencias en las demás cláusulas si este elemento estaba negado. Además modifica la información del valor de las variables en el arreglo de valores.
Esto se hace en O(m²)
Siendo m la suma del tamaño de todas las cláusulas.
Para esto también se ordenaron las cláusulas por orden de tamaño.

**propBinary(elemento[0],cláusulas,valores):**
Se encarga de eliminar del arreglo de cláusulas aquellas que no aportan información y trata de reducir las cláusulas de tamaño 2 a cláusulas de tamaño 1 para luego aplicar propagación unitaria.
Esto es simplemente unas comparaciones y luego una propagación binaria que se hace en O(m²)

Esto se podría hacer en tiempo O(m), con un gasto de memoria adicional.

**discard():**
Esta función se llama luego de haber limpiado el arreglo de cláusulas, y de haber llenado el arreglo de value (valores), y lo que hace es buscar en el arreglo de valores (value) lo que todavía no esté asignado y revisa las variables que representan su celda a ver si ya se tienen n-1 false, lo que implicaría que ese valor es true; o revisa si ya existe un true lo que significaría que el valor que se está revisando es falso. 
Esto toma O(cantidad_de_variables_no_asignadas * (n-1))
Y después de esto vuelvo a aplicar propagación unitaria. (Ya esta propagación no es tan costosa como al inicio pero sigue siendo costosa).
Dependiendo de qué tantas cláusulas existan en este momento mi O podría variar, sin embargo en la mayoría de los casos es O(m²) por la propagación unitaria.

Esta implementación está bastante a lo fuerza bruta, se puede mejorar indudablemente.

Este método es una especie de aprendizaje de implicantes, en donde con la información que se obtuvo en la primera limpieza se puede obtener más información y luego crear cláusulas unitarias que se propagan y ayudan a disminuir la cantidad de cláusulas y la cantidad de variables desconocidas.

Aprendizaje de implicantes: Dada una fórmula φ, agrega nuevas cláusulas que son implicadas por las cláusulas existentes en φ, que pueden llevar a la búsqueda a dar con una solución de forma más rápida.

Luego de haber hecho todo esto se revisa si se puede volver a realizar una limpieza con propagación unitaria, binaria y descarte, y luego de esta segunda pasada es que se aplica el Backtracking de ser necesario.

**Backtracking():**
Lo que hace es revisar el arreglo de valores (value), y al encontrar una variable sin asignar busca cuales son las posibles opciones que puede aplicar para esa variable. Eso lo hace con un método llamado opValid(), que es quien realmente ve si el agregar true o false es congruente con las cláusulas, y va agregando las opciones congruentes y les aplica otra vez backtracking para ver en una segunda vuelta las opciones congruentes dependiendo de la primera, y así sucesivamente.
Esto podría encontrar 2^n soluciones, siendo n en este caso el número de variables sin asignar. opValid() también usa propagación binaria, lo que tiene un O(2m²) que es O(m²) con m la suma del tamaño de las cláusulas.

Dependiendo de qué tanta información se pueda obtener de las cláusulas todo este procedimiento podría estar acotado por la propagación unitaria o por el backtracking, pero podría ser también con una combinación de los dos.

### Implementacion SolutionToSudoku

Para esto lo que se hizo fue crear una matriz con los datos obtenidos del programa de zChaff y el de SatSolver, y el hacer la matriz tomó o(n²) con n siendo las dimensiones del sudoku.

## La corrida de InstanciasSudoku.txt

Esto se corre con el archivo ./scriptinstancias.sh
Eso me va a retornar en la terminal y en el archivo outputs/outputinstancias.txt la resolución de los problemas.

Actualmente de 46 ejercicios 30 presentan fallas por propagación unitaria y afirman que el problema es insatisfacible.

Igual aquí se va a dejar un gráfico de rendimiento de zChaff vs nuestro programa.

Se colocó en 200 segundos los problemas que quedaron insatisfacibles en representación de que no llegaron a ninguna respuesta cuando sí la tenía.

![Gráfica de tiempos de ejecución de una muestra de 10 respuestas de sudoku](https://i.imgur.com/xuo7dTj.png)