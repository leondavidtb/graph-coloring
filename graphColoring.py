# INSTRUÇÕES DE EXECUÇÃO
# 1. A pasta "glucose-syrup-4.1" deve estar na mesma pasta em que o arquivo .py.
#   1.1 Execute o comando "sudo apt install zlib1g-dev".
#   1.2 Execute o comando make dentro da pasta glucose-syrup-4.1/parallel.
# 2. A pasta "instancias" também deve estar na mesma pasta em que o arquivo .py.
# 3. Execute o comando "python3 graphColoring.py".
#   3.1 O arquivo "output.cnf" será gerado dentro da pasta "parallel" do glucose.
#   3.2 O arquivo resultante do glucose também será gerado dentro da mesma pasta.

# IMPORTANDO BIBLIOTECAS
import numpy as np
import time as tm
import os

# LER O DATASET E DEFINIR O NUMERO DE LINHAS
def readDataSet():
    with open(dataset) as fp:  
        line = fp.readline()

        while line:
            if line.startswith("p"):
                a, b, c, d = line.split(" ")
                return int(c)
                
            line = fp.readline()
    fp.close()

# DEFINIÇÕES DO DATASET E NUMERO DE CORES
dataset = "instancias/myciel3.col"
glucose = "glucose-syrup-4.1/parallel/./glucose-syrup -model glucose-syrup-4.1/parallel/output.cnf > glucose-syrup-4.1/parallel/result.txt"
numRows = readDataSet()
numColors = 4

# CRIAÇÃO DA MATRIZ [LINHAS|CORES]
matrixValues = []

for i in range(numRows * numColors):
    matrixValues.append(i + 1)

matrix = np.array(matrixValues).reshape(numRows, numColors)

# ESCREVER O .CNF COM BASE NA QUANTIDADE DE LINHAS E CLAUSULAS
def writeOutput(numRows, numColors, clauseList):
    terms = numRows * numColors
    count = 0
    # countClause = 0
    
    f = open("glucose-syrup-4.1/parallel/output.cnf", "w+")
    
    f.write("p cnf %s %s\n" % (terms, int((len(clauseList)/2) + numRows)))
    
    for i in range (numRows):
        for j in range (numColors):
            f.write("%s " % matrix[i][j])
        f.write("0")
        f.write("\n")
        # countClause += 1
    
    for k in range (len(clauseList)):
        count += 1
        f.write("-%s " % clauseList[k])
        
        if count == 2:
            f.write("0\n")
            count = 0
            # countClause += 1
    f.close()    

# GERA UMA LISTA COM TODAS AS CLÁSULAS
def getCNF(numRows):
    x = 0
    y = 0
    clauseList = []
    with open(dataset) as fp:  
        line = fp.readline()
        
        while line:
                for i in range (numRows):
                        for j in range (numColors):
                            if line.startswith("e "):
                                a, b, c = line.split(" ")
                                x = matrix[int(b)-1][j]
                                y = matrix[int(c)-1][j]
                                clauseList.append(x)
                                clauseList.append(y)
                                
                        break
                line = fp.readline()
                
    return clauseList

# CHECAR SATISFAZIBILIDADE
def checkSatUnsat():
    with open("glucose-syrup-4.1/parallel/result.txt") as f:
        line = f.readline()

        while line:
            if line.startswith("s"):
                a, b = line.split(" ")
                if b == "SATISFIABLE\n":
                    print("SATISFAZÍVEL")
                    print(f.readline())
                    break
                else:
                    print("INSATISFAZÍVEL")
            line = f.readline()
    f.close()
                

# FUNÇÃO MAIN
def main():
    start_time = tm.time()
    #readDataSet()
    writeOutput(numRows, numColors, getCNF(numRows))
    os.system(glucose)
    checkSatUnsat()
    end_time = tm.time()

    print("Tempo de Execução: %f" % (end_time - start_time))

main()
