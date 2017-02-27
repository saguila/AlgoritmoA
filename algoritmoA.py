import Queue as q
from pqdict import PQDict as pq


class AlgoritmoA:
        def __init__(self,mapa,partida,objetivo,N,M):
            self.partida = Casilla(partida,0,celdaPunto(partida).Hfrom(celdaPunto(objetivo)))
            self.objetivo = objetivo
            self.M = int(M)
            self.N = int(N)
            self.l_abierta = pq
            self.l_abierta[partida] = self.partida  
            self.l_cerrada = []
            self.camino = []
        def celdaPunto(self,pos): #Para representar de forma bidimensional nuestro mapa.
            if pos == 0:
                return Punto(0,0)
            else:
                return Punto(pos % self.N,pos // self.N)

        def puntoCelda(self,punto):#Para pasar de la representacion bidimensional a la unidimensional.
            return int(((punto.y // self.N)*self.N) + (punto.x))
        
        def solucion(self):
            self.abierta[self.partida] = self.celdaPunto(self.partida).costeTotal(self.celdaPunto(self.objetivo),0) 
            self.popitem()
            #mirar arriba coste Mov 10
            if self.partida >= self.N && self.mapa[self.partida - self.N] != -1:
                coste = 10 + self.celdaPunto(self.partida - self.N).Hfrom()
            #mirar esquina superior derecha coste Mov 10
            if self.partida >= self.N && self.partida % self.N < (self.N - 1) && self.mapa[self.partida - (self.N - 1)] != -1:
                
            #mirar derecha costeMov
            if self.partida % self.N < (self.N - 1) && self.mapa[self.partida + 1] != -1:
                
            #mirar esquina inferior derecha coste Mov 14
            if self.partida < self.M * (self.N - 1) && self.partida % self.N < (self.N - 1) && self.mapa[self.partida + self.N + 1] != -1:
            #mirar abajo coste Mov 10
            if self.partida < self.M * (self.N - 1) && self.mapa[self.partida + self.N] != -1:
            #mirar esquina inferior izquierda coste mov 14
            if self.partida < self.M * (self.N - 1) && self.partida % self.N > 0 && self.mapa[self.partida + self.N - 1] != -1:
            #mirar izquierda coste mov 10
            if self.partida % self.N  > 0 && self.mapa[self.partida - 1] != -1:
            #mirar esquina superior izquierda coste Mov 14
            if self.partida >= self.N && self.partida % self.N  > 0 && self.mapa[self.partida - self.N - 1] != -1:
               
            self.cerrada.append(self.) 
class Casilla:
    def __init__(self,pos,coste=0,acumulado=0,padre=None):
        self.pos = int(pos)
        self.coste = int(coste)
        self.acumulado = int(acumulado)
        self.padre = padre
    def __lt__(self,casilla):
        return self.acumulado < casilla.acumulado
    def __repr__(self): #Como mostramos la informacion de nuestro punto.
        return 'Posicion -> ' + str(self.pos) + ' Coste -> ' + str(self.coste) + ' Padre -> ' + str(self.padre)

class Punto:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
    def Hfrom(self,punto): #Heuristica desde self hasta punto.
        return (abs(self.x - punto.x) + abs(self.y - punto.y)) * 10 #longitud de manhattan * 10
    def costeTotal(self,punto,costeAc): #Calculo de F(x)
        return self.Hfrom(punto,costeAc) + costeAc;
    def gradiente(self,punto):#Gradiente para ver a que direccion tengo que ir
        return Punto(punto.x - self.x,punto.y - self.y)
    def __lt__(self,punto): #Redefino el operador <
        return self  
    def __repr__(self): #Como mostramos la informacion de nuestro punto.
        return '( ' + str(self.x) + ' , ' + str(self.y) + ')'

            
mapa = [0,0,0,0,0,0,-1,0,0,-1,-1,0,0,0,0,0]
posPartida = Punto(0,1)
posObjetivo = Punto(0,4)
a = AlgoritmoA(mapa,posPartida,posObjetivo,4,4)
a.puntoCelda(posPartida)