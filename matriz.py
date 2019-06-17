#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import random
from celda import Celda

class Matriz:
    def __init__(self):
        self.__tamanio= None;
        self.__altura = None;
        self.__window = None
        self.__tam = 0
        self.__palabras = []
        self.__tamano_real = 0
        self.__dic = dict()

    def __tamaño_mayor(self):
        '''
            Me devuelve la longitud de la palabra mas larga para ajustar la matriz
        '''
        alto=0
        for i in self.__palabras:
            if(len(i)>alto):
                alto=len(i)
        return alto

    def get_tamaño(self):
        self.__tam = self.__tamaño_mayor() + 4 #El tamaño de la palabra + 4 lugares más
        if(len(self.__palabras) > 8): #Si la longitud de la palabra es mas de 8, el tamaño es el de la cantidad de palabras
            self.__tamano_real = len(self.__palabras)
        else:
            #Sino, es la cantidad de palabras + 1
            self.__tamano_real = len(self.__palabras) + 1
        self.__altura = self.__tamano_real * 25
        self.__tamanio = self.__tam * 25
        return (self.__tamanio,self.__altura)

    def set_palabras(self,palabras):
        self.__palabras = palabras

    def __elegir_fila(self,filas_elegidas):
        '''
            Elige una fila/columna donde puede ubicarse
        '''
        filasElegir = random.randint(0,self.__tamano_real-1)#La fila es entre 0 y el tamanño real definido previamente pero -1
        while(filasElegir in filas_elegidas):
            filasElegir = random.randint(0,self.__tamano_real-1)
        filas_elegidas.append(filasElegir)
        return filasElegir

    def __distribuir_palabras(self):
        '''
            Metodo que distribuye las palabras en la matriz y rellena los espacios libres con letras al azar
        '''
        matriz = []
        for i in range(self.__tamano_real):
            ##Crea las filas de la matriz
            lista = []
            matriz.append(lista) # [[] [] [] [] [] [] []]
        filas_elegidas = []
        for fila in range(len(self.__palabras)):
            filasElegir = self.__elegir_fila(filas_elegidas)
            columna = random.randint(0,self.__tam - len(self.__palabras[fila]))
            for j in range(0,(columna)):
                #este for completa con palabras al azar hasta la primera posicion donde arranca la palabra que corresponde
                letra_azar = chr(random.randint(97,122))
                matriz[filasElegir].append(letra_azar)
            for j in range(0,len(self.__palabras[fila])):
                #esto for ingresa las letras de la palabra la ual estamos analizando en i
                matriz[filasElegir].append(self.__palabras[fila][j])
            for j in range((columna + len(self.__palabras[fila])),self.__tam):
                #Desde la ultima posicion en que está la ultima letra de la palabra + 1 completa con letras al azar hasta el tamaño de la grilla
                letra_azar = chr(random.randint(97,122))
                matriz[filasElegir].append(letra_azar)
        for fila in range(len(self.__palabras),(self.__tamano_real)):##LLENA LAS FILAS QUE QUEDARON DE LA MATRIZ
            filasElegir = self.__elegir_fila(filas_elegidas)
            for i in range(self.__tam):
                matriz[filasElegir].append(chr(random.randint(97,122)))
        return matriz

    def __crear_grilla_horizontal(self,graph,mayus):
        matriz = self.__distribuir_palabras()
        print(matriz)
        '''
         Distribuye las palabras por la grilla. METODO PRIVADO
        '''
        dic = dict()
        dicAux = dict()
        y1 = 0
        y2 = 25
        for z in range(len(matriz)):    #cantidad de filas de la matriz
            _x1 = 0
            x2 = 25
            for n in range(len(matriz[z])):     #cantidad de columnas
                pos_sup = (_x1,y1)
                pos_inf = (x2,y2)
                cell = Celda()
                cell.set_coordenada_sup(pos_sup)
                cell.set_coordenada_inf(pos_inf)
                if(mayus == 'Mayuscula'):
                    cell.set_letra(matriz[z][n].upper())
                else:
                    cell.set_letra(matriz[z][n].lower())
                cell.draw_cell(graph)
                self.__dic[(z,n)] = cell
                _x1+=25
                x2+=25
            y1+=25
            y2+=25

    def __crear_grilla_vertical(self,graph,mayus):
        matriz = self.__distribuir_palabras()
        print(matriz)
        '''
         Distribuye las palabras por la grilla. METODO PRIVADO
        '''
        dic = dict()
        _x1 = 0
        x2 = 25
        for z in range(len(matriz)):    #cantidad de filas de la matriz
            y1 = 0
            y2 = 25
            for n in range(len(matriz[z])):     #cantidad de columnas
                pos_sup = (_x1,y1)
                pos_inf = (x2,y2)
                cell = Celda()
                cell.set_coordenada_sup(pos_sup)
                cell.set_coordenada_inf(pos_inf)
                if(mayus == 'Mayuscula'):
                    cell.set_letra(matriz[z][n].upper())
                else:
                    cell.set_letra(matriz[z][n].lower())
                cell.draw_cell(graph)
                self.__dic[(n,z)] = cell
                y1+=25
                y2+=25
            _x1+=25
            x2+=25

    def mostrar_matriz_vertical(self,graph,mayus):
        '''
            MUESTRA LA GRILLA POR PANTALLA VERTICALMENTE
        '''
        self.__crear_grilla_vertical(graph,mayus)
        return self.__dic
        ##Actualiza la pantalla
    def mostrar_matriz_horizontal(self,graph,mayus):
        '''
            MUESTRA LA GRILLA POR PANTALLA VERTICALMENTE
        '''
        self.__crear_grilla_horizontal(graph,mayus)
        return self.__dic

    def cambiar(self,pos,graph,color = 'red'):
        celda = self.__dic[(pos[0],pos[1])]
        ok=celda.set_color(color)
        celda.draw_cell(graph)
        return ok
