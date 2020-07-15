from sys import argv
#Obtener informacion de un tablero
def getLengthAndTable(line):
    tokens = line.split()
    length = int(tokens[0])
    table = tokens[1]
    if length**4 != len(table):
        print("Las dimensiones de este tablero "+ nTable +" no son correctas")
        return None,None
    else:
        return length,table

#Creo el tablero
def Sudoku(length,table):
    sudoku = []
    count=0
    while count < length**4:
        if count%(length**2)==0:
            sudoku.append([table[count]])
        else:
            sudoku[-1].append(table[count])
        count = count + 1
    return sudoku

#Generador de verdad de los valores iniciales
def initialToTrue(sudoku):
    global expresion
    global nConjunctions
    row = 0
    first = True
    for line in sudoku:
        column = 0
        for elem in line:
            if elem != "0":
                var = toVar(elem,row,column,sudoku)
                if first:
                    expresion = expresion + str(var)
                    first = False
                else:
                    expresion = expresion + " 0 " + str(var)
                nConjunctions = nConjunctions + 1
            column = column + 1
        row = row + 1
    if len(expresion)!=0:
        expresion = expresion + " 0\n"

#Todas las casillas deben tener un num entre 1 y n
def everyCell(sudoku):
    global expresion
    global nConjunctions
    global ALPHABET
    row = 0
    for line in sudoku:
        column = 0
        for elem in line:
            for digit in ALPHABET[:(len(sudoku))]:
                var = toVar(digit,row,column,sudoku)
                expresion = expresion + str(var) + " "
            expresion = expresion + "0 \n"
            nConjunctions = nConjunctions + 1
            column = column + 1
        row = row + 1
    #expresion = expresion + "\n"

def uniqueInCell(sudoku):
    global expresion
    global nConjunctions
    global ALPHABET
    row = 0
    for line in sudoku:
        column = 0
        for elem in line:
            for digit in ALPHABET[:(len(sudoku))]:
                var = toVar(digit,row,column,sudoku)
                for digit2 in ALPHABET[:(len(sudoku))]:
                    var2 = toVar(digit2,row,column,sudoku)
                    if var2 != var:
                        expresion = expresion + "-"+str(var) + " " + "-"+str(var2)+ " 0 "
                        nConjunctions = nConjunctions + 1
            expresion = expresion + "\n"
            #nConjunctions = nConjunctions + 1
            column = column + 1
        row = row + 1
    

#Todas las filas deben tener los numeros de 1 a n
def rowVerification(sudoku):
    global expresion
    global nConjunctions
    global ALPHABET
    row = 0
    for line in sudoku:
        column = 0
        for elem in line:
            for digit in ALPHABET[:(len(sudoku))]:
                var = toVar(digit,row,column,sudoku)
                disjun = "-"+str(var) + " "
                for i in range(0,len(sudoku)):
                    if i != column:
                        var = toVar(digit,row,i,sudoku)
                        expresion = expresion + disjun + "-"+str(var)+ " 0 "
                        nConjunctions = nConjunctions + 1    
            expresion = expresion + "\n"  
            column = column + 1
        row = row + 1
    #expresion = expresion + "\n"

#Todas las columnas deben tener los numeros de 1 a n
def columnVerification(sudoku):
    global expresion
    global nConjunctions
    global ALPHABET
    row = 0
    for line in sudoku:
        column = 0
        for elem in line:
            for digit in ALPHABET[:(len(sudoku))]:
                var = toVar(digit,row,column,sudoku)
                disjun = "-"+str(var) + " "
                for i in range(0,len(sudoku)):
                    if i != row:
                        var = toVar(digit,i,column,sudoku)
                        expresion = expresion + disjun + "-"+str(var)+ " 0 "
                        nConjunctions = nConjunctions + 1    
            expresion = expresion + "\n"  
            column = column + 1
        row = row + 1
    #expresion = expresion + "\n"

#Todas los cuadrantes deben tener los numeros de 1 a n
def squareVerification(sudoku):
    global expresion
    global nConjunctions
    global ALPHABET
    squareLen= (float(len(sudoku)))**(1./2.)
    squareLen = str(squareLen)
    squareLen = int(squareLen[0])
    row = 0
    for line in sudoku:
        column = 0
        for elem in line:
            squareRow= row//squareLen
            #print("squareRow "+str(squareRow))
            squareColumn = column//squareLen
            #print("squareColumn "+str(squareColumn))
            for digit in ALPHABET[:(len(sudoku))]:
                var = toVar(digit,row,column,sudoku)
                disjun = "-"+str(var) + " "
                for i in range(squareRow*squareLen,squareRow*squareLen+squareLen):
                    for j in range(squareColumn*squareLen,squareColumn*squareLen+squareLen):
                        #print("Mi i y j "+str(i)+", "+str(j))
                        if i != row or j !=column:
                            #print("Mi i y j distinto a en donde estoy"+str(i)+", "+str(j))
                            var = toVar(digit,i,j,sudoku)
                            expresion = expresion + disjun + "-"+str(var)+ " 0 "
                            nConjunctions = nConjunctions + 1    
            expresion = expresion + "\n"  
            column = column + 1
        row = row + 1
    #expresion = expresion + "\n"


        

#Convertir en variable
def toVar(digit,row,column,sudoku):
    global ALPHABET
    digitIndex = (ALPHABET[:(len(sudoku))]).index(digit)
    lenght = len(sudoku)
    maxi = (row+1) * (lenght**2)
    mini = maxi - lenght**2
    number = mini+1 + (column * lenght) + digitIndex
    return number


expresion = ""
nConjunctions = 0
ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]

def SudokuToSat(filepath):
    global ALPHABET
    global nTable
    inputfile = open (filepath,'r')
    lines = inputfile.readlines()
    nTable = 0
    outputfile = open('outputs/output.txt',"w+")
    for line in lines:
        global nConjunctions
        global output
        global expresion
        expresion = ""
        nConjunctions = 0
        output = "c Este es el tablero " + str(nTable) + " en CNF\n"
        length,table = getLengthAndTable(line)
        sudoku=Sudoku(length,table)
        initialToTrue(sudoku)
        everyCell(sudoku)
        uniqueInCell(sudoku)
        rowVerification(sudoku)
        columnVerification(sudoku)
        squareVerification(sudoku)
        expresion = expresion[:-3]
        output = output + "p cnf " + str((len(sudoku))**3) + " " + str(nConjunctions) + "\n"
        output = output + str(expresion) + "\n"
        print(output)
        outputfile.write(output)
        nTable = nTable + 1
    outputfile.close()
    inputfile.close()

def main():
    #MAIN
    global ALPHABET
    global nTable
    #Leo archivo de entrada de un txt
    filepath = 'inputs/input1.txt'
    if len(argv) > 1:
        filepath = argv[1]
    SudokuToSat(filepath)
    


if __name__ == "__main__":
    main()