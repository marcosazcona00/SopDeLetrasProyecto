#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import json
import PySimpleGUI as sg
from pattern.es import tag
from pattern.web import Wiktionary,SEARCH

class Buscador:
    def __init__(self,palabra):
        self.__razon = ''
        self.__tipo = None
        self.__definicion = ''
        self.__palabra = palabra
        self.__objeto_buscador = None
        self.__dic = {'JJ':'adjetivo','VB':'verbo','NN':'sustantivo'}

    def get_tipo(self):
        return self.__tipo

    def __verficar_palabra_wikcionario(self):
        '''
            Verifica si la palabra existe en wikcionario y devuelve su tipo
        '''
        buscador = Wiktionary(language = 'es')
        self.__objeto_buscador = buscador.search(self.__palabra,type = SEARCH)
        try:
            ##objeto_buscador es de tipo WiktionaryArticle
            self.__tipo =  self.__objeto_buscador.sections[3].title.split()[0].lower()
        except (AttributeError,IndexError):
            ##Hacer reporte de que no estaba en wikcionario
            sg.Popup('error')
            return None
        else:
            sg.Popup(self.__tipo)
        return self.__tipo

    def __verificar_palabra_patterEs(self):
        '''
            Devuelve el tipo de la palabra de Pattern.es
        '''
        try:
            return self.__dic[tag(self.__palabra)[0][1]]
        except (IndexError,KeyError):
            return ' '

    def get_defincion(self):
        return self.__razon

    def __generar_reporte(self,archivo):
        '''
            Metodo que genera el reporte de la palabra
        '''
        print('entre')
        if os.stat(archivo).st_size != 0:
            file = open(archivo,'r')
            dic = json.load(file)
            file.close()
            #Si está vacio el Archivo
        else:
            dic=dict()
        file = open(archivo,'w')
        print('Razon',self.__razon)
        dic[self.__palabra] = self.__razon
        json.dump(dic,file)
        file.close()

    def validacion(self,repetida):
        '''
            se asume que toda palabra que no este en wikcionario y patter retorna que es sustantivo, sera una palabra invalida
            Asumimos que si no es una palabra valida, pattern la devuelve como sustantivo

        '''
        tipoWikcionario = self.__verficar_palabra_wikcionario()
        tipoPattern = self.__verificar_palabra_patterEs()
        print('Wikcionario ',tipoWikcionario)
        print('Pattern ',tipoPattern)
        if(tipoWikcionario != None):
            #SI existe en wikcionario
                self.__tipo = tipoWikcionario
                print('Valores: ',self.__dic.values())
                if(tipoWikcionario != tipoPattern):
                    #Si wikcionario y pattern no coincidiero
                    self.__razon = 'No coincidio con pattern'
                    self.__generar_reporte('reporte.json')
                if(self.__tipo in self.__dic.values()): #Si son distintios pero el tipo Wikcionario es un Sustantivo Adjetivo o Verbo
                    self.__razon = self.__obtener(self.__objeto_buscador.sections[3].string)
                    self.__generar_reporte('definicion.json')    

        else:
            #No estaba en wikcionarios
            if(tipoPattern != 'sustantivo'):
                ##Si pattern me devuelve un tipo válido
                self.__tipo = tipoPattern
                if(not repetida):
                    self.__razon = sg.PopupGetText('Ingrese la defincion de la palabra ',self.__palabra)
                    self.__generar_reporte('definicion.json')
                    self.__razon='No estaba en wikcionario'
                    self.__generar_reporte('reporte.json')
            else:
                #No estaba en patter ni wikcionario
                self.__razon = 'No estaba en pattern ni wikcionario'
                self.__generar_reporte('reporte.json')
                return None
        return self.__tipo


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
        definicion = str(definicion).split('\n')
        #La defincion la creo como una lista separada por renglones
        for n in range(0,len(definicion)):
            if(definicion[n] != ''):
                if(definicion[n][0] == '1'):
                    definicion_corta = definicion[n][1:]
                    palabra = self.__separar_defincion(definicion_corta)
                    break
        return palabra
