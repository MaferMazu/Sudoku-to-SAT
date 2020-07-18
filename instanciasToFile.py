filepath='InstanciasSudoku.txt'
inputfile = open (filepath,'r')
lines = inputfile.readlines()
n=1
for line in lines:
    if len(line)>2:
        outputfile = open('instanciasSudoku/input'+str(n)+'.txt',"w+")
        outputfile.write(line)
        outputfile.close()
        n=n+1
inputfile.close()