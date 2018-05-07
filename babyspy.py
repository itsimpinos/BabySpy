#raspivid -o - -t 0 -n -w 600 -h 400 -fps 12 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264
#Ανοίγω vlc και rtsp://###.###.###.###:8554/
#where ###.###.###.### is the IP address of the RPi.
import Adafruit_DHT
import RPi.GPIO as GPIO
import datetime
import time
import os
import sys
import subprocess
from guizero import App, Text, PushButton
#sudo pip3 install guizero για εγκατάσταση της guizero

import smtplib

def clear():
 
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def write_temp(temp):
    with open("{0}_temp.csv".format(datetime.datetime.now().strftime("%d-%m-%Y")), "a") as log:
    #with open("babyspy_temp.csv", "w") as log:
        log.write("{0},{1}\n".format(datetime.datetime.now().strftime("%H:%M:%S"),str(temp)))

def write_hum(humidity):
    with open("{0}_hum.csv".format(datetime.datetime.now().strftime("%d-%m-%Y")), "a") as log:
    #with open("babyspy_hum.csv", "w") as log:
        log.write("{0},{1}\n".format(datetime.datetime.now().strftime("%H:%M:%S"),str(humidity)))

def write_move():
    with open("{0}_move.csv".format(datetime.datetime.now().strftime("%d-%m-%Y")), "a") as log:
    #with open("babyspy_move.csv", "w") as log:
        log.write("{0}\n".format(datetime.datetime.now().strftime("%H:%M:%S")))

def close():
    App.destroy(app)

def movement():
    App.destroy(app)


pir=21
pin=4
SoundPin=16

humidity, temp = Adafruit_DHT.read_retry(11,pin)
clear()
app = App(title="Θερμοκρασία", height=100, width=400)
app.title = "Θερμοκρασία - Υγρασία!"
text = Text(app, text="Θερμοκρασία: {0:0.1f} C Υγρασία: {1:0.1f} %".format(temp, humidity))
button = PushButton(app, text="ΟΚ",command=close)                      
app.display()        


#print ('Θερμοκρασία: {0:0.1f} C Υγρασία: {1:0.1f} %'.format(temp, humidity))
h1=humidity
write_hum(humidity)
t1=temp
write_temp(temp)

try:
    while True:
        humidity, temp = Adafruit_DHT.read_retry(11,pin)
        if h1!= humidity:
            clear()
            #print ('Θερμοκρασία: {0:0.1f} C Υγρασία: {1:0.1f} %'.format(temp, humidity))
            write_hum(humidity)
            h1=humidity
        if t1!= temp:    
            clear()
            #print ('Θερμοκρασία: {0:0.1f} C Υγρασία: {1:0.1f} %'.format(temp, humidity))
            write_temp(temp)
            t1=temp
        if abs(temp-t1)>5:
            app = App(title="Θερμοκρασία", height=100, width=400)
            app.title = "Θερμοκρασία!"
            text = Text(app, text="Θερμοκρασία > 20!!")
            button = PushButton(app, text="ΟΚ",command=close)                      
            app.display()           
           
                        
        while True:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pir,GPIO.IN)
            if (GPIO.input(pir)==1):
                #Για να μη τρέχει στην εκκίνηση η camera
                #sudo nano /etc/rc.local
                #Και διαγράφουμε τη γραμμή
                #(sleep 10;python3 home/pi/camerapi.py)&
                
                #subprocess.Popen("python3 camerapi.py", shell=True)                
                #os.system('python3 camerapi.py')

                #clear()
                                
                server = smtplib.SMTP_SSL('smtp.gmail.com',port=465) #server for sending the email

                server.ehlo() # simple starting of the connection
                server.login('babyspy5ek','b@byspy1') # login credentials and password


                msg = """From:babyspy5ek
                Subject: Babyspy \n
                Alert, open browser
                """

                server.sendmail('babyspy5ek@gmail.com','babyspy5ek@gmail.com',msg) # this is where the email is sent to the recipient

                server.quit() # exit the connection


                
                #app = App(title="Κίνηση", height=100, width=600)
                #app.title = "Κίνηση!"
                #text = Text(app, text="Υπάρχει κίνηση!!")
                #text = Text(app, text=datetime.datetime.now().strftime('%d-%m-%y  %H:%M:%S'))
                #text = Text(app, text="Ανοίξτε τον browser στη συσκευή σας για livstreaming!!")
                #button = PushButton(app, text="ΟΚ",command=close)                      
                #app.display()       
                                   
                #print('Ανησυχία...:', datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S'))
                write_move()
            else:
                time.sleep(5)
                break

except KeyboardInterrupt:
    GPIO.cleanup()
    print('''Καλή Συνέχεια
             Τα δεδομένα έχουν καταγραφεί στα εξής αρχεία:
             Θερμοκρασία  : /home/pi/Ημερομηνία_temp.csv
             Υγρασία      : /home/pi/Ημερομηνία_hum.csv
             Κινητικότητα : /home/pi/Ημερομηνία_move.csv''')
    
      
