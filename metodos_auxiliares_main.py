#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import json
import PySimpleGUI as sg
import os
def definir_tipo_ayuda(ayuda,listaPalabras,dic_color_cantPalabras):
    columna=[]
    if(ayuda == 'Ninguna'):
        for i in dic_color_cantPalabras:
            columna.append([sg.T(i + ' ' + dic_color_cantPalabras[i][1])])
    elif(ayuda == 'definiciones'):
        with open('definicion.json','r') as file:
            try:
                dic = json.load(file)
                for i in listaPalabras:
                    if(i in dic.keys()):
                        columna.append([sg.T(dic[i])])
            except json.decoder.JSONDecodeError:
                sg.Popup('No hay definiciones disponibles')
    else:
        for i in listaPalabras:
            columna.append([sg.T(i)])
    return columna

def elegir_orientacion(columna,orientacion,colores_mostrar,tamX,tamY,dic_color_cantPalabras):
    '''
        Dibuja el layout dependiendo de la orientacion elegida.
        Retorna el layout
    '''
    if(orientacion == 'Horizontal'):
        aux = 1
        layout = [
                [sg.InputCombo(colores_mostrar,size = (20,20),key = 'combo')],
                [sg.Graph(canvas_size = (tamX,tamY),graph_bottom_left=(0,tamY), graph_top_right=(tamX,0),enable_events = True,key = 'graph'),sg.Column(columna,background_color='#dbdbdb')],
                [sg.Submit('Terminar')]
                ]
    else:
         aux = 2
         layout = [
             [sg.T('tipo de palabra'),sg.InputCombo(colores_mostrar,size = (20,20),key = 'combo')],
             [sg.Graph(canvas_size = (tamY,tamX),graph_bottom_left=(0,tamX), graph_top_right=(tamY,0),enable_events = True,key = 'graph'),sg.Column(columna,background_color='#dbdbdb')],
             [sg.Submit('Terminar')]
             ]
    window = sg.Window('Ventana').Layout(layout)
    window.Finalize()
    graph = window.FindElement('graph')

    return (layout,aux,window,graph)

def palabras_acertadas(lista,palabrasAcertadas):
    '''
        Saca de la lista de palabras seleccionadas las palabras ya acertadas para mostrarlas en mostrar_resultado
    '''
    for i in palabrasAcertadas:
        if(i in lista):
            lista.pop(lista.index(i))
    return lista

def mostrar_resultado(lista,palabrasAcertadas):
    '''
        Muestra en un layout las palabras acertadas y erradas
    '''
    print('lista',lista)
    layout = [
            [sg.T('Palabras no Acertadas')],
            [sg.Listbox(lista,size = (10,6))],
            [sg.T('Palabras Acertadas')],
            [sg.Listbox(palabrasAcertadas, size = (12,6))]
            ]
    if(lista == []):
        sg.Popup('Felicitaciones, completaste la Sopa de Letras!')
    else:
        sg.Popup('Bien! Estuviste muy cerca, la proxima te va a ir mejor')
    window = sg.Window('Resultado').Layout(layout)
    window.Read()
    os._exit(1)
