<img src="BabySpy/pir_wiring.png">
import RPi.GPIO as GPIO
import datetime
import time


pir=21
try:
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pir,GPIO.IN)
        if GPIO.input(pir):
            print('Kίνηση...:',datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S'))
            time.sleep(1)
                        
except KeyboardInterrupt:
    GPIO.cleanup()
    print('Καλή Συνέχεια')
    
