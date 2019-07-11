#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import json
import PySimpleGUI as sg

def mostrar_reporte():
    '''
        Muestra el reporte en pantalla
    '''
    try:
        fuente,dic = pedir_fuente()
        layout = []
        for i in dic:
            layout.append([sg.T(i.upper() + ': ' + dic[i],font = fuente)])
        window = sg.Window('Reporte').Layout(layout)
        event = window.Read()
        if(event == None):
            window.Close()
            os._exit(1)
    except (TypeError,ValueError):
<<<<<<< HEAD
        #levanta ValueError si eliminé y quedó el archivo con {}
        print(" ")

=======
        #levanta ValueError si eliminé una palabra y quedó el archivo con {}
        print(" ")
>>>>>>> efe5b110265e0a13a8487c22e8a2dc58b600afd5

def ventana_elegir_fuente():
    '''
        Muestra una ventana con las fuentes a elegir si el archivo reporte.json no estaba vacio
    '''
    layout = [
        [sg.T('Elija la funete con la quiere que se presente el reporte')],
        [sg.InputCombo(['Arial 12','Courier 12','Comic 12','Fixedsys 12','Times 12','Verdana 12'],size = (10,10),key = 'fuente')],
        [sg.Submit('Enviar')]
    ]
    window = sg.Window('Fuente del Reporte').Layout(layout)
    event,values = window.Read()

    if(event == 'Enviar'):
        window.Close()
        return values['fuente']
    else:
        os._exit(1)


def pedir_fuente():
    '''
        Pide al profesor la fuente con la que quiere mostrar el reporte
    '''
    file = open('reporte.json')
    try:
        dic = json.load(file)
    except json.decoder.JSONDecodeError:
<<<<<<< HEAD
        #Excepcion en caso de que el archivo se encuentre vacío
        sg.Popup('Archivo reporte ".json" Vacio. No habra reporte para mostrar')
        return None
    else:
        fuente = ventana_elegir_fuente()
        return (fuente,dic)
=======
        #SI el Json estaba vacio
        window.Close()
        sg.Popup('Archivo reporte ".json" Vacio. No habra reporte para mostrar')
        return None
    else:
        window.Close()
        file.close()
        return (values['fuente'],dic)
>>>>>>> efe5b110265e0a13a8487c22e8a2dc58b600afd5
