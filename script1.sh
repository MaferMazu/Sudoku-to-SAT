#!/bin/bash
echo "
"
echo "Script 1: Compara el zChaff con nuestro algoritmo para el archivo: input2.txt con T=4100
"
T=4100
mydir=$(pwd)
python3 SudokuToSat.py inputs/input2.txt
cd ..
cd zchaff64
./zchaff $mydir/outputs/outputSudokuToSat.txt $T > ../Sudoku-to-SAT/outputs/outputszchaff.txt
cd ..
cd Sudoku-to-SAT
python3 SolutionzChaffToSudoku.py outputs/outputszchaff.txt


python3 SatSolver.py $T > outputs/outputtime.txt
echo "El tiempo de nuestro algoritmo fue"
cat outputs/outputtime.txt
python3 SolutionToSudoku.py
