#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import json
import PySimpleGUI as sg
import pattern
from pattern.es import tag
from pattern.web import Wiktionary,SEARCH

class Buscador:
    def __init__(self,palabra):
        self.__razon = ''
        self.__tipo = None
        self.__palabra = palabra
        self.__objeto_buscador = None
        self.__dic = {'JJ':'adjetivo','VB':'verbo','NN':'sustantivo'}


    def __verficar_palabra_wikcionario(self):
        '''
            Verifica si la palabra existe en wikcionario y devuelve su tipo
        '''
        buscador = Wiktionary(language = 'es')
        try:
            self.__objeto_buscador = buscador.search(self.__palabra,type = SEARCH)
            self.__tipo =  self.__objeto_buscador.sections[3].title.split()[0].lower()
        except (AttributeError,IndexError,pattern.web.URLError):
            print('Error')
        else:
            sg.Popup(self.__tipo,auto_close=True,auto_close_duration=1)
        return self.__tipo

    def __verificar_palabra_patterEs(self):
        '''
            Devuelve el tipo de la palabra de Pattern.es
        '''
        tipo = ' '
        try:
            tipo =  self.__dic[tag(self.__palabra)[0][1]]
        except (IndexError,KeyError):
            print('Error con pattern')
        finally:
            return tipo


    def __generar_reporte(self,archivo):
        '''
            Metodo que genera el reporte de la palabra
        '''
        if os.stat(archivo).st_size != 0:
            file = open(archivo,'r')
            dic = json.load(file)
            file.close()
            #Si está vacio el Archivo
        else:
            dic=dict()
        file = open(archivo,'w')
        dic[self.__palabra] = self.__razon
        json.dump(dic,file)
        file.close()

    def validacion(self,lista,dic):
        '''
            Se evalúa el tipo de la palabra entre Pattern y Wikcionario. En caso de conflicto, se genera el correspondiente reporte

        '''
        tipoWikcionario = self.__verficar_palabra_wikcionario()
        tipoPattern = self.__verificar_palabra_patterEs()
        if(self.__palabra not in lista):
            #Si está reptida
            if(tipoWikcionario != None):
                #SI existe en wikcionario
                    self.__tipo = tipoWikcionario
                    if(self.__tipo in self.__dic.values()): #Si son distintios pero el tipo Wikcionario es un Sustantivo Adjetivo o Verbo
                        self.__razon = self.__obtener(self.__objeto_buscador.sections[3].string)
                        self.__generar_reporte('definicion.json')
                    if(tipoWikcionario != tipoPattern): #Si wikcionario y pattern no coincidiero
                        self.__razon = 'No coincidio con pattern'
                        self.__generar_reporte('reporte.json')
            else: #No estaba en wikcionarios
                if(tipoPattern != 'sustantivo'): ##Si pattern me devuelve un tipo válido
                    self.__tipo = tipoPattern
                    self.__razon = sg.PopupGetText('Ingrese la defincion de la palabra ',self.__palabra)
                    self.__generar_reporte('definicion.json')
                    self.__razon='No estaba en wikcionario'
                else: #No estaba en patter ni wikcionario
                    self.__razon = 'No estaba en pattern ni wikcionario'
                    self.__tipo = None
                self.__generar_reporte('reporte.json')
            return (self.__tipo,False)
        else: #Si está repetida, buscamos el tipo
            for i in dic:
                if(self.__palabra in dic[i]):
                    self.__tipo = i #Me quedó con el tipo de la Palabra
                    break
            return self.__tipo,True

    def __separar_defincion(self,definicion):
        '''
            Separa la definicion hasta encontrar un punto
        '''
        cadena = ''
        for i in range(len(definicion)):
            if(definicion[i] != '.'):
                cadena+=definicion[i] #Concateno las letras de la definicion
            else:
                break
        return cadena

    def __obtener(self,definicion):
        '''
            Obtiene una unica definicion
        '''
        palabra = ''
        definicion = str(definicion).split('\n')
        #La defincion la creo como una lista separada por renglones
        for n in range(0,len(definicion)):
            if(definicion[n] != ''):
                if(definicion[n][0] == '1'):
                    definicion_corta = definicion[n][1:]
                    palabra = self.__separar_defincion(definicion_corta)
                    break
        return palabra
