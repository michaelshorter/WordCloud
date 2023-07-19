# This code reads the state of a 4 position switch connected to pins GND, GPIO 6, GPIO 13, GPIO 19 and GPIO 26.
# Depending on the switch state it will display images 1-4 on the E-Ink Display.

import RPi.GPIO as GPIO
import os
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins connected to the switches
switch_pins = [6, 13, 19, 26]

# Set up the GPIO pins as inputs with internal pull-up resistors
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variable to store the previous switch state
prev_switch_state = None

# Function to determine the position of the switch
def get_switch_position():
    position = [GPIO.input(pin) for pin in switch_pins]
    return tuple(position)

# Function to print the switch position
def print_switch_position(position):
    if position == (0, 1, 1, 1):
        print("Mode 4")
        os.system("python3 dither-image-what.py --colour 'red' --image 'latestWordCloud.png'")
        print("Mode 4 process completed")

    elif position == (1, 0, 1, 1):
        print("Mode 3")
        os.system("python3 dither-image-what.py --colour 'red' --image 'test1.png'")
        print("Mode 3 process completed")

    elif position == (1, 1, 0, 1):
        print("Mode 1")
        os.system("python3 dither-image-what.py --colour 'red' --image 'test2.png'")
        print("Mode 1 process completed")
	
    elif position == (1, 1, 1, 0):
        print("Mode 2")
        os.system("python3 dither-image-what.py --colour 'red' --image 'LoadScreen.jpg'")
        print("Mode 2 process completed")

    else:
        print("Unknown Position")

# Main program
if __name__ == "__main__":
    try:
        while True:
            # Get the current position of the switch
            switch_position = get_switch_position()

            # Check if the switch state has changed
            if switch_position != prev_switch_state:
                # Introduce a 1-second delay
                time.sleep(1)

                # Print the switch position
                print_switch_position(switch_position)

                # Update the previous switch state
                prev_switch_state = switch_position
            
    except KeyboardInterrupt:
        # Clean up GPIO on keyboard interrupt
        GPIO.cleanup()
