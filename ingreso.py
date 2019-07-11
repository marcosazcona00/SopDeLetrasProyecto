#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import sys
import json
import PySimpleGUI as sg
from buscador import Buscador

def mostrar_palabras_ya_existentes(dic):
    '''
        Retorna una lista de las palabras que ya habian sido cargadas
    '''
    lista = []
    for i in dic:
        for j in dic[i]:
            lista.append(j)
    return lista



def buscar_palabra(palabra,dic):
    '''
        Busca si la palabra ya existe
    '''
    if(palabra in dic.keys()):
        return True
    else:
        return False

def eliminar_palabra(palabra,archivo):
    '''
        Elimina la palabra del archivo
    '''
    try:
        print('Entre')
        file = open(archivo,'r')
        dic = json.load(file)
        file.close()
        if(buscar_palabra(palabra,dic)): #Si la palabra ya existe
            del dic[palabra]
            file = open(archivo,'w')
            json.dump(dic,file)
            file.close()
    except json.JSONDecodeError:
        print('Archivo Vacio')

def verificar():
    '''
        Verifica si quiere o no ingresar nuevas palabras.
        La primer vez que se ejecute se pedirán palabras obligatoriamente
    '''
    aux = False
    dic = {"Verbo": [], "Sustantivo": [], "Adjetivo": []}
    file = None
    if (os.stat('tipos.json').st_size == 0):
        #Si el archivo está vacio, lo creo y agrego palabras
        file = open('tipos.json','w',encoding = 'utf-8')
        aux = True
    else:
        ok = sg.PopupYesNo('¿ Desea agregar nuevas palabras para jugar o eliminar alguna palabra cargada ?')
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
                if(palabra != ''):
                    window.FindElement('palabra_elegida').Update('')
                    searcher = Buscador(palabra)
                    (tipo,repetida) = searcher.validacion(lista,dic)
                    if(tipo != None): #Si está en wikcionario
                        tipo = tipo.capitalize() #Ponemos la primer letra mayuscula pues el diccionario sus claves tiene la primer letra Mayuscula
                        if(tipo in lAux):
                            #Si estaba en la lista de tipos
                            if(palabra not in dic[tipo]):
                                #Si la palabra no está en el tipo, la agrego
                                dic[tipo].append(palabra)
                                lista.append(palabra)
                            else:
                                sg.Popup('La palabra ingresada no es correcta, por tanto no será incluida en la sopa de letras')
                        else:
                            sg.Popup('La palabra ingresada no es correcta, por tanto no será incluida en la sopa de letras')
                    #Si retorno None, puede pasar que haya sido la primera vez y quiera borrar
                    if(repetida):
                        sg.Popup('Palabra ya existente')
                        ok = sg.PopupYesNo('¿ Desea eliminar la palabra {} ?'.format(palabra))
                        if(ok == 'Yes'):
                            dic[tipo].remove(palabra)
                            lista.remove(palabra)
                            eliminar_palabra(palabra,'definicion.json')
                            eliminar_palabra(palabra,'reporte.json')
                    window.FindElement('palabras_ingresadas').Update(values = lista) #Actualizamos el listbox de las palabras ya ingresadas
            elif(button == 'Finalizar'):
                file = open('tipos.json','w') #Lo abro de nuevo porque si hubo remove falla ya que un elemento se fue, pero escribe lo nuevo, lo anterior lo deja como estaba
                json.dump(dic,file)
                file.close()
                window.Close()
                break
            else:
                os._exit(1)
        except TypeError:
            break

            
def main_ingreso():
    '''
    Pide al profesor el ingreso de las palabras y escribe en reporte las palabras que no coincidieron
    '''

    # --------------------- Main Ingreso ------------------------- #
    nuevas_palabras,dic,file = verificar()
    if(nuevas_palabras):   #Solo se ejecutará si se desea agregar mas palabras o si no habia palabras cargadas
        file.close() #Cerramos el archivo si decide elegir nuevas palabras
        lista = mostrar_palabras_ya_existentes(dic) #Mostramos las palabras existentes en el listbox
        layout=[
            [sg.T('Ingrese sus palabras',key = 'text')],
            [sg.InputText('',key = 'palabra_elegida',size = (20,10))],
            [sg.Submit('Aceptar'),sg.Submit('Finalizar')],
            [sg.T('Palabras ya ingresadas: ')],
            [sg.Listbox(lista,size=(20,30),key='palabras_ingresadas')],
        ]

        window = sg.Window('Ingreso de palabras',size = (450,300)).Layout(layout)
        agregar_palabras(file,dic,window,lista)
