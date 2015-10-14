import matplotlib.pyplot as plt

def deucli(h1,h2):          #Funcion que retorna la distancia euclidiana entre 2 parrafos
    # Diccionarios = { Palabras: frecuencia en el parrafo}
    sumatoria=0
    for palabra in h1:      
        for palabra2 in h2:         
            if palabra == palabra2:
                sumatoria+= (h1[palabra] - h2[palabra2])**2
    sumatoria = (sumatoria)**0.5
    return sumatoria

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

def matriztexto():          #Esta funcion cuenta la cantidad de parrafos que hay en archivo y retorna una matriz vacia de parrafos x parrafos
    arch= open(archivo + ".txt")
    count=0
    matriz=[]
    for linea in arch:
        if linea.strip().split() == []:
            continue
        count+=1
    for i in range(count):
        matriz.append([])
        for j in range(count):
            matriz[i].append(0.0)     
    return matriz

def matrizfinal(matriz):            #Esta funcion copia la parte triangular superior de una matriz a su parte triangular inferior
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[j][i] = matriz[i][j]

def graficar(distancias):
    plt.hist(distancias,(max(distancias) - min(distancias))*100,(min(distancias),max(distancias)),color = "m")
    plt.ion()
    if distancias== lista_eucli:
        plt.title("Distancia Euclidiana")
    else:
        plt.title("Distancia Coseno")
    plt.xlabel("Distancias")
    plt.ylabel("Frecuencia de distancias")
    plt.savefig("grafico.png")

def LimitesPlagio(matriz):
    if matriz == matrizeu:
        print "Ingrese el intervalo en el que se encuentra el plagio a partir del grafico de Distancia Euclidiana \n"
    else:
        print "Ingrese el intervalo en el que se encuentra el plagio a partir del grafico de Distancia Coseno \n"
    menor = float(raw_input("Limite menor: "))
    mayor = float(raw_input("Limite mayor: "))
    print "--------------------------------------------------------------------------------------------------------------------"
    plagio = []                                  #Lista que contendra una tupla con los parrafos que contendrian plagio
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j]>= menor and matriz[i][j]<= mayor:  #Buscamos los parrafos que se encuentran en el rango indicado.
                plagio.append((i+1,j+1))
                for parrafo in plagio:
                    a,b=parrafo
                    for parrafo2 in plagio:
                        c,d=parrafo2
                        if a == d and b==c:
                           del plagio[plagio.index((c,d))]  #Eliminamos los pares de parrafos repetidos.
                   
    for x in plagio:
        par1, par2 =x
        print "-El parrafo " + str(par1) + " con el parrafo " + str(par2) +" pareciera ser plagio. \n"
    plt.close()


while True:
    try:
        archivo = raw_input("Ingrese el nombre del archivo (sin extension):  ")
        arch = open(archivo + ".txt")    #Leo el archivo
        break
    except:
        print("No se ha encontrado el archivo, intente nuevamente.")
print "--------------------------------------------------------------------------------------------------------------------"
lista_eucli= []                              #Lista que almacenara las distancias euclidianas            
lista_cos= []                                #Lista que almacenara las distancias coseno                       
nparrafo=0                                        #Variable que maneja el numero de parrafo en el cual estoy, del documento que estoy leyendo.
matrizeu = matriztexto()                 #matriz  de distancia  euclidiana ntotalparrafos x ntotalparrafos
matrizcos = matriztexto()               #matriz de distancia coseno ntotalparrafos x ntotalparrafos
for linea in arch:
    if linea.strip().split()== []:                       
        continue
    nparrafo+=1
    arch2 = open(archivo + ".txt")   #Abro el archivo en otra variable para ir comparandolo
    nparrafo2=0                                 #Variable que maneja el numero de linea que leo del documento 2  que estoy leyendo.
    nparrafosvacios = 0
    for i,linea2 in enumerate(arch2):        #Funcion que enumera el texto por cada linea (enumeracion, linea)
        if linea2.strip().split()== []:
            nparrafosvacios+=1
            continue
        if i+1<=nparrafo+nparrafosvacios:           
            nparrafo2+=1
            continue
        nparrafo2+=1
        h1 = {}
        h2=  {}
        parrafo1= linea.translate(None, ".,:-!@'#()$").lower().strip().split()               #Quitamos caracteres especiales
        parrafo2= linea2.translate(None, ".,:-!@'()#$").lower().strip().split()  #Quitamos caracteres especiales          
        voca= set(parrafo1)| set(parrafo2)                                         #Se hacen conjunto las dos listas y se unen para generar un vocabulario general de las palabras
        for palabra in parrafo1:
            if palabra not in h1:
                h1[palabra]=0.0
            h1[palabra]+=1/float(len(parrafo1))       #Se normaliza
        for palabra in voca:
            if palabra not in h1:
                h1[palabra]=0.0
        for palabra in parrafo2:
            if palabra not in h2:
                h2[palabra]=0.0
            h2[palabra]+=1/float(len(parrafo2))           #Se normaliza
        for palabra in voca:
            if palabra not in h2:
                h2[palabra]=0.0
        matrizeu[nparrafo-1][nparrafo2-1]= round(deucli(h1,h2),2)
        matrizfinal(matrizeu)
        matrizcos[nparrafo-1][nparrafo2-1]= round(abs(dcos(h1,h2)),2)
        matrizfinal(matrizcos)     
        lista_eucli.append(round(deucli(h1,h2),2))
        lista_cos.append(round(dcos(h1,h2),2))
        
    arch2.close()
arch.close()

#Para mostrar matrices
#for x in matrizeu:
 #  print x
#for x in matrizcos:
#    print x

print "Con que distancia desea calcular: \n"
print " (1) Distancia Euclidiana"
print " (2) Distancia Coseno \n"

while True:
    try:
        dato = int(raw_input("Ingrese (1) o (2):  "))
        if dato== 1 or dato==2:
            break
        else:
            print "No ha ingresado un dato correcto."
    except:
            print "No ha ingresado un dato correcto."
print "--------------------------------------------------------------------------------------------------------------------"
if dato ==1:
    graficar(lista_eucli)
    LimitesPlagio(matrizeu)
if dato ==2:
    graficar(lista_cos)
    LimitesPlagio(matrizcos)
raw_input("Presione Enter para salir...")
