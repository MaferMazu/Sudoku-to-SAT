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

ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]
value = []
clausulas=[]
nClausulas=0
n=0

def SatSolver(filepath):
    global ALPHABET
    global value
    global clausulas
    global nClausulas
    global n
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
    nClausulas = len(clausulas)
    while len(clausulas)>0 and len(clausulas[0])==1:
        valid=propUnitary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop unitaria")
            break
    while nClausulas>0 and len(clausulas[0])==2:
        #print(clausulas[0])
        valid=propBinary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop binaria")
            break
    discard()
    nClausulas = len(clausulas)
    while len(clausulas)>0 and len(clausulas[0])==1:
        valid=propUnitary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop unitaria")
            break
    while nClausulas>0 and len(clausulas[0])==2:
        #print(clausulas[0])
        valid=propBinary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop binaria")
            break
    discard()
    #print(clausulas)
    #print(value)
    for i in range(1,len(value)+1):
        if value[i-1]==True:
            print(toSudoku(i,n))
    #Sols=Backtracking(value,clausulas)
    """ print(Sols)
    for j in Sols:
        for i in range(1,len(j)+1):
            if j[i-1]==True:
                print(toSudoku(i,n)) """


def propUnitary(elem_unit,clausulas,value):
    global nClausulas 
    if elem_unit[0]<0:
        if value[(elem_unit[0]*(-1))-1]==True:
            return False
        value[(elem_unit[0]*(-1))-1] = False
        for clausula in clausulas[1:]:
            if len(clausula)>1:
                if (elem_unit[0]*(-1)) in clausula:
                    index=clausula.index(elem_unit[0]*(-1))
                    clausula.pop(index)
    else:
        if value[elem_unit[0]-1]==False:
            return False
        value[elem_unit[0]-1] = True
        for clausula in clausulas[1:]:
            if len(clausula)>1:
                if (elem_unit[0]*(-1)) in clausula:
                    index=clausula.index(elem_unit[0]*(-1))
                    clausula.pop(index)
    clausulas.pop(0)
    nClausulas = nClausulas - 1
    clausulas.sort(key=len)
    return True

def propBinary(elem_bin,clausulas,value):
    global nClausulas
    
    #print(getValue(elem_bin[0]),getValue(elem_bin[1]))
    if getValue(elem_bin[0],value)==True:
        if getValue(elem_bin[1],value)==True or getValue(elem_bin[1],value)==False:
            clausulas.pop(0)
        else:
            binary=clausulas.pop(0)
            clausulas.append(binary)
            #clausulas=clausulas[1:].append(clausulas[0])
    elif getValue(elem_bin[0],value)==False:
        if getValue(elem_bin[1],value)==False:
            return False
        else:
            editValue(elem_bin[1],True,value)
            clausulas[0].pop(0)
            propUnitary(clausulas[0],clausulas,value)
    else:
        if getValue(elem_bin[1],value)==False:
            editValue(elem_bin[0],True,value)
            clausulas[0].pop(1)
            propUnitary(clausulas[0],clausulas,value)
        else:
            #print("Here")
            #print(clausulas)
            binary = clausulas[0]
            #print(binary)
            clausulas.pop(0)
            clausulas.append(binary)
            #print(clausulas)
    nClausulas=nClausulas-1
    return True


def getValue(num,value):
    pos=0
    if num<0:
        pos = num *(-1)
        if value[pos-1]!=None:
            return not value[pos-1]
    else:
        if value[num-1]!=None:
            return value[num-1]
    return None

def editValue(num,valor,value):
    pos=0
    if num<0:
        pos = num *(-1)
        value[pos-1] = not valor
    else:
        value[num-1] = valor

def toVar(digit,row,column,n):
    global ALPHABET
    digitIndex = (ALPHABET[:n]).index(digit)
    lenght = n
    maxi = (row+1) * (lenght**2)
    mini = maxi - lenght**2
    number = mini+1 + (column * lenght) + digitIndex
    return number

