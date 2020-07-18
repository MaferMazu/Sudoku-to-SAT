from sys import argv
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


ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]
matrix = []
output = ""

def SolutionToSudoku(filepath):
    global ALPHABET
    global matrix
    global output
    inputfile = open (filepath,'r')
    lines = inputfile.readlines()
    n=0
    count = 0
    variables=[]
    number = 1
    time=-1
    for line in lines:
        if count == 5:
            line=line.rstrip("\n")
            variables = line.split(" ")[:-3]
            count = count + 1
        elif count == 9:
            line=line.rstrip("\n")
            token = line.split("\t")
            number = int(token[-1])
            n = (float(number))**(1./3.)
            n = int(n)
            matrix = [ [ "0" for i in range(n+1) ] for j in range(n+1) ]
            for elem in variables:
                if len(elem)>0:
                    if elem[0] != "-":
                        digit,row,column=toSudoku(elem,n+1)
                        matrix[row][column] = digit
            count = count +1
            
        elif count == 19:
            line=line.rstrip("\n")
            token = line.split("\t")
            time = token[-1]
            count = count +1
            print("El tiempo de zChaff fue de: "+str(time))
        else:
            count = count +1
    printOutput(n)
    print(output)




def main():
    #MAIN
    global ALPHABET
    global matrix
    global output
    filepath = 'outputs/outputszchaff.txt'
    if len(argv) > 0:
        filepath = argv[1]
    SolutionToSudoku(filepath)
    

if __name__ == "__main__":
    main()