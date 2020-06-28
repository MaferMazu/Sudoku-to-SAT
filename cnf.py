#Import Libraries
import re
######################################################
# cells_asociation: Map the set of values to their
# respective Sudoku Cell

def cells_association(n):
    diccionario = {}

    for i in range(n**4):    
        j = (i*(n**2))+1
        top = ((i+1)*(n**2))
        while (j <= top):
            # SON LOS VALORES DE LA COLUMNA
            diccionario[str(j)]= i            
            j = j+1
            
    return diccionario
######################################################
# values_asociation: Map the set of values to their
# respective Sudoku Number

def values_association(n):
    diccionario = {}

    for i in range(n**4):    
        j = (i*(n**2))+1
        top = ((i+1)*(n**2))
        while (j <= top):
            # SON LOS VALORES DE LA COLUMNA
            diccionario[str(j)]= j-4*i           
            j = j+1
            
    return diccionario

######################################################
# boolean_asociation: fit the boolean value of
# each variable in the starting state

def boolean_association(n, fijos):
    diccionario = {}

    for i in range(n**4):    
        j = (i*(n**2))+1
        top = ((i+1)*(n**2))
        while (j <= top):
            # SON LOS VALORES DE LA COLUMNA
            if (j in fijos):
                diccionario[str(j)]= True           
            else:
                diccionario[str(j)]= None
            j = j+1
                
    return diccionario
######################################################
######################################################
# getTable: return an array with the strings of the
#document file_array
######################################################
def getTable(file_array):
    dimension = 0
    n = 0
    clausulas = 0
    for linea in file_array:
        patron_C = re.search('c', linea)
        if (patron_C != None):
            if(patron_C.start()!=0):
                values = re.split(' ', linea)
                dimension = int(values[2])
                clausulas = int(values[3])
                if (dimension == 4):
                    n = 1
                    break
                if (dimension == 64):
                    n = 2
                    break
                if (dimension == 729):
                    n = 3
                    break
                if (dimension == 4096):
                    n = 4
                if (dimension == 15625):
                    n = 5
                    break
                if (dimension == 46656):
                    n = 6
                    break
                else:
                    print("invalid dimension")
    file_array.pop(0)
    file_array.pop(0)
    return file_array, n, dimension, clausulas

archivo = open("cnf.txt", "r")

file_array = archivo.readlines()
archivo.close()

file_array, n, dimension, clausulas = getTable(file_array)

asignados = re.split(" 0", file_array[0])
file_array.pop(0)
asignados.pop()

fijos = [int(x) for x in asignados]
conjunciones = re.split("0", file_array[1])

#print(fijos)    
#print(clausulas)
#print(conjunciones)


mapeo_posicion = cells_association(n)
mapeo_valor = values_association(n)
mapeo_boolean = boolean_association(n,fijos)
#def cell_market(f,p):

 #   for v i fijos:
        
#celdas_ocupadas = cell_market(fijos, mapeo_posicion)
#mapeo_booleano = boolean_values(asignados, asignados_values, asignados_posicion)
#print(mapeo_posicion)
#print(mapeo_valor)
print(mapeo_boolean)

#print (mapeo_boolean["1"])

for linea in file_array:
    disjunciones = re.split(" 0 ", linea)
    disjunciones.pop()
    #print(disjunciones)
print("###############################################")
for j in fijos:
    val = mapeo_valor[str(j)]
    for x in range(0,n,n**2):
        if(mapeo_boolean[str(x+val)]!=True):
            mapeo_boolean[str(x+val)] = False
print(mapeo_boolean)
    

#x = [int(x) for x in range(0,n**6,n**2)]
