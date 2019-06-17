#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import sys
import json
import matriz
import selector
import muestra_reporte
import PySimpleGUI as sg
from metodos_auxiliares_main import *
from menu import menu_opciones
from ingreso import main_ingreso


def main():
    '''
        JUGABLE
    '''
    ##Menu que pide si quiere o no nuevas palabras
    main_ingreso()

    #Muestra al profesor el reporte de palabras que generaron problemas
    muestra_reporte.mostrar_reporte()

    #Menu de opciones
    dic_color_cantPalabras,orientacion,ayuda,mayus = menu_opciones()

    #Devuelve la lista de palabras que estarán en la matriz
    listaPalabras,dicTipoPalabra=selector.main_selector(dic_color_cantPalabras)  #recibe las listas de palabras y lista de palabras desordenadas

    #Defino los atributos de la matriz
    grilla = matriz.Matriz()
    grilla.set_palabras(listaPalabras)
    tamX,tamY = grilla.get_tamaño()


    columna= definir_tipo_ayuda(ayuda,listaPalabras,dic_color_cantPalabras)
    layout, aux, window, graph = elegir_orientacion(columna,orientacion,list(dic_color_cantPalabras.keys()),tamX,tamY,dic_color_cantPalabras)

    if(aux == 1):
        dic = grilla.mostrar_matriz_horizontal(graph,mayus)
    else:
        dic = grilla.mostrar_matriz_vertical(graph,mayus)

    dicGeneral = dict()
    ok = True
    color = 'white'
    while(ok):
        event,values = window.Read()
        if(event == 'Terminar'):
            palabrasAcertadas = verificar_grilla(dicGeneral,dic,dicTipoPalabra,orientacion,dic_color_cantPalabras)
            window.Close()
            palabras_acertadas(listaPalabras,palabrasAcertadas)
            mostrar_resultado(listaPalabras,palabrasAcertadas)
            break
        elif(event == None):
            sys.exit()
        if(values['graph'] != (None,None)):
            #Si el evento del mouse no retorna None,None
            #aux = 0 #Aux va aca adentro inicializado porque no cambia
            columna = values['graph'][0] // 25
            fila = values['graph'][1] // 25
            print(values['combo'][0])
            ok1=grilla.cambiar((fila,columna),graph,dic_color_cantPalabras[values['combo']][0])
            if(orientacion == 'Horizontal'):
                llenar_diccionario(ok1,color,aux,dicGeneral,fila,columna,values['combo'])
            else:
                llenar_diccionario(ok1,color,aux,dicGeneral,columna,fila,values['combo'])
    # sys.exit()
    os._exit(1)

def llenar_diccionario(ok1,color,aux,dicGeneral,fila,columna,tipo):
    '''
        Distribuye las letras en el diccionario general que tiene Color:{fila:[columnas],fila[columnas]}
        este proceso va actualizando las letras que se seleccionan en la layout
    '''
    aux = 0
    if(ok1 and color != '#f4f4f4'):
        if(tipo not in dicGeneral):
            #Si el color no está en el diccionario, lo pone como clave
            dicGeneral[tipo] = dict()
        if(fila not in dicGeneral[tipo]):
            #Si la fila seleccionado no está en el diccionario del color elegido, se agrega
            dicGeneral[tipo][fila] = list()
        elif(fila in dicGeneral[tipo])and(columna in dicGeneral[tipo][fila]):
            #Si la fila está ya seleccionada y la columna tambien, significa que elegió deseleccionarla
            aux = 1
            dicGeneral[tipo][fila].pop(dicGeneral[tipo][fila].index(columna))
        if(aux == 0):
            #aux == 0 cuando haya seleccionado por primera vez
            dicGeneral[tipo][fila].append(columna)

def verificar_diferencias(listaOrdenada):
    '''
        Verifica que la diferencia entre las letras no sea mayor a 1
    '''
    listaAuxiliar = list()
    pos = 0
    if(listaOrdenada != []):
        for i in range(1,len(listaOrdenada)):
            if((listaOrdenada[i] - listaOrdenada[i-1] ) == 1):   #como arranca en 1  verifico el actual con el anterior
                listaAuxiliar.append(listaOrdenada[i-1])
                pos = i
            #Si la diferencia no dio 1, entonces al reporte
            elif (listaAuxiliar != []):  #si la lista no esta vacia entonces la diferencia se produce al final por lo que las letras despues de esta no seran validas
                break
        listaAuxiliar.append(listaOrdenada[pos])
    return listaAuxiliar

def verificar_grilla(dicGeneral,dic,dicTipoPalabra,orientacion,dicAux):
    '''
        Verifica si la palara es valida
        Recorre el dicionario de colores, elige cada palabra de cada color, concatena sus letras y verifica si es valida, comparando
        con dicTipoPalabra que es un diccionario con Llave color y valor lista de palabras seleccionadas para el color.
    '''
    palabrasAcertadas = []
    for i in dicGeneral: #i tiene los colores
        dicFilas = dicGeneral[i]
        #dicFilas es el diccionario con las claves que son las filas elegidas
        for fila in dicFilas:
            listaColumnas = dicGeneral[i][fila]
            #Me quedo con las columnas elegidas de esa fila
            listaOrdenada = sorted(listaColumnas,key = lambda x: x)
            #Ordeno las columnas de menor a mayor
            palabra=''
            #Verifico si las diferencias entre las columnas son de 1.
            listaAuxiliar = verificar_diferencias(listaOrdenada)
            for n in listaAuxiliar:
                if(orientacion =='Horizontal'):
                    letra = dic[(fila,n)].get_letra()
                else:
                    letra = dic[(n,fila)].get_letra()
                palabra = palabra + letra
            if(palabra.lower() in dicTipoPalabra[dicAux[i][0]]):
                palabrasAcertadas.append(palabra.lower())
                #dicAux[i][0] es el color en hexadecimal, porque i es el tipo Sustantivo, adjetivo o verbo
    return palabrasAcertadas

main()
