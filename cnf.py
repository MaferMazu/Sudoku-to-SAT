#Import Libraries
import re
import numpy as np

######################################################
def valido(arr):
    if(arr[1] == "cnf"):
        return true
    else:
        return false
#####################################################    
def getEmptyMatrix(n):
    main_matrix = []
    for i in range(n):
        main_matrix.append([])
    return main_matrix
#####################################################    
def crear_archivo(sat_sol):
    f = open ('sat_solution.txt','w')
    f.write('c Ejemplo de solución para fórmula en CNF\nc\n')
    tam = len(sat_sol)
    if (sat_sol == []):
        f.write('s cnf '+str(0)+" "+str(tam)+"\n")
    else:
        f.write('s cnf '+str(1)+" "+str(tam)+"\n")
        for i in range(tam):
            f.write('v '+str(sat_sol[i])+"\n")
    f.close()
####################################################
def validar_tablero(tablero, dim, negativos):
    solucion = False
    values = []
    
    while(not solucion):
        
        for i in range(dim):
            try:
                indices=np.where(tablero[i] == True)
            except ValueError:
#                print("buscar los negativos")
                for neg in negativos:
#                    print("verificar si alguno esta en esa fila")
                    if (neg[0]==i):
                        values = cambiar_negativo(negativos,tablero,i,dim)
                        break
            else:
#                print("indices:")
#                print(indices[0])
#                print("values:")
#                print(values)
                values = np.unique(np.concatenate((values,indices[0])).astype(int))
        break
        
    return values

######################################################
def cambiar_negativo(negaciones, table, line, r):
#    print("................................")
    for t in negaciones:

        if (t[0]==line and table[line][t[1]]==False):
            column = t[1]
            
            for i in range(r):
                
                if( table[i][column]==False):
                    table[i][column]=True
                else:
                    table[i][column]=False
            break
            
    val = validar_tablero(table,r,negaciones)
#    print("+++++++++++++")
    for i in range(len(val)):
#        print(val[i])
        for j in negaciones:
#            print("negaciones:")
#            print(j)
            if (j[1]==i):
#               print("    encontró una:")
                val[i]= -val[i]
#    print("+++++++++++++")
    return val       
                
######################################################

archivo = open("cnf.txt", "r")

num_var = 0
num_conj = 0
tablero = np.array([])
row = 0
negatives = []
file_array = archivo.readlines()
archivo.close()

for linea in file_array:
    patron_C = re.search('c', linea)

    if (patron_C==None):
        #This case means the line has not a 'c' so is neither the commentary
        #neither the p
        
        for indx in linea.split(" "):
            indice = int(indx)
            if (indice>=0):
                tablero[row][indice]=True
            else:
                negatives.append([row,-indice])
        row = row+1   
    else:
        if(patron_C.start()!=0):
            values = re.split(' ', linea)
            num_var = int(values[2])+1
            num_conj = int(values[3])
            tablero = np.zeros((num_conj, num_var), dtype=bool)    
    
#print(tablero)
#print()
#print(negatives)

solucion = cambiar_negativo(negatives,tablero,2,3)
print("LA SOLUCION:")
crear_archivo(solucion)
print(solucion)

