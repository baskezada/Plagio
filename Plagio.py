import matplotlib.pyplot as plt
from numpy import *         #Se importa numpy para poder fabricar la matriz

def deucli(h1,h2):          #Funcion que retorna la distancia euclidiana entre 2 parrafos
    suma=0
    for palabra in h1:      
        for palabra2 in h2:         
            if palabra == palabra2:
                suma+= (h1[palabra] - h2[palabra2])**2
    sumafinal = (suma)**0.5
    return sumafinal

def dcos(h1,h2):            #Funcion que retorna la distancia coseno entre 2 parrafos
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

def matriztexto():          #Esta funcion cuenta la cantidad de parrafos que hay en archivo y retorna una matriz de parrafos x parrafos
    arch = open(archivo + ".txt")
    count=0
    for linea in arch:
        if "\n" == linea:
            continue
        count+=1
    return [[i]*count for i in range(count)]

def matrizfinal(matriz):            #Esta funcion copia la parte triangular superior de una matriz a su parte triangular inferior
    for i in range(len(matriz)):
        for x in range(len(matriz[i])):
            matriz[x][i] = matriz[i][x]

archivo = raw_input("Ingrese el nombre del archivo (sin extension):  ")
arch = open(archivo + ".txt")    #Leo el archivo
lista_eucli= []                                          
lista_cos= []
nlinea=0                                        #Variable que maneja el numero de linea que leo del documento que estoy leyendo.
matrizeu = matriztexto()
matrizcos = matriztexto()
diccos={}
for linea in arch:
    arch2 = open(archivo + ".txt")   #Abro el archivo en otra variable para ir comparandolo
    nlinea2=0                                 #Variable que maneja el numero de linea que leo del documento 2  que estoy leyendo.
    if linea == "\n":                       
        continue
    if "\n" in linea:
        nlinea+=1
    for i,linea2 in enumerate(arch2):        #Funcion que enumera el texto por cada linea (enumeracion, linea)
        if linea2 == "\n":
            continue
        if i+1<=nlinea:                 
            nlinea2+=1
            continue
        if "\n" in linea2:
             nlinea2+=1
        h1 = {}
        h2=  {}
        parrafo1= linea.translate(None, '.,:-!@#$').lower().strip().split()               #Quitamos caracteres especiales
        parrafo2= linea2.translate(None, '.,:-!@#$').lower().strip().split()            #Quitamos caracteres especiales          
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
        matrizcos[nlinea-1][nlinea2-1]= round(abs(dcos(h1,h2)),2)
        matrizfinal(matrizcos)
        matrizcos= array(matrizcos)
        if nlinea == nlinea2:                                           #Para no agregar las distancias de parrafos iguales a las listas
            continue
        lista_eucli.append(round(deucli(h1,h2),2))
        lista_cos.append(round(dcos(h1,h2),2))
        
    arch2.close()
arch.close()


#print matrizeu
#print matrizcos

#Creamos el grafico con la distancia euclidiana.
min1 = min(lista_eucli)
max1 = max(lista_eucli)
plt.hist(lista_eucli,(max1 - min1)*100,(min1,max1),color = "m")
plt.ion() 
plt.title("Distancia euclidiana")
plt.xlabel("distancias")
plt.ylabel("frecuencia de distancias")
plt.savefig("grafico_euclides.png")

#Pedimos el rango de distancia en el que se encuentra el plagio analizando los graficos.
print "ingrese el intervalo en el que se encuentra el plagio a partir del grafico de distancia euclidiana \n"
menor1 = float(raw_input("Limite menor: "))
mayor1 = float(raw_input("Limite mayor: "))
print "\n"
plagio_euc = []                                  #Lista que contendrá los parrafos que presentan posibles plagios.
for a in range(len(matrizeu)):
    for x in range(len(matrizeu[a])):
        if matrizeu[a][x]>= menor1 and matrizeu[a][x]<= mayor1:  #Buscamos los parrafos que se encuentran en el rango indicado.
            plagio_euc.append((a+1,x+1))
            for parrafo in plagio_euc:
                e,b=parrafo
                for parrafo2 in plagio_euc:
                    c,d=parrafo2
                    if e == d and b==c:
                       del plagio_euc[plagio_euc.index((c,d))]  #Eliminamos los pares de parrafos repetidos.
               
for x in plagio_euc:
    par1, par2 =x
    print "-El parrafo " + str(par1) + " con el parrafo " + str(par2) +" pareciera ser plagio. \n"
plt.close()


#Creamos el grafico con la distancia coseno.
min2 = min(lista_cos)
max2 = max(lista_cos)
plt.ion() 
plt.hist(lista_cos,(max1 - min1)*100,(min2,max2),color = "c")
plt.title("Distancia coseno")
plt.xlabel("distancias")
plt.ylabel("frecuencia de distancias")
plt.savefig("grafico_coseno.png")


    
print "ingrese el intervalo en el que se encuentra el plagio a partir del grafico de distancia coseno. \n"
menor2 = float(raw_input("Limite menor: "))
mayor2 = float(raw_input("Limite mayor: "))
print "\n"
plagio_cos = []                                  #Lista que contendrá los parrafos que presentan posibles plagios.
for a in range(len(matrizcos)):
    for x in range(len(matrizcos[a])):
        if matrizcos[a][x]>= menor2 and matrizcos[a][x]<= mayor2:  #Buscamos los parrafos que se encuentran en el rango indicado.
            plagio_cos.append((a+1,x+1))
            for parrafo in plagio_cos:
                e,b=parrafo
                for parrafo2 in plagio_cos:
                    c,d=parrafo2
                    if e == d and b==c:
                       del plagio_cos[plagio_cos.index((c,d))]   #Eliminamos los pares de parrafos repetidos.

for x in plagio_cos:
    par1, par2 = x
    print "-El parrafo " + str(par1) + " con el parrafo " + str(par2) +" pareciera ser plagio. \n"
plt.close()
