

def varToProp(var,n):
    global ALPHABET
    var=int(var)
    #print("mi n="+str(n))
    #print(n**2)
    row = (var/(n**2))
    if var%(n**2)==0 and row!=0:
        row = row -1
    row = str(row)
    row = int(row[0])
    #print("Mi init var="+str(var))
    #print("Mi row="+str(row))
    var = var - row*(n**2)
    #print("Mi var - row="+str(var))
    column = (var/n)
    if var%(n)==0 and column!=0:
        column = column -1
    column = str(column)
    column = int(column[0])
    #print("Mi column="+str(column))
    var = var - column*n
    #print("Mi var - column="+str(var))
    digit=ALPHABET[:n][var-1]
    #print(digit,var)
    #return var
    return "p("+str(digit)+", "+str(row)+", "+str(column)+")"


ALPHABET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","."]

def main():
    #MAIN
    global ALPHABET
    inputfile = open ('output.txt','r')
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
                n=str(n)
                n=int(n[0])
            elif line[0] == "c":
                output = output + "\n\n"+ line + "\n"
            else:
                #print(line[0])
                token = line.split(" ")
                #print(token)
                for tok in token:
                    tok.strip()
                    if len(tok)>0:
                        if tok[0]=="-":
                            output = output + "-" +str(varToProp(tok[1:],n))+ " "
                        elif tok[0]=="0":
                            output = output + " ^ "
                        else:
                            #print("Sot tok[0]"+ str(tok[0]))
                            output = output + str(varToProp(tok,n))+ " "
            output = output + "\n"
    print(output)

if __name__ == "__main__":
    main()