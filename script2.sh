#!/bin/bash
echo "
"
echo "Script 2 to compare zChaff and own programm input1.txt
"
T=4100
python3 SudokuToSat.py inputs/input1.txt > outputs/output.txt
cd ..
cd zchaff64
./zchaff ~/Documents/Diseño\ de\ Algoritmos/Sudoku-to-SAT/outputs/output.txt $T > ../Sudoku-to-SAT/outputs/outputs1zchaff.txt
cd ..
cd Sudoku-to-SAT
python3 SolutionzChaffToSudoku.py outputs/outputs1zchaff.txt
