import RPi.GPIO as GPIO

class Sonido:
    def __init__(self,canal = 22):
        self.__canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__canal,GPIO.IN)
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self.__canal,GPIO.RISING)

    def evento_detectado(self):
        if(GPIO.event_detected(self.__canal)):
            return True
        else:
            return False