def Backtracking(value,clausulas):
    global n
    n = (float(len(value))**(1./3.))
    n = int(n)+1
    Sols = []
    if withOutNone(value):
        Sols.append(value)
        return Sols
    else:
        #print("Tengo none")
        clausulasval,valuesval = opValid(value,clausulas)
        #print(clausulasval,valuesval)
        for i in range(len(clausulasval)):
            Sols=Sols+Backtracking(valuesval[i],clausulasval[i])
        return Sols
    
def discard():
    global value
    global clausulas
    global n
    global nClausulas
    countFalse=0
    findTrue=False
    for i in range(len(value)):
        if value[i]==None:
            #print(value)
            #print("Encontre None en ",i)
            digit,row,column=toSudoku(i+1,n)
            #print("Este es el dig, row colim ",digit,row,column)
            for digit2 in ALPHABET[:n]:
                if digit != digit2:
                    var=toVar(digit2,row,column,n)
                    if value[var-1]==False:
                        #print("Encontre false dig row colum",digit2,row,column)
                        countFalse=countFalse+1
                    elif value[var-1]==True:
                        findTrue = True
            #print("coount false y n-1",countFalse,n-1)
            if countFalse == n-1:
                value[i]=True
                countFalse=0
                clausulas.insert(0,[i+1])
                nClausulas=nClausulas+1
                propUnitary(clausulas[0],clausulas,value)
            elif findTrue:
                #print("Asigne false")
                value[i]=False
                clausulas.insert(0,[(i*(-1))+1])
                nClausulas=nClausulas+1
                propUnitary(clausulas[0],clausulas,value)
                findTrue=False
            else:
                countFalse=0
                findTrue=False
                #print("No asigne valor")
                pass


def opValid(value,clausulas):
    global n
    global nClausulas
    valid = False
    clausulasval=[]
    valuesval=[]
    for i in range(len(value)):
        if value[i]==None:
            tryvalue = value
            tryvalue[i]=True
            tryclausulas = clausulas
            tryclausulas2 = clausulas
            print("Haré true ",i)
            tryclausulas.insert(0,[i+1])
            nClausulas=len(tryclausulas)
            #print(tryclausulas)
            while len(clausulas)>0 and len(clausulas[0])==1:
                valid=propUnitary(tryclausulas[0],tryclausulas,tryvalue)
                if not valid:
                    print("Error en prop unitaria validaciones")
                    break
            #digit,row,column=toSudoku(elem,n)
            while valid and nClausulas>0 and len(tryclausulas[0])==2:
                #print(clausulas[0])
                valid=propBinary(tryclausulas[0],tryclausulas,tryvalue)
                if not valid:
                    print("Error en prop binaria validaciones")
                    break
            if valid:
                clausulasval.append(tryclausulas)
                valuesval.append(tryvalue)
                valid=False
            
            tryvalue2 = value
            tryvalue2[i]=False
            #print(tryclausulas2)
            print("Haré false ",i)
            tryclausulas2.insert(0,[(i+1)*(-1)])
            nClausulas=len(tryclausulas2)
            #print(tryclausulas2)
            while len(tryclausulas2)>0 and len(tryclausulas2[0])==1:
                valid=propUnitary(tryclausulas2[0],tryclausulas2,tryvalue2)
                if not valid:
                    print("Error en prop unitaria validaciones")
                    break
            #digit,row,column=toSudoku(elem,n)
            while valid and nClausulas>0 and len(tryclausulas2[0])==2:
                #print(clausulas[0])
                valid=propBinary(tryclausulas2[0],tryclausulas2,tryvalue2)
                if not valid:
                    print("Error en prop binaria validaciones")
                    break
            if valid:
                clausulasval.append(tryclausulas2)
                valuesval.append(tryvalue2)

            return clausulasval,valuesval


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