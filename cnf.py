import re

def new_true(estado, n):
    estado[str(n)] = True
    return estado

def new_false(estado, n):
    estado[str(n)] = False
    return estado

###########################################                
def new_list(suc,nivel,pos):
    v = []
    cont = 0
    for i in suc:
        if (cont != pos):
            node = Nodo(i.current_value,nivel)
            v.append(node)
        cont=cont+1
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
#########################################
# 
def SAT(clausulas, estados): 
    root = Nodo(clausulas,estados)
    root.search_valid_state()

#############################################################
# CLASE NODO
#############################################################
class Nodo:
    def __init__(self, clausula, estados):
        self.estados=estados
        self.clausula = clausula
        
    def tiene_None(self, estado):
        existe_none = False
        est = 0
        #print(estado)
        for e in estado.keys():
            if(estado[e] == None):
                existe_none = True
                est = e
                break
        return est, existe_none
    
    def search_valid_state(self):
        solucion = []
        sol = []
        #INICIALIZAMOS LA BUSQUEDA CON EL PRIMER CONJUNTO
        # DE CLAUSULAS
#        for i in range(len(self.clausula)):
#        print(self.estados[0])
        pos, existe = self.tiene_None(self.estados[0])
        if (existe):
            # Inicializo las nuevas Ramas
            s1 = self.estados[0].copy()
            #print(s1)
            s2 = self.estados[0].copy()
            #print("++++++++++++++++++++++++++++++++++++++++++++")
            rama_true = Nodo(self.clausula[0],new_true(s1, pos))
            rama_false = Nodo(self.clausula[0],new_false(s2, pos))
            
            sol.append(busqueda(rama_true))
            solucion.append(sol)
            print("SOLUCION PRIMERA CLAUSULA")
            print(sol)
            print(len(solucion))
                
def busqueda(bloque):
   
    key, existe = bloque.tiene_None(bloque.estados)
    sol = []
    if (existe):
        s1 = bloque.estados.copy()
        rama_true = Nodo(bloque.clausula,new_true(s1, key))
        sol.append(busqueda(rama_true))
        s2 = bloque.estados.copy()
        rama_false = Nodo(bloque.clausula,new_false(s1, key))
        sol.append(busqueda(rama_false)) 
    else:
        aux = False
        
        for c in bloque.clausula:
            #print (c)
            for elem in c:
                #print(elem)
                if (elem < 0):
                    #rint("negativo")
                    aux = aux or (not bloque.estados[str(elem)])
                else:
                    #print("positivo")
                    #print(bloque.estados[str(elem)])
                    aux = aux or bloque.estados[str(elem)]
        print(aux)
        if(aux):
            print(bloque.estados)
            return bloque.estados
        else:
            return

#########################################################
def main():
    #MAIN
    global mapeo_posicion  # Numero
    global mapeo_valor # Celda
    global mapeo_column  # columna
    global mapeo_fila  # fila
    global mapeo_boolean # Valor Booleano Asignado
    archivo = open("output.txt", "r")
    file_array = archivo.readlines()
    archivo.close()

    file_array, n, dimension, n_clausulas = getTable(file_array)
    asignados = re.split(" 0 ", file_array[0])
    asignados.pop()
    fijos = [int(x) for x in asignados]
    
    mapeo_posicion = cells_association(n) # Numero
    mapeo_column = col_association(n) # Columna
    mapeo_fila = row_association(n)   # Fila
    mapeo_valor = values_association(n)   # Celda

    mapeo_boolean = boolean_association(n,fijos) # Valor Booleano Asignado

    disj = []
    count = 1
    unit_clausules = [[] for j in range(n**4)]
    
    for linea in file_array:

        disjunciones = re.split(" 0 ", linea)
        disjunciones.pop()
        disj.append(disjunciones)

    firstCicle=True
    for linea in file_array[1:]:

        if firstCicle and count > n**4:
            firstCicle = False
        rest = count%(n**4)
        disjunciones = re.split(" 0 ", linea)
        disjunciones.pop()
        if not firstCicle:
            if rest ==0:
                unit_clausules[(n**4)-1] = unit_clausules[(n**4)-1] + disjunciones
            else:
                unit_clausules[rest-1]=unit_clausules[rest-1]+disjunciones
        else:
            if rest == 0:
                unit_clausules[(n**4)-1]=disjunciones
            else:
                  unit_clausules[rest-1]=disjunciones
        count = count + 1

    
        
###########################################################
    # SE AGRUPAN LAS CLAUSULAS EN GRUPOS RESPECTIVOS A
    #CLAUSULA POR CELDAS
    clausula = []
    for e in unit_clausules:
        group = []
        for i in range(len(e)):
            group.append(re.split(" ",e[i]))
            group = get_clausules(group, len(group))
        clausula.append(group)
            
    # SE OBTIENE LOS ESTADOS DE CASA SUBCLAUSULA     
    estados = []
    for e in clausula:
        cl = {}
        for x in e:
            for j in x:
                cl[str(abs(j))] = mapeo_boolean[str(abs(j))]
        estados.append(cl)
    
    sol = SAT(clausula, estados)
###########################################################    
    
if __name__ == "__main__":
    main()



