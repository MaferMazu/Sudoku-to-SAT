import re

def SAT(estados):
    cl = []
    state = [x for x in mapeo_boolean.values()]
    for e in estados:
        for i in range(len(e)):
            cl.append(re.split(" ",e[i]))
    #print(cl)
    #print(state)
    
    root = Nodo(state, cl)
    root.search_valid_state()
##############################################################
# ClASE Tree
##############################################################
class Tree:
    def __init__(self):
        self.raiz = None
        self.estado = []
#############################################################
# CLASE NODO
#############################################################
class Nodo:
    def __init__(self, state, clausula):
        self.estado=state
        self.clausula = clausula
        siguiente = None
        self.valido = False # Recorrido 
        
    def search_valid_state(self):
        try:
            
            p = self.estado.index(None)
            print(p)
            new_state = self.estado
            print(new_state)
            new_state[0] = False
            
            self.siguiente.append(Nodo(new_state,self.clausula))
            
            print(len(self.siguiente))
            new_state2[p] = True
            print(new_state2)
            self.siguiente.append(Nodo(new_state2,self.clausula))
            
            for c in(self.siguiente):
                c.search_valid_state()
        except:
            #for c in self.clausula:
            print("")
    
    def compare(self):
        b = True
        for x in self.clausula:
            a = False
            for l in range(len(x)):
                # compara con False
                v = int(x[l])
                if (v<0):
                    boolean = mapeo_boolean[str(-1*v)]
                    a = a or boolean
            b = b and a
        print("el valor de b es: ", end=" ")
        print(b)
                
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

#####################################################    
def getEmptyMatrix(n):
    main_matrix = []
    for i in range(n):
        main_matrix.append([])
    return main_matrix
#####################################################    
def to_n(n,value,nivel):
    v = []
    for i in range(n):
        if (i!=value):
            node = Nodo(i,nivel)
            v.append(node)
    return v
###########################################

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
    for j in fijos:
        val = mapeo_valor[str(j)]
        if(j>3):
            for k in range(j-val+1,j-val+(n**2)+1,1):
                diccionario[str(k)]= False
        else:
            for k in range(1+n**2):
                diccionario[str(k)]= False
        diccionario[str(j)]= True
        for i in get_columns(str(j),n):
            if(int(i)!=j):
                diccionario[i] = False
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
    return file_array, n, dimension
#########################################################
def main():
    #MAIN
    global mapeo_posicion  # Numero
    global mapeo_valor # Celda
    global mapeo_column  # Numero
    global mapeo_boolean # Valor Booleano Asignado
    archivo = open("cnf.txt", "r")
    file_array = archivo.readlines()
    archivo.close()

    file_array, n, dimension = getTable(file_array)
    asignados = re.split(" 0 ", file_array[0])
    asignados.pop()
    fijos = [int(x) for x in asignados]
    
    mapeo_posicion = cells_association(n) # Numero
    mapeo_column = col_association(n) # Columna
    mapeo_valor = values_association(n)   # Celda
    mapeo_boolean = boolean_association(n,fijos) # Valor Booleano Asignado
    
    disj = []
    
    for linea in file_array:
        disjunciones = re.split(" 0 ", linea)
        disjunciones.pop()
        disj.append(disjunciones)
    
    #print(mapeo_boolean)
    sol = SAT(disj)
###########################################################    
    
if __name__ == "__main__":
    main()

#########################################################

