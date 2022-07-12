#This script deletes all contents of the contents.txt file when a button is pressed.
#Button is connected between GPIO 10 (5th pin close edge) and 5V (1st pin far edge)
import RPi.GPIO as GPIO

def button_callback(channel):
    print('content.txt deleted')
    file = open('content.txt','r+')
    file.truncate(0)
    file.close()
    

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)

message = input ('press enter to quit\n\n')

GPIO.cleanup()


        
        