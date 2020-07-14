import re

###########################################                
def solution():
    v = []
    for k in mapeo_boolean.keys():
        if (mapeo_boolean[k]):
            v.append(mapeo_valor[k])
    return v
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
######################################################
# boolean_asociation: fit the boolean value of
# each variable in the starting state
def get_columns(v,n):
    col = mapeo_column[v]
    val = mapeo_valor[v]
    casilla = n*col+val
    a = []
    for i in range(n**2):
        c = val + i*(n**4)
        a.append(str(c))
    return a
######################################################
# boolean_asociation: fit the boolean value of
# each variable in the starting state

def boolean_association(n, fijos):
    diccionario = dict.fromkeys(mapeo_posicion.keys(),None)
    for i in fijos:
        diccionario[str(i)] = True 
        fila = mapeo_fila[str(i)]
        columna = mapeo_column[str(i)]
        valor = mapeo_valor[str(i)]
        for j in diccionario.keys():
            v = mapeo_valor[j]
            f = mapeo_fila[j]
            c = mapeo_column[j]
            if(((f==fila)or(c==columna)) and (valor==v) and not (str(i)==j)):
                diccionario[j] = False
            #else:   CASO CUADRICULAS EN PROCESO
    return diccionario
######################################################
######################################################
# colum_asociation: fit the boolean value of
# each variable in the starting state
def col_association(n):
    diccionario = dict.fromkeys(mapeo_posicion.keys(),0)
    col = 0
    i = -1
    for j in range(n**6):
        diccionario[str(j+1)]=col
        i = i+1
        if (i == 3):
            col = col+1
            i = -1
        if (col==4):
            col=0
    return diccionario
######################################################
######################################################
# row_asociation: fit the boolean value of
# each variable in the starting state
def row_association(n):
    diccionario = dict.fromkeys(mapeo_posicion.keys(),0)
    row = 0
    contador = 0
    for j in range(len(diccionario)):        
        diccionario[str(j+1)] = row
        contador=contador+1
        if (contador==n**4):
            row = row+1
            contador = 0
        
    return diccionario
######################################################
# Primero: leer extraer el contenido del documento
######################################################
def getTable(file_array):
    dimension = 0
    n = 0
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
#########################################################
#get_clausules(): Take an array of clausules and return
# a new array with the position of each clausule that co-
#tains the variable for example x1vx2 ^ -x3 ^ x2vx3
# will return the array [[0],[0,2],[1,2]]
#This will be used to compare more easly the clausules


def get_clausules(clausulas, n_clausulas):
    var_clausule_position = []
    for i in range(len(clausulas)):
        p = [int(x) for x in clausulas[i]]
        clausulas[i] = p
    return clausulas

###########################################
# REDUCCION DE CLAUSULAS
###########################################
# Se Asignan los valores unitarios y
# las clausulas de tamaño dos cuyas variables
# solo satisfacen la clausula con un solo valor
def propagacion_unitaria(clausulas):
    it1 = -1
    
    for c in clausulas:
        it1=it1+1
        i = -1
        for lista in c:
            i=i+1
            #ASIGNACION DE UNICIDAD POR CLAUSULA
            if (len(lista)==2):
                v1 = mapeo_boolean[str(abs(lista[0]))]
                v2 = mapeo_boolean[str(abs(lista[1]))]

                if ((v1==None) ^ (v2==None)):
                    assigSecondVariable(lista)
                    
            #ASIGNACION DE UNICIDAD POR CELDA: Si la celda ya esta asignada se ponen todos 
            #los valores faltantes en False
            if(len(lista)>2):
                var_asignada = hayTrue(lista)
                if(var_asignada!=None):
                    for elem in lista:
                        if(elem != var_asignada):
                            mapeo_boolean[str(abs(elem))] = False
                tam = 0
                long =len(lista)-1
            #ASIGNACION Y DESCARTE: se descartan variables ya asignadas, si el resultado
            #tiene longitud 1 se asigna True (ASIGNACION POR DESCARTE)
                for v in reversed(lista):
                    if (mapeo_boolean[str(abs(v))] != None):
                        lista.pop(long-tam)
                    tam=tam+1
                if (len(lista)==1):
                    mapeo_boolean[str(abs(lista[0]))]=True
                    lista.pop()
#--------------------------------------------------------------
def hayTrue(clausula):
    v = None
    for var in clausula:
        if(mapeo_boolean[str(abs(var))]==True):
            v = var
            break
    return v
#--------------------------------------------------------------
# Input: Se recibe una clausula de dos variables con una sola
# ya asignada.
# Processing: si la variable asignada evalúa True, se ignora la
# clausula. Si evalua False, se asigna a la otra variable el
# valor único que asegura que evalue a verdadero la clausula
#Output: void.

