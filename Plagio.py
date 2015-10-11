
from numpy import *         #Se importa numpy para poder fabricar la matriz

def deucli(h1,h2):
    suma=0
    for palabra in h1:
        for palabra2 in h2:
            if palabra == palabra2:
                suma+= (h1[palabra] - h2[palabra2])**2
    sumafinal = (suma)**0.5
    return sumafinal

def dcos(h1,h2):
    suma=0
    x = {}
    y = {}
    for palabra in h1:
        x[palabra] = 0.0
        for palabra2 in h2:
            y[palabra2] = 0.0
            if palabra == palabra2:
                suma+= h1[palabra] * h2[palabra2]
    distancia = 1 - (suma/(deucli(h1,x)*deucli(h2,y)))
    return distancia

def matriztexto():
    arch = open("texto.txt")
    count=0
    for linea in arch:
        if "\n" == linea:
            continue
        count+=1
    return [[i]*count for i in range(count)]

def matrizfinal(matriz):
    for i in range(len(matriz)):
        for x in range(len(matriz[i])):
            matriz[x][i] = matriz[i][x]
            
arch = open("texto.txt")
lista= []
lista2= []
nlinea=1
matrizeu = matriztexto()
matrizcos = matriztexto()
diccos={}
for linea in arch:
    arch2 = open("texto.txt")
    nlinea2=1
    if linea == "\n":
        continue
    for i,linea2 in enumerate(arch2):
        if linea2 == "\n":
            continue
        if i<nlinea:
            nlinea2+=1
            continue
        h1 = {}
        h2=  {}
        parrafo1= linea.translate(None, '.,:-!@#$').lower().strip().split()
        parrafo2= linea2.translate(None, '.,:-!@#$').lower().strip().split()
        voca= set(parrafo1)| set(parrafo2)
        for palabra in parrafo1:
            if palabra not in h1:
                h1[palabra]=0.0
            h1[palabra]+=1/float(len(parrafo1))
        for palabra in voca:
            if palabra not in h1:
                h1[palabra]=0.0
        for palabra in parrafo2:
            if palabra not in h2:
                h2[palabra]=0.0
            h2[palabra]+=1/float(len(parrafo2))
        for palabra in voca:
            if palabra not in h2:
                h2[palabra]=0.0
        matrizeu[nlinea-1][nlinea2-1]= round(deucli(h1,h2),2)
        matrizfinal(matrizeu)
        matrizeu= array(matrizeu)
        matrizcos[nlinea-1][nlinea2-1]= round(dcos(h1,h2),2)
        matrizfinal(matrizcos)
        matrizcos= array(matrizcos)
        
        lista.append(round(deucli(h1,h2),2))
        lista2.append(round(dcos(h1,h2),2))
        nlinea2+=1
    arch2.close()
    nlinea+=1
                
arch.close()
print matrizeu
print matrizcos

#Pedimos el rango de distancia en el que se encuentra el plagio analizando los graficos.
print "ingrese el intervalo en el que se encuentra el plagio a partir del grafico de distancia euclidiana"
menor1 = float(raw_input("Limite menor: "))
mayor1 = float(raw_input("Limite mayor: "))
plagio_euc = []
for a in range(len(matrizeu)):
    for x in range(len(matrizeu[a])):
        if matrizeu[a][x]>= menor1 and matrizeu[a][x]<= mayor1:
            plagio_euc.append((a+1,x+1))
            for parrafo in plagio_euc:
                e,b=parrafo
                for parrafo2 in plagio_euc:
                    c,d=parrafo2
                    if e == d and b==c:
                       del plagio_euc[plagio_euc.index((c,d))]
               
for x in plagio_euc:
    par1, par2 =x
    print "El parrafo " + str(par1) + " con el parrafo " + str(par2) +" pareciera ser plagio."
    
print "ingrese el intervalo en el que se encuentra el plagio a partir del grafico de distancia coseno"
menor2 = float(raw_input("Limite menor: "))
mayor2 = float(raw_input("Limite mayor: "))
plagio_cos = []
for a in range(len(matrizcos)):
    for x in range(len(matrizcos[a])):
        if matrizcos[a][x]>= menor2 and matrizcos[a][x]<= mayor2:
            plagio_cos.append((a+1,x+1))
            for parrafo in plagio_cos:
                e,b=parrafo
                for parrafo2 in plagio_cos:
                    c,d=parrafo2
                    if e == d and b==c:
                       del plagio_cos[plagio_cos.index((c,d))]

for x in plagio_cos:
    par1, par2 = x
    print "El parrafo " + str(par1) + " con el parrafo " + str(par2) +" pareciera ser plagio."







    
