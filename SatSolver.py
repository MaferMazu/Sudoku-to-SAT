from sys import argv
import signal,time

# Variables globales
ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]
value = []
clausulas=[]
nClausulas=0
n=0
output=""

# Traducir de variables a coordenadas de sudoku
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

#De coordenadas pasar al numero de la variable
def toVar(digit,row,column,n):
    global ALPHABET
    digitIndex = (ALPHABET[:n]).index(digit)
    lenght = n
    maxi = (row+1) * (lenght**2)
    mini = maxi - lenght**2
    number = mini+1 + (column * lenght) + digitIndex
    return number


#Propagacion unitaria
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


#Propagacion binaria
def propBinary(elem_bin,clausulas,value):
    global nClausulas
    
    if getValue(elem_bin[0],value)==True:
        if getValue(elem_bin[1],value)==True or getValue(elem_bin[1],value)==False:
            clausulas.pop(0)
        else:
            binary=clausulas.pop(0)
            clausulas.append(binary)
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
            binary = clausulas[0]
            clausulas.pop(0)
            clausulas.append(binary)
    nClausulas=nClausulas-1
    return True

#Obtener el valor de una variable dentro de mi arreglo value
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

#Editar el valor de una variable en mi arreglo value
def editValue(num,valor,value):
    pos=0
    if num<0:
        pos = num *(-1)
        value[pos-1] = not valor
    else:
        value[num-1] = valor


#Otra optimizacion que me permite asignar valores por casilla si ya tengo suficiente info  
def discard():
    global value
    global clausulas
    global n
    global nClausulas
    countFalse=0
    findTrue=False
    for i in range(len(value)):
        if value[i]==None:
            digit,row,column=toSudoku(i+1,n)
            for digit2 in ALPHABET[:n]:
                if digit != digit2:
                    var=toVar(digit2,row,column,n)
                    if value[var-1]==False:
                        countFalse=countFalse+1
                    elif value[var-1]==True:
                        findTrue = True
            if countFalse == n-1:
                value[i]=True
                countFalse=0
                clausulas.insert(0,[i+1])
                nClausulas=nClausulas+1
                propUnitary(clausulas[0],clausulas,value)
            elif findTrue:
                value[i]=False
                clausulas.insert(0,[(i*(-1))+1])
                nClausulas=nClausulas+1
                propUnitary(clausulas[0],clausulas,value)
                findTrue=False
            else:
                countFalse=0
                findTrue=False
                pass

#Backtracking
def Backtracking(value,clausulas):
    global n
    n = (float(len(value))**(1./3.))
    n = int(n)+1
    Sols = []
    if withOutNone(value):
        Sols.append(value)
        return Sols
    else:
        clausulasval,valuesval = opValid(value,clausulas)
        for i in range(len(clausulasval)):
            Sols=Sols+Backtracking(valuesval[i],clausulasval[i])
        return Sols


#Me devuelve lista de operaciones validas para el backtracking
def opValid(value,clausulas):
    global n
    global nClausulas
    valid = False
    clausulasval=[]
    valuesval=[]
    for i in range(len(value)):
        if value[i]==None:
            tryvalue = value.copy()
            tryvalue2 = value.copy() 
            tryclausulas = clausulas.copy()
            tryclausulas2 = clausulas.copy()

            #Probamos caso TRUE
            tryvalue[i]=True
            tryclausulas.insert(0,[i+1])
            nClausulas=len(tryclausulas)
            while len(clausulas)>0 and len(clausulas[0])==1:
                valid=propUnitary(tryclausulas[0],tryclausulas,tryvalue)
                if not valid:
                    print("Error en prop unitaria validaciones")
                    break
            while valid and nClausulas>0 and len(tryclausulas[0])==2:
                valid=propBinary(tryclausulas[0],tryclausulas,tryvalue)
                if not valid:
                    print("Error en prop binaria validaciones")
                    break
            if valid:
                clausulasval.append(tryclausulas)
                valuesval.append(tryvalue)
                valid=False
            
            #Probamos caso FALSE
            tryvalue2[i]=False
            tryclausulas2.insert(0,[(i+1)*(-1)])
            nClausulas=len(tryclausulas2)
            while len(tryclausulas2)>0 and len(tryclausulas2[0])==1:
                valid=propUnitary(tryclausulas2[0],tryclausulas2,tryvalue2)
                if not valid:
                    print("Error en prop unitaria validaciones")
                    break
            while valid and nClausulas>0 and len(tryclausulas2[0])==2:
                valid=propBinary(tryclausulas2[0],tryclausulas2,tryvalue2)
                if not valid:
                    print("Error en prop binaria validaciones")
                    break
            if valid:
                clausulasval.append(tryclausulas2)
                valuesval.append(tryvalue2)

            return clausulasval,valuesval