def assigSecondVariable(clausula):
    
    v1 = mapeo_boolean[str(abs(clausula[0]))]
    v2 = mapeo_boolean[str(abs(clausula[1]))]
    
    if( v1==None ):
        if(clausula[1]<0 and v2):
            if(clausula[0]<0):
                mapeo_boolean[str(abs(clausula[0]))] = False
            else:
                mapeo_boolean[str(abs(clausula[0]))] = True
        elif((clausula[1]>0 and not v2)):
            if(clausula[0]<0):
                mapeo_boolean[str(abs(clausula[0]))] = False
            else:
                mapeo_boolean[str(abs(clausula[0]))] = True            
    else:
        if(clausula[0]<0 and v1):
            if(clausula[1]<0):
                mapeo_boolean[str(abs(clausula[1]))] = False
            else:
                mapeo_boolean[str(abs(clausula[1]))] = True
        elif((clausula[0]>0 and not v2)):
            if(clausula[1]<0):
                mapeo_boolean[str(abs(clausula[1]))] = False
            else:
                mapeo_boolean[str(abs(clausula[1]))] = True
#--------------------------------------------------------------
def tiene_None(clausula):
    existe_none = False
    #print(estado)
    for c in clausula:
        if(mapeo_boolean[str(abs(c))] == None):
            existe_none = True
            break
    return existe_none
#--------------------------------------------------------------
def limpiar_clausulas(clausula):
    
    tam = len(clausula)
    # Lista Principal de Clausulas
    #print("ANTES")
    #print(clausula[2])
    for i in range(tam):
        pos = 0
        indices = []
        # Clausulas por celda
        for j in clausula[i]:
            if(not tiene_None(j)):
                indices.insert(0,pos)
            pos = pos+1
        for index in indices:
            clausula[i].pop(index)
    #print("DESPUES")
    #print(clausula[2])
#-----------------------------------------------------------------
def get_nones(clave):
    if (mapeo_boolean[clave]==None):
        return [int(clave)]
    else:
        return []
#-----------------------------------------------------------------
def clausule_association(var,clausulas):
    tam = len(clausulas)
    asociaciones = []
    for v in var:
        aparecio = False
        clausula_por_variable = []
        for cl in clausulas:
            for c in cl:
                if ((v in c) or (-v in c)):
                    aparecio = True
                    clausula_por_variable.append(c)
        if(aparecio):
            asociaciones.append(clausula_por_variable)
    return asociaciones
#############################################################
# FUNCIONES EXTERNAS PARA EL BACKTRACKING
#############################################################
def new_true(estado, n):
    estado[str(n)] = True
    return estado

def new_false(estado, n):
    estado[str(n)] = False
    return estado

#############################################################
# INVOCACION DEL BACKTRACKING
#############################################################
def SAT2(no_asignados, clausulas):
    root = Nodo2(no_asignados, clausulas)
    sol = root.search_valid_states(True)
    solucion=solution()
    print(solucion)
    print(len(solucion))
    

 
#############################################################
# CLASE NODO2
#############################################################
class Nodo2:
    def __init__(self, variables, clausulas):
        self.variables= variables
        self.clausulas = clausulas
        
    def tiene_none(self,clausula):
        existe_none = False
        val =-1
        #print(estado)
        for c in clausula:
            if(mapeo_boolean[str(abs(c))] == None):
                existe_none = True
                val=c
                break
        return val, existe_none
    
    def evalua_true(self,clausula):
        aux = False        
        for c in clausula:
            if (c < 0):
                aux = aux or (not mapeo_boolean[str(abs(c))])
            else:
                aux = aux or mapeo_boolean[str(c)]
                
        return aux
    # LA BUSQUEDA SIEMPRE SE INICIA CON TRUE
    #EN CASO DE NO SATISFACER UNA CLAUSULA SE ESTUDIA EL CASO FALSE
    def search_valid_states(self,caso):
        #mapeo_boolean[str(self.variables[index])] = case
        #aux = self.variables.copy()
        #var = aux.pop(0)
        index=0
        hay_solucion=True
        #Ciclo verdadero
        #while index<len(self.clausulas):
        #Ciclo Pruebas
        while index<1:
            print("ITERACION")
            print(str(index))
            if (not self.buscar(caso, index)):
                hay_solucion =False
                break
            index=index+1
            print(mapeo_boolean)
            print("")
        return hay_solucion
    
    def buscar(self,case,index):
        
        mapeo_boolean[str(self.variables[index])] = case
        #print("CASO: "+str(case)+" VARIABLE: "+str(self.variables[index]))
        
        for c in self.clausulas[index]:
            print()
            print("   CLAUSULA: "+str(c))
            print("CLAUSULAS:")
            print(self.clausulas[index])
            print("")
            
            # ATIENDE LOS CASOS SI O NO DE NONE!
            var_con_none, existeN = self.tiene_none(c)
            if(not existeN):
                print("      ENTRO EN CASO NO EXISTEN NONE:")
                if(not self.evalua_true(c)):
                    print("        No Evalua True")
                    print(mapeo_boolean[str(abs(c[0]))])
                    print(mapeo_boolean[str(abs(c[1]))])
                    break
                    if(case):
                        return (True and self.buscar(False,index))
                    else:
                        return False
            else:
                #print("      ENTRO EN CASO EXISTE NONE:")
                i = self.variables.index(abs(var_con_none))
                #print("        el NONE es :"+str(i))
                if(self.buscar(True,i)):
                    #print("        HAY SOLUCION PARA FALSO")
                    continue
                else:
                    if(self.buscar(False,i)):
                        #print("        HAY SOLUCION PARA TRUE")
                        continue
                    else:
                        if(case==True):
                            return (True and self.buscar(False,index))
                        else:
                            return False
        return True            
                    
