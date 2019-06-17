#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import PySimpleGUI as sg
import json
import os

def devolver_cantidades_tipos():
    '''
        Devuelve la cantidad de palabras de cada tipo.
        Si hay más de 6 palabras, da la posibilidad de como máximo elegir 6
    '''
    with open('tipos.json','r') as file:
        dic = json.load(file)
    cantidad = list()
    for i in dic:
        if(len(dic[i]) < 6):
            #Si la cantidad de palabras que tiene el diccionario son menos de 6, mostrar las que tiene + 1
            cantidad.append(len(dic[i])+1)
        else:
            #Sino. como maximo mostrar para elegir 7
            cantidad.append(7)
    return cantidad

def generar_layout():
    '''
        Genera layout menu principal
    '''
    cantidad = devolver_cantidades_tipos()
    columna1=[  [sg.Text('Verbos',background_color='#dbdbdb')],
                [sg.T('cantidad',background_color='#dbdbdb'),sg.InputCombo([x for x in range(cantidad[0])],key='cantidad_verbo',size=(20,20),change_submits=True ,enable_events =True)],
                 [sg.T('Color para representarlo ',background_color='#dbdbdb'),sg.ColorChooserButton('Elegir color',key='color_Verbos')]
            ]
    columna2=[
              [sg.T('Sustantivos',background_color='#dbdbdb')],
              [sg.T('cantidad',background_color='#dbdbdb'),sg.InputCombo([x for x in range(cantidad[1])],key='cantidad_sustantivo',size=(20,20),enable_events =True)],
               [sg.T('Color para representarlo ',background_color='#dbdbdb'),sg.ColorChooserButton('Elegir color',key='color_Sustantivos')]
             ]
    columna3=[
              [sg.T('Adjetivos',background_color='#dbdbdb')],
              [sg.T('cantidad',background_color='#dbdbdb'),sg.InputCombo([x for x in range(cantidad[2])],key='cantidad_adjetivo',size=(20,20),enable_events =True)],
              [sg.T('Color para representarlo ',background_color='#dbdbdb'),sg.ColorChooserButton('Elegir color',key='color_Adjetivos')]
             ]
    orientacion=['Horizontal','vertical']
    ayuda=['Ninguna','definiciones','Lista de palabras']
    letra=['Mayuscula','Minuscula']
    layout=[[sg.T('Menu de opciones')],
            [sg.Column(columna1, background_color='#dbdbdb'), sg.Column(columna2,background_color='#dbdbdb',key='columna2'),sg.Column(columna3,background_color='#dbdbdb')],
            [sg.T('    Seleccione la orientacion'),sg.InputCombo(orientacion,key='orientacion',size=(20,20)),sg.T('Seleccione el tipo de ayuda'),sg.InputCombo(ayuda,key='ayuda')],
            [sg.T('    seleccione como desea que aparezcan las letras'),sg.InputCombo(letra,key='letra')],
            [sg.Submit('Aceptar'),sg.Submit('Cancelar')]
            ]
    return layout

def verificar_datos(dic):
    '''
        Verifica que todos los campos esten llenos
    '''
    print(dic)
    ok = True
    for i in dic:
        if(dic[i] == ''):
            sg.Popup('Por favor llene todos los campos')
            ok = False
            break
    return ok

def menu_opciones():
    layout = generar_layout()
    window=sg.Window('ventana').Layout(layout)
    dic_color_cantPalabras = {'Sustantivo': [],'Adjetivo':[],'Verbo':[]}
    while True:
        button,values=window.Read()
        if(button == 'Aceptar'):
            dic = values
            if(verificar_datos(values) != False):
                #Si todos los campos están llenos
                break
        elif(button == 'Cancelar')or(button == None):
            os._exit(1)
    window.Close()
    dic_color_cantPalabras['Sustantivo'] = [dic['color_Sustantivos'],dic['cantidad_sustantivo']]
    dic_color_cantPalabras['Adjetivo'] = [dic['color_Adjetivos'],dic['cantidad_adjetivo']]
    dic_color_cantPalabras['Verbo'] = [dic['color_Verbos'],dic['cantidad_verbo']]
    return (dic_color_cantPalabras,dic['orientacion'],dic['ayuda'],dic['letra'])
