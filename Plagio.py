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

arch = open("texto.txt")
lista= []
lista2= []
nlinea=1
for linea in arch:
    arch2 = open("texto.txt")
    for i,linea2 in enumerate(arch2):
        if i<nlinea:
            continue
        h1 = {}
        h2=  {}
        parrafo1= linea.translate(None, '.,:-!@#$').lower().strip().split()
        parrafo2= linea2.translate(None, '.,:-!@#$').lower().strip().split()
        if parrafo1 == [] or parrafo2 == []:
            continue
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
        lista.append(round(deucli(h1,h2),2))
        lista2.append(round(dcos(h1,h2),2))
    arch2.close()
    nlinea+=1
                
print lista, lista2        
arch.close()