#########################################################
def main():
    #MAIN
    global mapeo_posicion  # Numero
    global mapeo_valor # Celda
    global mapeo_column  # columna
    global mapeo_fila  # fila
    global mapeo_boolean # Valor Booleano Asignado
    archivo = open("output2.txt", "r")
    file_array = archivo.readlines()
    archivo.close()

    file_array, n, dimension, n_clausulas = getTable(file_array)
    asignados = re.split(" 0", file_array[0])
    asignados.pop()
    fijos = [int(x) for x in asignados]
    #print("ASIGNADOS")
    #print(asignados)
    #print("")
    mapeo_posicion = cells_association(n) # Numero
    mapeo_column = col_association(n) # Columna
    mapeo_fila = row_association(n)   # Fila
    mapeo_valor = values_association(n)   # Celda
    mapeo_boolean = boolean_association(n,fijos) # Valor Booleano Asignado

    #disj = []
    count = 1
    unit_clausules = [[] for j in range(n**4)]
    
    #for linea in file_array:

     #   disjunciones = re.split(" 0 ", linea)
      #  if(disjunciones[len(disjunciones)-1]=="\n"):
       #     disjunciones.pop()
        #disj.append(disjunciones)

    firstCicle=True
    n_to_pwr_4 = n**4
    
    for linea in file_array[1:]:
        if firstCicle and count > n_to_pwr_4:
            firstCicle = False
        rest = count%(n_to_pwr_4)
        disjunciones = re.split(" 0 ", linea)
        if(disjunciones[len(disjunciones)-1]=="\n"):
            disjunciones.pop()
        if not firstCicle:
            if rest ==0:
                unit_clausules[(n_to_pwr_4)-1] = unit_clausules[(n_to_pwr_4)-1] + disjunciones
            else:
                unit_clausules[rest-1]=unit_clausules[rest-1]+disjunciones
        else:
            if rest == 0:
                unit_clausules[(n_to_pwr_4)-1]=disjunciones
            else:
                  unit_clausules[rest-1]=disjunciones
        count = count + 1

    # SE AGRUPAN LAS CLAUSULAS EN GRUPOS RESPECTIVOS A
    #CLAUSULA POR CELDAS
    #print(unit_clausules)
    clausula = []
    for e in unit_clausules:
        group = []
        for i in range(len(e)):
            group.append(re.split(" ",e[i]))
            if("\n" in group[len(group)-1]):
                group[len(group)-1].pop()
            group = get_clausules(group, len(group))
        clausula.append(group)
    # SE PROCEDE A ASIGNAR LAS CLAUSULAS BINARIAS CON
    # VALORES UNICOS
    propagacion_unitaria(clausula)
    # SE ELIMINAN LAS CLAUSULAS CUYAS VARIABLES ESTEN ASIGNADAS
    limpiar_clausulas(clausula)
    
    #SE CREA UN ARREGLO DE LAS VARIABLES NO ASIGNADAS

    no_asignados = []
    for k in mapeo_boolean.keys():
        no_asignados = no_asignados+get_nones(k)
        
    # AGRUPACION DE CLAUSULAS POR VARIABLE NO ASIGNADA
    agrupacion = clausule_association(no_asignados,clausula)
    print(no_asignados)
    #print(len(no_asignados))
    print("")
    print(mapeo_boolean)
    print("")
    sol = SAT2(no_asignados,agrupacion)
###########################################################    
    
if __name__ == "__main__":
    main()

