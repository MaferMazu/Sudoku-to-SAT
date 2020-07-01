import re

def new_true(estado, n):
    estado[n] = True
    return estado

def new_false(estado, n):
    estado[n] = False
    return estado

def SAT(clausulas):
    estado = [x for x in mapeo_boolean.values()]  
    #print(clausulas)
    print(estado)
    #root = Nodo(estado,clausulas)
    #root = Nodo(estado,clausulas)
    #root.search_valid_state()

#############################################################
# CLASE NODO
#############################################################
class Nodo:
    def __init__(self, state, clausula):
        self.estado=state
        self.clausula = clausula
        self.siguiente = []
        
    
    def search_valid_state(self):
        if (self.tiene_None()):
            # Inicializo las nuevas Ramas
            p = self.estado.index(None)

            s1 = self.estado.copy()
            s2 = self.estado.copy()
            #print(self.estado)
            print("++++++++++++++++++++++++++++++++++++++++++++")
            rama_true = Nodo(new_true(s1, p),self.clausula)
            rama_false = Nodo(new_false(s2, p),self.clausula)
            
            self.siguiente.append(rama_true)
            self.siguiente.append(rama_false)
            
            # Busco en cada una de las Ramas
            sol = []
            for i in self.siguiente:
                i.search_valid_state()
        else:                  
            self.verify_clausule()
    
        
    def verify_clausule(self):
        sol = True
        for c in self.clausula:
            eval_true = False
            for v in c:
                #print("value:", end=" ")
                #print(v)
                #print(self.estado[abs(v)-1])
                if(v<0):
                    eval_true = eval_true or (not self.estado[abs(v)-1])
                else:
                    eval_true = eval_true or (self.estado[abs(v)-1])
            if(not eval_true):
                #print(self.estado)
                #print(c, end=" ")
                #print(v)
                sol = False
                break
        
        if(sol):
            print("##################################")
            print("UNA SOLUCION ES:")
            print(self.estado)
            print("##################################")
        
        
    def tiene_None(self):
        existe_none = False
        for e in self.estado:
            if(e == None):
                existe_none = True
                break
        return existe_none
                
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
        #print(p)
        clausulas[i] = p
    return clausulas
#                posicion.append(i)
#        var_clausule_position.append(posicion)
#    print(var_clausule_position)
        
        
#########################################################
def main():
    #MAIN
    global mapeo_posicion  # Numero
    global mapeo_valor # Celda
    global mapeo_column  # columna
    global mapeo_fila  # fila
    global mapeo_boolean # Valor Booleano Asignado
    archivo = open("cnf.txt", "r")
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
    print("Posicion")
    print(mapeo_posicion)
    print("")
    print("Valor")
    print(mapeo_valor)
    print("")
    print("Columna")
    print(mapeo_column)
    print("")
    print("Fila")
    print(mapeo_fila)
    print("")
    print("Estado Inicial Booleanos")
    print(mapeo_boolean)
    print("")
    
    disj = []
    
    for linea in file_array:
        disjunciones = re.split(" 0 ", linea)
        disjunciones.pop()
        disj.append(disjunciones)
###########################################################
    clausula = []
    for e in disj:
        for i in range(len(e)):
            clausula.append(re.split(" ",e[i]))            
    int_clausulas = get_clausules(clausula, len(clausula))
    
#    sol = SAT(int_clausulas)
###########################################################    
    
if __name__ == "__main__":
    main()

#########################################################

