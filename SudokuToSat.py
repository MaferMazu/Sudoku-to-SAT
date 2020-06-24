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

#Generador de variables
def variablesGenerator(sudoku):
    myalphabet = ALPHABET[:(len(sudoku))]
    print(myalphabet)
    row = 0
    variables = []
    for line in sudoku:
        column = 0
        for elem in line:
            if elem == "0":
                variables.append(["0",row,column])
            column = column + 1
        row = row + 1
    return variables

""" def rowRule(sudoku,variables):
    
    print(myalphabet)
    for row in sudoku:
        for elem in row:
            if 
                for elem in myalphabet: """

def main():
    #MAIN
    global ALPHABET
    global nTable
    ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]

    #Leo archivo de entrada de un txt
    f = open ('input1.txt','r')
    lines = f.readlines()
    nTable = 0
    for line in lines:
        length,table = getLengthAndTable(line)
        sudoku=Sudoku(length,table)
        print("Sudoku " + str(nTable) + "\n"+str(sudoku))
        variables = variablesGenerator(sudoku)
        print("Variables "+ str(nTable) + "\n"+str(variables))
        nTable = nTable + 1

if __name__ == "__main__":
    main()
    