#Verificacion rapida de que no hay nones para backtracking
def withOutNone(value):
    for elem in value:
        if elem==None:
            return False
    return True

def handler(signum, frame):
    raise Exception("end of time")

#Resolvedor de SAT
def SatSolver(filepath):
    global ALPHABET
    global value
    global clausulas
    global nClausulas
    global n
    global output
    inputfile = open (filepath,'r')
    lines = inputfile.readlines()
    clausulas = []
    output=""
    for line in lines:
        line=line.rstrip(" \n")
        if line[0]=="c":
            output=output+line+" \n"
        else:
            if line[0]=="p":
                token=line.split(" ")
                n = (float(token[2])**(1./3.))
                n = int(n)+1
                value = [None for i in range(int(token[2]))]
                output=output+"s cnf "
            else:
                myclau = line.split(" ")
                trim = []
                for elem in myclau:
                    if elem!="0":
                        elem=int(elem)
                        trim.append(elem)
                    else:
                        if len(trim)>0:
                            clausulas.append(trim)
                        trim=[]
                if len(trim)>0:
                    clausulas.append(trim)
    
    #Ordeno las clausulas
    clausulas.sort(key=len)
    nClausulas = len(clausulas)

    #Si tengo para hacer propagacion unitaria y binaria
    while len(clausulas)>0 and len(clausulas[0])==1:
        valid=propUnitary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop unitaria")
            break
    while nClausulas>0 and len(clausulas[0])==2:
        valid=propBinary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop binaria")
            break
    
    #Aplico otra optimizacion
    discard()
    nClausulas = len(clausulas)

    #Si tengo para hacer propagacion unitaria y binaria
    while len(clausulas)>0 and len(clausulas[0])==1:
        valid=propUnitary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop unitaria")
            break
    while nClausulas>0 and len(clausulas[0])==2:
        valid=propBinary(clausulas[0],clausulas,value)
        if not valid:
            print("Error en prop binaria")
            
    #Otra optimizacion
    discard()

    #Si con eso no lo resuelve le hago backtracking
    Sols=Backtracking(value,clausulas)

    #Creo mi output
    if len(Sols)>0:
        output=output+"1 "+str(n**3)+"\n"
        for i in range(len(Sols[0])):
            if Sols[0][i]==False:
                output=output+"v -"+str(i+1)+"\n"
            elif Sols[0][i]==True:
                output=output+"v "+str(i+1)+"\n"
    elif len(Sols)==0:
        output=output+"0 "+str(n**3)+"\n"

    inputfile.close()
    
    """ print(Sols)
    for j in Sols:
        for i in range(1,len(j)+1):
            if j[i-1]==True:
                print(toSudoku(i,n)) """

def main():
    #MAIN
    global ALPHABET
    global output
    #Leo archivo de entrada de un txt
    filepath = 'outputs/outputSudokuToSat.txt'
    mytime=40000
    if len(argv) > 1:
        mytime = float(argv[1])
        mytime=mytime/1000.0
    
    start_time = time.time()
    # Register the signal function handler
    signal.signal(signal.SIGALRM, handler)

    # Define a timeout for your function
    signal.setitimer(0,mytime,0.0)

    try:
        SatSolver(filepath)
        
    except:
        output=output+"-1 "+str(n**3)+"\n"
    outputfile = open('outputs/outputSatSolver.txt',"w+")
    outputfile.write(output)
    outputfile.close()
    print(time.time() - start_time)
    #print(output)

if __name__ == "__main__":
    main()