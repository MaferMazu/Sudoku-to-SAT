from sys import argv
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

ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]
value = []
clausulas=[]
def SatSolver(filepath):
    global ALPHABET
    global value
    global clausulas
    inputfile = open (filepath,'r')
    lines = inputfile.readlines()
    clausulas = []
    for line in lines:
        line=line.rstrip(" \n")
        if line[0]=="c":
            print(line)
        else:
            if line[0]=="p":
                token=line.split(" ")
                n = (float(token[2])**(1./3.))
                n = int(n)+1
                value = [None for i in range(int(token[2]))]
            else:
                myclau = line.split(" ")
                #print(myclau)
                trim = []
                for elem in myclau:

                    #print(elem)
                    if elem!="0":
                        #print(elem)
                        elem=int(elem)
                        trim.append(elem)
                        #print(trim)
                    else:
                        if len(trim)>0:
                            clausulas.append(trim)
                        trim=[]
                if len(trim)>0:
                    clausulas.append(trim)
    clausulas.sort(key=len)
    #print(clausulas)
    while len(clausulas)>0 and len(clausulas[0])==1:
        propUnitary(clausulas[0])
    print(clausulas)
    print(value)
    if len(clausulas)>0 and len(clausulas[0])==2:
        propBinary(clausulas[0])
    for i in range(1,len(value)+1):
        if value[i-1]==True:
            print(toSudoku(i,n))


def propUnitary(elem_unit):
    global clausulas
    global value

    if elem_unit[0]<0:
        value[(elem_unit[0]*(-1))-1] = False
        for clausula in clausulas[1:]:
            if len(clausula)>1:
                if (elem_unit[0]*(-1)) in clausula:
                    index=clausula.index(elem_unit[0]*(-1))
                    clausula.pop(index)
    else:
        value[elem_unit[0]-1] = True
        for clausula in clausulas[1:]:
            if len(clausula)>1:
                if (elem_unit[0]*(-1)) in clausula:
                    index=clausula.index(elem_unit[0]*(-1))
                    clausula.pop(index)
    clausulas.pop(0)
    clausulas.sort(key=len)

def propBinary(elem_bin):
    global clausulas
    for i in range(0,1):
        if elem_bin[i]<0:
            pos = elem_bin[i] *(-1)
            if value[pos]==True:
                #index=elem_bin.index(elem_bin[i])
                elem_bin.pop(i)
                propUnitary(elem_bin[0])
            else:
                if elem_bin[i-1]<0:
                    pos = elem_bin[i] *(-1)
                    if value[pos]==True:
                        clausulas.pop(0)
                        break
                else:
                    if value[elem_bin[i-1]]==True:
                        clausulas.pop(0)
                        break

        else:
            if value[elem_bin[i]]==False:
                #index=elem_bin.index(elem_bin[i])
                elem_bin.pop(i)
                propUnitary(elem_bin[0])
            else:
                if elem_bin[i-1]<0:
                    pos = elem_bin[i] *(-1)
                    if value[pos]==True:
                        clausulas.pop(0)
                        break
                else:
                    if value[elem_bin[i-1]]==True:
                        clausulas.pop(0)
                        break
    

def Backtracking(value):
    n = (float(len(value))**(1./3.))
    n = int(n)+1
    Sols = []
    if withOutNone(value):
        Sols.append(value)
        return Sols
    for elem in value:
        if elem==None:
            digit,row,column=toSudoku(elem,n)

def withOutNone(value):
    for elem in value:
        if elem==None:
            return False
    return True

def main():
    #MAIN
    global ALPHABET
    #Leo archivo de entrada de un txt
    filepath = 'outputs/output.txt'
    if len(argv) > 1:
        filepath = argv[1]
    SatSolver(filepath)

if __name__ == "__main__":
    main()