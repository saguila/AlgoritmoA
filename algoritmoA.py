class AlgoritmoA:
        def __init__(self,mapa,partida,objetivo,N,M):
            self.partida = partida
            self.objetivo = objetivo
            self.M = int(M)
            self.N = int(N)
            self.l_abierta = []
            self.l_cerrada = []
        def celdaPunto(self,pos): #Para representar de forma bidimensional nuestro mapa.
            if pos == 0:
                return Punto(0,0)
            else:
                return Punto(pos % self.N,pos // self.N)

        def puntoCelda(self,punto):#Para pasar de la representacion bidimensional a la unidimensional.
            return int(((punto.y // self.N)*self.N) + (self.N - punto.x))
class Punto:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
    def Hfrom(self,punto): #Heuristica desde self hasta punto.
        return (abs(self.x - punto.x) + abs(self.y - punto.y)) * 10 #longitud de manhattan * 10
    def gradiente(self,punto):#Gradiente para ver a que direccion tengo que ir
        return Punto(punto.x - self.x,punto.y - self.y)
    def __repr__(self): #Como mostramos la informacion de nuestro punto.
        return '( ' + str(self.x) + ' , ' + str(self.y) + ')' 

            
mapa = [0,0,0,0,0,0,-1,0,0,-1,-1,0,0,0,0,0]
posPartida = Punto(0,1)
posObjetivo = Punto(0,4)
a = AlgoritmoA(mapa,posPartida,posObjetivo,4,4)
a.puntoCelda(posPartida)