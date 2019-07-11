#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import json
import time
import PySimpleGUI as sg
<<<<<<< HEAD

def columna_ayudas(ayuda,listaPalabras,dic_color_cantPalabras):
    '''
        Devuelve la columna con la ayuda elegida
    '''
=======
import os

def definir_tipo_ayuda(ayuda,listaPalabras,dic_color_cantPalabras):
>>>>>>> efe5b110265e0a13a8487c22e8a2dc58b600afd5
    columna=[]
    if(ayuda == 'Cantidad Tipos'):
        for i in dic_color_cantPalabras:
            columna.append([sg.T(i + ' ' + dic_color_cantPalabras[i][1])])
    elif(ayuda == 'Definiciones'):
        with open('definicion.json','r') as file:
            try:
                dic = json.load(file)
                for i in listaPalabras:
                    if(i in dic.keys()):
                        columna.append([sg.T(dic[i])])
            except json.decoder.JSONDecodeError:
                #Si está vacío, significa que no hay definiciones disponibles.
                sg.Popup('No hay definiciones disponibles')
    else:
        for i in listaPalabras:
            columna.append([sg.T(i)])
    return columna

def screen(orientacion,colores_mostrar,tamX,tamY,dic_color_cantPalabras):
    '''
        Dibuja el layout dependiendo de la orientacion elegida.
        Retorna el layout
    '''
    ayuda=['Cantidad Tipos','Definiciones','Lista de palabras']
    if(orientacion == 'Horizontal'):
        #aux es una variable que indica la orientación
        aux = 1
        layout = [
                [sg.T('Tipo de Palabra'),sg.InputCombo(colores_mostrar,size = (20,20),key = 'combo')],
                [sg.T('Seleccione el tipo de ayuda'),sg.InputCombo(ayuda,key='ayuda'),sg.Submit('Ayuda')],
                [sg.Graph(canvas_size = (tamX,tamY),graph_bottom_left=(0,tamY), graph_top_right=(tamX,0),enable_events = True,key = 'graph')],
                [sg.Submit('Terminar')]
                ]
    else:
         aux = 2
         layout = [
             [sg.T('Tipo de Palabra'),sg.InputCombo(colores_mostrar,size = (20,20),key = 'combo')],
             [sg.T('Seleccione el tipo de ayuda'),sg.InputCombo(ayuda,key='ayuda'),sg.Submit('Ayuda')],
             [sg.Graph(canvas_size = (tamY,tamX),graph_bottom_left=(0,tamX), graph_top_right=(tamY,0),enable_events = True,key = 'graph')],
             [sg.Submit('Terminar')]
             ]
    window = sg.Window('Ventana').Layout(layout)
    window.Finalize()
    graph = window.FindElement('graph')

    return (layout,window,graph)


def palabras_acertadas(lista,palabrasAcertadas):
    '''
        Saca de la lista de palabras seleccionadas las palabras ya acertadas para mostrarlas en mostrar_resultado
    '''
    for i in palabrasAcertadas:
        if(i in lista): #Si la palabra elegida está en la lista de palabras.
            lista.pop(lista.index(i)) #Saco de la lista de palabras las acertadas
    return lista

def mostrar_resultado(lista,palabrasAcertadas):
    '''
        Muestra en un layout las palabras acertadas y erradas
    '''
    layout = [
            [sg.T('Palabras no Acertadas')],
            [sg.Listbox(lista,size = (10,6))],
            [sg.T('Palabras Acertadas')],
            [sg.Listbox(palabrasAcertadas, size = (12,6))]
            ]
    if(lista == []):
    #    sg.Popup('Felicitaciones, completaste la Sopa de Letras!')
        juego_completado = [sg.Image(filename= 'premio.png')],[sg.T(' ')]
        window_completado = sg.Window('Felicitaciones').Layout(juego_completado)
        window_completado.Read()
        window_completado.Close()
    else:
        sg.Popup('Bien! Estuviste muy cerca, la proxima te va a ir mejor')
    window = sg.Window('Resultado').Layout(layout)
    window.Read()

def ventana_ayuda(columna):
    layout = [
                [sg.Column(columna,background_color='#dbdbdb')],
                [sg.Submit('Cerrar')]
              ]
    window = sg.Window('Ayuda').Layout(layout)
    event,values = window.Read()
    if(event == 'None' or event == 'Cerrar'):
        window.Close()
