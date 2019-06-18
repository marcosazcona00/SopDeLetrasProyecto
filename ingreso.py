#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import PySimpleGUI as sg
from buscador import Buscador
import json
import sys
import os

def mostrar_palabras_ya_existentes(dic):
    lista = []
    for i in dic:
        for j in dic[i]:
            lista.append(j)
    return lista

def main_ingreso():
    '''
    Pide al profesor el ingreso de las palabras y escribe en reporte las palabras que no coincidieron
    Pide que ingrese colores y cantidades para los tipos
    '''

    def verificar():
        aux = False
        dic = {"Verbo": [], "Sustantivo": [], "Adjetivo": []}
        file= None
        if (os.stat('tipos.json').st_size == 0):
            #Si el archivo está vacio, lo creo y agrego palabras
            file = open('tipos.json','w',encoding = 'utf-8')
            aux = True
        else:
            ok = sg.PopupYesNo('¿ Desea agregar nuevas palabras para jugar ?')
            #Si no está vacio pregunto si quiere agregar nuevas
            if(ok == 'Yes'):
                #Si desea agregar,abrimos el archivo como lectura escritura
                file = open('tipos.json','r',encoding = 'utf-8')
                aux = True
                dic = json.load(file)
            elif(ok != 'No'):
                #Si no selecciono el boton de Si ni No es porque apretó la X de salir
                os._exit(1)

        return (aux,dic,file)

    def agregar_palabras(file,dic,window,lista):
        '''
            Agrega las nuevas palabras al archivo
            En caso de existir alguna, permite la opcion de borrarla
            Si no existe, pide una defincion y se la guarda en definicion.json
        '''
        lAux = ['Sustantivo','Adjetivo','Verbo']
        while True:
            repetida = False
            button,values=window.Read()
            try:
                palabra = values['palabra_elegida']
                if(button == 'Aceptar'):
                    if(palabra in lista):
                        repetida = True
                    window.FindElement('palabra_elegida').Update('')
                    searcher = Buscador(palabra)
                    tipo = searcher.validacion(repetida)
                    if(tipo != None):
                        #Si está en wikcionario
                        tipo = tipo.capitalize() #Ponemos la primer letra mayuscula pues el diccionario sus claves tiene la primer letra Mayuscula
                        if(tipo in lAux):
                          #Si estaba en el diccionario el tipo
                            if(palabra not in dic[tipo]):
                                #Si la palabra no está en el tipo, la agrego
                                dic[tipo].append(palabra)
                                lista.append(palabra)
                            else:
                                #En caso de ya existir, aviso que existe
                                sg.Popup('Palabra ya existente')
                                ok = sg.PopupYesNo('¿ Desea eliminar la palabra {} ?'.format(palabra))
                                #Si no está vacio pregunto si quiere agregar nuevas
                                if(ok == 'Yes'):
                                    dic[tipo].remove(palabra)
                                    lista.remove(palabra)
                            window.FindElement('palabras_ingresadas').Update(values = lista)
                        else:
                            sg.Popup('La palabra ingresada no es correcta, por tanto no será incluida en la sopa de letras')
                    else:
                        sg.Popup('La palabra ingresada no es correcta, por tanto no será incluida en la sopa de letras')
                elif(button == 'Finalizar'):
                    file = open('tipos.json','w') #Lo abro de nuevo porque si hubo remove se rompe ya que un elemento se fue, pero escribe lo nuevo, lo anterior lo deja como estaba
                    json.dump(dic,file)
                    file.close()
                    window.Close()
                    break
                else:
                    os._exit(1)
            except TypeError:
                break



    aux,dic,file = verificar()
    if(aux):   #solo se ejecutara si se desea agregar mas palabras o si no habia palabras cargadas
        file.close() #Cierro el archivo aca
        lista = mostrar_palabras_ya_existentes(dic)
        print(lista)
        layout=[[sg.T('Ingrese sus palabras',key = 'text')],
            [sg.InputText('',key = 'palabra_elegida'),sg.Submit('Aceptar')],
            [sg.T('Palabras ya ingresadas: ')],
            [sg.Listbox(lista,size=(20,30),key='palabras_ingresadas')],
            [sg.Submit('Finalizar')]
        ]

        window = sg.Window('Ingreso de palabras').Layout(layout)
        agregar_palabras(file,dic,window,lista)
