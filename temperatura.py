import Adafruit_DHT
from datetime import datetime

class Temperatura:
    def __init__(self,pin = 17, sensor = Adafruit_DHT.DHT11):
        self.__sensor = sensor
        self.__data_pin = pin

    def __obtener_fecha(self):
        now = datetime.now()
        fecha = str(now.year) + '/' + str(now.month) + '/' + str(now.day)
        return fecha

    def datos_sensor(self):
        humedad,temperatura = Adafruit_DHT.read_retry(self.__sensor,self.__data_pin)
        return {'temperatura':temperatura, 'humedad':humedad, 'fecha':self.__obtener_fecha()}
