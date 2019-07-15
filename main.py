#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import json
import matriz
import selector
import muestra_reporte
import PySimpleGUI as sg
from menu import menu_opciones
from ingreso import main_ingreso
from metodos_verificadores import *
from metodos_auxiliares_main import *

# ---------  MODULOS  ---------------- #

def elegir_oficina():
    '''
        Pide al profesor la oficina. Retorna el look and feel
    '''
    look = 'GreenTan'
    file = open('datos-oficina.json','r')
    try:
        dic = json.load(file)
        file.close()
        layout = [
                  [sg.InputCombo(list(dic.keys()),size = (20,10)),sg.Submit('Enviar')]
                 ]
        window = sg.Window('Oficina').Layout(layout)
        event,values = window.Read()
        if(event == 'Enviar'):
            oficina = values[0]
            ultimo_registro = dic[oficina][-1] #Nos quedamos con el ultimo registro, el ultimo diccionario
            temperatura = int(ultimo_registro['temperatura'])
            if(temperatura <= 15):
                look = 'BlueMono'
            elif(temperatura > 15 and temperatura <= 28):
                look = 'SandyBeach'
            else:
                look = 'Purple'
            window.Close()
        return look
    except json.decoder.JSONDecodeError:  #Si no hay datos de oficinas en el archivo
        return look


def sin_contenido_tipos():
    '''
        Verifica si el profesor ingreso o no palabras
    '''
    try:
        file = open('tipos.json')
        dic = json.load(file)
        cant = 0
        for i in dic:
            if(dic[i] == []):
                cant+=1
        return (cant == 3)
        #Si retorna que cant == 3 significa que había 3 listas vacias de tipos.
        #Lo que quiere decir que no se cargaron datos en los tipos
    except json.decoder.JSONDecodeError:
        return True

def pedir_palabras_profesor():
    '''
        Pide al profesor palabras. Si no hay palabras, vuelve a pedir hasta que se ingrese al menos una palabra.
    '''
    main_ingreso()
    while(sin_contenido_tipos()):
        sg.Popup('No se ingresaron palabras')
        main_ingreso()

def mostrar_grilla(orientacion,grilla,graph,mayus):
    '''
        Dibuja la grilla en base a la orientación elegida para las palabras
    '''
    if(orientacion == 'Horizontal'):
        dic = grilla.mostrar_matriz_horizontal(graph,mayus)
    else:
        dic = grilla.mostrar_matriz_vertical(graph,mayus)
    return dic

def resultados_juego(listaPalabras,palabrasAcertadas):
    '''
    Muestra los resultados del juego
    '''
    palabras_acertadas(listaPalabras,palabrasAcertadas)
    mostrar_resultado(listaPalabras,palabrasAcertadas)

# ----------------------------------------- #

def main():
    '''
    JUGABLE
    '''
    # ----------------------------------------- #
                    #Variables
    dicGeneral = dict()
    # ----------------------------------------- #

    # ----------------------------------------- #
    #Menu que pide la oficina y retorna el look and feel
    look = elegir_oficina()
    sg.ChangeLookAndFeel(look)
    # ----------------------------------------- #

    # ----------------------------------------- #
                ##Menu que pide si quiere o no nuevas palabras
    pedir_palabras_profesor()
    # ----------------------------------------- #


    # ----------------------------------------- #
                #Muestra al profesor el reporte de palabras que generaron problemas
    muestra_reporte.mostrar_reporte()
    # ----------------------------------------- #


    # ----------------------------------------- #
                #Menu de opciones
    dic_color_cantPalabras,orientacion,mayus = menu_opciones()
    # ----------------------------------------- #


    # ----------------------------------------- #
                #Devuelve la lista de palabras que estarán en la matriz
    listaPalabras,dicTipoPalabra=selector.main_selector(dic_color_cantPalabras)  #Retorna las listas de palabras y lista de palabras desordenadas
    # ----------------------------------------- #


    # ----------------------------------------- #
                #Defino los atributos de la matriz
    grilla = matriz.Matriz()
    grilla.set_palabras(listaPalabras)
    tamX,tamY = grilla.get_tamaño()
    # ----------------------------------------- #

    # ----------------------------------------- #
                #Devuelve el layout y el graph ya dibujado
    layout, window, graph = screen(orientacion,list(dic_color_cantPalabras.keys()),tamX,tamY,dic_color_cantPalabras)
    # ----------------------------------------- #


    # ----------------------------------------- #
    dic = mostrar_grilla(orientacion,grilla,graph,mayus)
    #dic es un diccionario de clave (fila,columna) y valor, la referencia del objeto celda correspondiente a esa fila y columna
    # ----------------------------------------- #


    # ----------- Sopa de Letras  ---------------- #
    while True:
        event,values = window.Read()
        if(event == 'Ayuda'):
            columna = columna_ayudas(values['ayuda'],listaPalabras,dic_color_cantPalabras)
            ventana_ayuda(columna)
        elif(event == 'Terminar'):
            palabrasAcertadas = verificar_grilla(dicGeneral,dic,dicTipoPalabra,orientacion,dic_color_cantPalabras)
            window.Close()
            resultados_juego(listaPalabras,palabrasAcertadas)
            break
        elif(event == None):
            os._exit(1)
        if(values['graph'] != (None,None)): #Si el evento del mouse no retorna None,None
            columna = values['graph'][0] // 25
            fila = values['graph'][1] // 25
            try: #esto porque puede tocar un pixel que no corresponde
                ok1=grilla.cambiar((fila,columna),graph,dic_color_cantPalabras[values['combo']][0])
                if(orientacion == 'Horizontal'):
                    #llenar_diccionario(ok1,dicGeneral,fila,columna,values['combo'])
                    llenar_diccionario(ok1,dicGeneral,fila,columna,dic_color_cantPalabras[values['combo']][0])
                else:
                    llenar_diccionario(ok1,dicGeneral,columna,fila,dic_color_cantPalabras[values['combo']][0])
            except KeyError:
                print('posicion fuera de rango')
    # ----------------------------------------- #

def playable():
    '''
        Ejecuta el juego, y una vez finalizado pide si quiere o no volver a jugarlo
    '''
    while True:
        main()
        boton = sg.PopupYesNo('Desea jugar nuevamente')
        if(boton == 'No'):
            break


if __name__ == '__main__':
    '''
        Se ejecutará desde el módulo main.py
    '''
    playable()
