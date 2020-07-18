from sys import argv
def varToProp(var,n):
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
    return "p("+str(digit)+", "+str(row)+", "+str(column)+")"


ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]

def main():
    #MAIN
    global ALPHABET
    filepath = 'outputs/outputSudokuToSat.txt'
    if len(argv) > 1:
        filepath = argv[1]
    inputfile = open (filepath,'r')
    lines = inputfile.readlines()
    output = ""
    n=0
    for line in lines:
        line=line.rstrip("\n")
        if len(line)>0:
            if line[0] == "p":
                token = line.split(" ")
                ##print("Mi cantidad de vars es="+str(token[2]))
                n = int(token[2])
                n = n**(1./3.)
                n=int(n)
                #n=int(n[0])
            elif line[0] == "c":
                output = output + line
            else:
                #print(line[0])
                token = line.split(" ")
                #print(token)
                for tok in token:
                    tok.strip()
                    if len(tok)>0:
                        if tok[0]=="-":
                            output = output + "-" +str(varToProp(tok[1:],n+1))+ " "
                        elif tok[0]=="0":
                            output = output + " ^ "
                        else:
                            #print("Sot tok[0]"+ str(tok[0]))
                            output = output + str(varToProp(tok,n+1))+ " "
            output = output + "\n"
    print(output)

if __name__ == "__main__":
    main()