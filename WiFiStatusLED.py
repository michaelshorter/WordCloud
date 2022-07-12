# Script to light up LED when connected to wifi.
#LED connected to GPIO 18 (6th pin outside edge) and GND (3rd pin outside edge)
#Turns on if yes and off in no. Repeats every second.

import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
import subprocess

ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

while True:
    ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:

        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        print('Online')
        GPIO.output(18,GPIO.HIGH)
        sleep(1)
    
    
    except subprocess.CalledProcessError:
        print("Offline")
        GPIO.output(18,GPIO.LOW)
        sleep(1)
        