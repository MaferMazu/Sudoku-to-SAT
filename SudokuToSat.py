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
            if elem == "0":
                for digit in ALPHABET[:(len(sudoku))]:
                    var = toVar(digit,row,column,sudoku)
                    expresion = expresion + str(var) + " "
                expresion = expresion + "0 \n"
                nConjunctions = nConjunctions + 1
            column = column + 1
        row = row + 1
    expresion = expresion + "\n"
    nConjunctions = nConjunctions - 1

#Todas las filas deben tener los numeros de 1 a n
""" def rowVerification(sudoku):
    global expresion
    global nConjunctions
    global ALPHABET
    row = 0
    for line in sudoku:
        column = 0
        for elem in line:
            if elem == "0":
                for digit in ALPHABET[:(len(sudoku))]:
                    var = toVar(digit,row,column,sudoku)
                    expresion = expresion + "-"+str(var) + " "
                expresion = expresion + "0 \n"
                nConjunctions = nConjunctions + 1
            column = column + 1
        row = row + 1
    expresion = expresion + "\n"
    nConjunctions = nConjunctions - 1 """
        

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



def main():
    #MAIN
    global ALPHABET
    global nTable
    #Leo archivo de entrada de un txt
    inputfile = open ('input1.txt','r')
    lines = inputfile.readlines()
    nTable = 0
    outputfile = open('output.txt',"w+")
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
        output = output + "p cnf " + str((len(sudoku))**3) + " " + str(nConjunctions) + "\n"
        output = output + str(expresion) + "\n"
        print(output)
        outputfile.write(output)
        nTable = nTable + 1
    outputfile.close()
    inputfile.close()


if __name__ == "__main__":
    main()
    