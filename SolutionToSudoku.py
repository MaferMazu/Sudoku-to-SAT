from sys import argv

#Variables globales
ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]
matrix = []
output = ""

#Traducir de variable a tablero de sudoku
def toSudoku(var,n):
    global ALPHABET
    var=int(var)
    row = (var//(n**2))
    if var%(n**2)==0 and row!=0:
        row = row -1
    var = var - row*(n**2)
    column = (var//n)
    if var%(n)==0 and column!=0:
        column = column -1
    var = var - column*n
    digit=ALPHABET[:n][var-1]
    return digit,row,column

#Imprimir el output
def printOutput(n):
    global matrix
    global output
    inline=""
    insquare=""
    for i in range(0,n+1):
        for j in range(0,n+1):
            inline = inline + str(matrix[i][j])
            insquare = insquare + str(matrix[i][j]) + " "
        insquare = insquare + "\n"
    output = output + "\n" + str(n+1) + " "+ inline + "\n"
    output = output + insquare + "\n"

#Implementacion de la transformacion
def SolutionToSudoku(filepath):
    global ALPHABET
    global matrix
    global output
    inputfile = open (filepath,'r')
    lines = inputfile.readlines()
    n=0
    satisfa=False
    for line in lines:
        line=line.rstrip("\n")
        if len(line)>0:
            if line[0] == "s":
                token = line.split(" ")
                max = int(token[3])
                if token[2]=="1":
                    n = (float(token[3]))**(1./3.)
                    n = int(n)
                    matrix = [ [ "0" for i in range(n+1) ] for j in range(n+1) ]
                    satisfa=True
                elif token[2]=="0":
                    output=output+"Es insatisfacible\n"
                elif token[2]=="-1":
                    output=output+"No se logró resolver en el tiempo dado\n"
                
            elif line[0] == "v" and satisfa:
                max = max - 1
                token = line.split(" ")
                if len(token[1])>0:
                    if token[1][0] != "-":
                        digit,row,column=toSudoku(token[1],n+1)
                        matrix[row][column] = digit
                if max == 0:
                    printOutput(n)
                    satisfa=False

    print(output)


def main():
    #MAIN
    global ALPHABET
    global matrix
    global output
    filepath = 'outputs/outputSatSolver.txt'
    if len(argv) > 1:
        filepath = argv[1]
    SolutionToSudoku(filepath)
    

if __name__ == "__main__":
    main()