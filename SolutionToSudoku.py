
def toSudoku(var,n):
    global ALPHABET
    var=int(var)
    #print("mi n="+str(n))
    #print(n**2)
    row = (var//(n**2))
    if var%(n**2)==0 and row!=0:
        row = row -1
    #row = str(row)
    #row = int(row[0])
    #print("Mi init var="+str(var))
    #print("Mi row="+str(row))
    var = var - row*(n**2)
    #print("Mi var - row="+str(var))
    column = (var//n)
    if var%(n)==0 and column!=0:
        column = column -1
    #column = str(column)
    #column = int(column[0])
    #print("Mi column="+str(column))
    var = var - column*n
    #print("Mi var - column="+str(var))
    digit=ALPHABET[:n][var-1]
    #print(digit,var)
    #return var
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

def main():
    #MAIN
    global ALPHABET
    global matrix
    global output
    inputfile = open ('outputrosi.txt','r')
    lines = inputfile.readlines()
    n=0
    
    
    for line in lines:
        #print(line)
        line=line.rstrip("\n")
        if len(line)>0:
            if line[0] == "s":
                token = line.split(" ")
                max = int(token[3])
                if token[2]=="1":
                    n = (float(token[3]))**(1./3.)
                    n = str(n)
                    n = int(n[0])
                    matrix = [ [ None for i in range(n+1) ] for j in range(n+1) ]
                    """ elem=[]
                    for i in range(0,n+1):
                        elem.append("0")
                    for i in range(0,n+1):
                        matrix.append(elem) """
                    #print("Matriz tamano "+str(len(matrix))+"\n"+str(matrix))
                
            elif line[0] == "v":
                max = max - 1
                #print(line[0])
                token = line.split(" ")
                if len(token[1])>0:
                    if token[1][0] != "-":
                        #print("La variable" + str(token[1]))
                        digit,row,column=toSudoku(token[1],n+1)
                        #print("p("+str(digit)+", "+str(row)+", "+str(column)+")")
                        #print(matrix[row][column])
                        matrix[row][column] = digit
                        #print(matrix)
                if max == 0:
                    printOutput(n)

    output = output + "\n"
    #print(matrix)
    print(output)

if __name__ == "__main__":
    main()