#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import json
import collections
import PySimpleGUI as sg

# ---------  MODULOS  ---------------- #
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
            #Sino. como maximo mostrar para elegir 6
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
    ayuda=['Cantidad Tipos','Definiciones','Lista de palabras']
    letra=['Mayuscula','Minuscula']
    layout=[[sg.T('Menu de opciones')],
            [sg.Column(columna1, background_color='#dbdbdb'), sg.Column(columna2,background_color='#dbdbdb',key='columna2'),sg.Column(columna3,background_color='#dbdbdb')],
            [sg.T('    Seleccione la orientacion'),sg.InputCombo(orientacion,key='orientacion',size=(20,20))],
            [sg.T('    seleccione como desea que aparezcan las letras'),sg.InputCombo(letra,key='letra')],
            [sg.Submit('Aceptar'),sg.Submit('Cancelar')]
            ]
    return layout

def verificar_datos(dic):
    '''
        Verifica que todos los campos esten llenos
    '''
    ##Retorna True si todos están llenos
    ok = True
    for i in dic:
        if(dic[i] == ''):
            sg.Popup('Por favor llene todos los campos')
            ok = False
            break
    return ok

def agregar_color(dic,lista):
    '''
        Agrega los colores elegidos.
    '''
    lista.insert(2,dic['color_Verbos'])
    lista.insert(0,dic['color_Sustantivos'])
    lista.insert(1,dic['color_Adjetivos'])

def verificar_color_repetido(lista):
    '''
        Verifica si hubo o no repiticones de colores
    '''
    #Ejemplo
    #[A,B,C]
    #color = A
    #listaN = [B,C].
    #color = B
    #listaN = [C]
    #Sale porque no coincide con ok = false

    ##[A,B,A]
    ##color = A
    ##listaN = [B,A]
    ##color repetido, sale con ok = True porque coincidieron
    listaTipos = ['Verbo','Sustantivo','Adjetivo']
    ok = False #Si sale con false significa que no hubo colores repetidos
    for i in range(len(lista)-1):
        color = lista[i]
        listaN =  lista[i+1:len(lista)]
        for j in range(len(listaN)):
            if(color == listaN[j]):
                sg.Popup('Se repitio el color del tipo ',listaTipos[i], 'y', listaTipos[j+i+1])
                ok = True #Se repitio
                break
        if(ok):
            #Como no estamos seguros si el break corta con el primer for, lo verificamos acá si cortó por el ok = True
            break
    return ok

def verificar_cantidades(dic):
    if((dic['cantidad_sustantivo'] == '0')and(dic['cantidad_adjetivo'] == '0')and(dic['cantidad_verbo'] == '0')):
        sg.Popup('Elija por lo menos una palabra para un tipo')
        return False
    else:
        return True

def menu_opciones():
    '''
        Menu de Opciones
    '''
    layout = generar_layout()
    window=sg.Window('ventana').Layout(layout)
    dic_color_cantPalabras = {'Sustantivo': [],'Adjetivo':[],'Verbo':[]}
    while True:
        button,values=window.Read()
        if(button == 'Aceptar'):
            dic = values
            if(verificar_datos(values)):
                #Si todos los campos están lleno
                lista = []
                agregar_color(dic,lista)
                #Agregamos los colores seleccionados
                if(not verificar_color_repetido(lista) and (verificar_cantidades(dic))):
                    #Si no hubo colores repetidos
                    break
        elif(button == 'Cancelar')or(button == None):
            os._exit(1)
    window.Close()
    dic_color_cantPalabras['Sustantivo'] = [lista[0],dic['cantidad_sustantivo']]
    dic_color_cantPalabras['Adjetivo'] = [lista[1],dic['cantidad_adjetivo']]
    dic_color_cantPalabras['Verbo'] = [lista[2],dic['cantidad_verbo']]
    return (dic_color_cantPalabras,dic['orientacion'],dic['letra'])
