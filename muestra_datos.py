import time
import PySimpleGUI as sg
from sonido import Sonido
from matriz_led import Led
from temperatura import Temperatura


def main():
    #variables
    sound = Sonido()
    temp = Temperatura()
    matriz_led = Led()

    while True:
        if(sound.evento_detectado()):
            datos = temp.datos_sensor() #Me cargo los datos procesados
            mensaje = 'Temperatura' + str(datos['temperatura']) + 'Humedad ' + str(datos['humedad']) #Me quedo con el último registro ambiental del archivo de la oficina en la que estoy
            matriz_led.mostrar_mensaje(msg = mensaje) #Mando el mensaje a mostrar
            event = sg.PopupYesNo('Terminar',auto_close=True,auto_close_duration=2)
            if(event == 'Yes'):
                break

if __name__ == '__main__':
    main()
