#!/bin/bash
python3 instanciasToFile.py
T=60000
mydir=$(pwd)
for i in {1..46}
do
    echo "instanciasSudoku" $i
    python3 SudokuToSat.py instanciasSudoku/input$i.txt
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
done | tee outputs/outputsInstancias.txt

