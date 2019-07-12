#@Autores: Azcona Marcos -> Alvarez Cristian Gabriel
import os
import json
import time
import PySimpleGUI as sg
from sonido import Sonido
from matriz_led import Led
from temperatura import Temperatura

class Registro:

    def __init__(self):
        self.__oficina = ''
        self.__dic = dict()

    def set_oficina(self,oficina):
        self.__oficina = oficina

    def get_oficina(self):
        return self.__oficina

    def __verificar_archivo(self):
        '''
            Verifica si el archivo tenía o no datos ya cargados previamente. Se ejecutará desde Sopa De Letras, previo a cualquier línea de código a ejecutar
        '''
        if(os.stat('datos-oficina.json').st_size != 0): #Si no está vacío, cargo lo que tiene en memoria
            file = open('datos-oficina.json','r')
            self.__dic = json.load(file)
            file.close()
        if((os.stat('datos-oficina.json').st_size == 0) or (self.get_oficina() not in self.__dic.keys())):
            self.__dic[self.get_oficina()] = list()

    def interfaz(self):
        '''
            Se pide al usuario la oficina sobre la que desea obtener y actualizar datos
        '''
        layout = [
                    [sg.InputText('Ingrese la oficina')],
                    [sg.Submit('Enviar')]
                ]

        window = sg.Window('Oficina').Layout(layout)
        while True:
            event,values = window.Read()
            if(event == 'Enviar' and values[0] != ''):
                self.set_oficina(values[0])
                window.Close()
                break
            if(event != 'Enviar' or values[0] == ''):
                event = sg.Popup('Ingrese el nombre de una oficina',auto_close=True,auto_close_duration=2)

    def loop(self):
        '''
            Metodo que itera guardando los datos de temperatura obtenidos
        '''
        #Variables
        self.__verificar_archivo()
        temp = Temperatura()
        matriz_led = Led()

        while True:
            datos = temp.datos_sensor() #Me cargo los datos procesados
            self.__dic[self.get_oficina()].append(datos)
            event = sg.PopupYesNo('Terminar')
            if(event == 'Yes'):
                break
            time.sleep(60) #Espera 60 segundos para volver a iterar
        file = open('datos-oficina.json','w')
        json.dump(self.__dic,file)
        file.close()


def main():
    registro = Registro()
    registro.interfaz()
    registro.loop()

if __name__ == '__main__':
    main()
