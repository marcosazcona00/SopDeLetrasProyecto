#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import PySimpleGUI as sg
import json
import os

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
        #levanta ValueError si eliminé una palabra y quedó el archivo con {}
        print(" ")

def pedir_fuente():
    '''
        Pide al profesor la fuente con la que quiere mostrar el reporte
    '''
    layout = [
        [sg.T('Elija la funete con la quiere que se presente el reporte')],
        [sg.InputCombo(['Arial 12','Courier 12','Comic 12','Fixedsys 12','Times 12','Verdana 12'],size = (10,10),key = 'fuente')],
        [sg.Submit('Enviar')]
    ]
    window = sg.Window('Fuente del Reporte').Layout(layout)
    event,values = window.Read()

    if(event == 'Enviar'):
        print('enviado')
    else:
        window.Close()
        os._exit(1)

    file = open('reporte.json')
    try:
        dic = json.load(file)
    except json.decoder.JSONDecodeError:
        #SI el Json estaba vacio
        window.Close()
        sg.Popup('Archivo reporte ".json" Vacio. No habra reporte para mostrar')
        return None
    else:
        window.Close()
        file.close()
        return (values['fuente'],dic)
