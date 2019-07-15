#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel


# -------------------------------------------------------------------------------------------------------------- #

                #Métodos para verificar si una palabra es o no válida.
def llenar_diccionario(ok1,dicGeneral,fila,columna,tipo):
    '''
        Distribuye las letras en el diccionario general que tiene Color:{fila:[columnas],fila[columnas]}
        este proceso va actualizando las letras que se seleccionan en la layout
    '''
    aux = 0
    if(ok1):
        if(tipo not in dicGeneral): #Si el color no está en el diccionario, lo pone como clave
            dicGeneral[tipo] = dict()
        if(fila not in dicGeneral[tipo]): #Si la fila seleccionado no está en el diccionario del color elegido, se agrega
            dicGeneral[tipo][fila] = list()
        elif(fila in dicGeneral[tipo])and(columna in dicGeneral[tipo][fila]):
            #Si la fila está ya seleccionada y la columna tambien, significa que elegió deseleccionarla
            aux = 1
            dicGeneral[tipo][fila].pop(dicGeneral[tipo][fila].index(columna))
        if(aux == 0): #aux == 0 cuando haya seleccionado por primera vez
            dicGeneral[tipo][fila].append(columna)

def verificar_diferencias(listaOrdenada):
    '''
        Verifica que la diferencia entre las letras no sea mayor a 1
    '''
    listaAuxiliar = list()
    pos = 0
    if(listaOrdenada != []): #Preguntamos si no está vacía porque pudo haber pasado que se hayan deseleccionador filas/columnas y quede una lista vacía
        for i in range(1,len(listaOrdenada)):
            if((listaOrdenada[i] - listaOrdenada[i-1] ) == 1):   #como arranca en 1  verifico el actual con el anterior
                listaAuxiliar.append(listaOrdenada[i-1])
                pos = i
            elif (listaAuxiliar != []):  #si la lista no esta vacia entonces la diferencia se produce al final por lo que las letras despues de esta no seran validas
                break
        listaAuxiliar.append(listaOrdenada[pos])   #agrega el ultimo que falta
    return listaAuxiliar

def verificar_grilla(dicGeneral,dic,dicTipoPalabra,orientacion,dicAux):
    '''
        Verifica si la palara es valida
        Recorre el dicionario de colores, elige cada palabra de cada color, concatena sus letras y verifica si es valida, comparando con dicTipoPalabra que es un diccionario con Llave color y valor lista de palabras seleccionadas para el color.
    '''
    palabrasAcertadas = []
    print('Diccionario General ',dicGeneral)
    for i in dicGeneral: #i es el color de tipo en hexadecimal sustantivo, adjetivo o verbo
        dicFilas = dicGeneral[i] #dicFilas es el diccionario con clave fila/columna y valor lista de filas/columnas elegidas
        for fila in dicFilas:
            listaColumnas = dicGeneral[i][fila] #Me quedo con las columnas elegidas de esa fila, o las filas de la columna.
            listaOrdenada = sorted(listaColumnas,key = lambda x: x) #Ordeno las columnas de menor a mayor
            palabra=''
            listaAuxiliar = verificar_diferencias(listaOrdenada) #Verifico si las diferencias entre las columnas son de 1.
            for n in listaAuxiliar:  #forma la palabra
                if(orientacion =='Horizontal'):
                    letra = dic[(fila,n)].get_letra()
                else:
                    letra = dic[(n,fila)].get_letra()
                palabra = palabra + letra
            print('Diccionario Tipo Palabra ',dicTipoPalabra[i])
            if(palabra.lower() in dicTipoPalabra[i]): #dicTipoPalabra diccionario {Color_en_Hexadecimal: [lista de palabras del color (tipo)]}
                palabrasAcertadas.append(palabra.lower())
    return palabrasAcertadas

# -------------------------------------------------------------------------------------------------------------- #
