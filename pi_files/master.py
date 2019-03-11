#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time

reader = SimpleMFRC522.SimpleMFRC522()

op = [36, 37]

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
         
        while True:
                _, prompt = reader.read()
                
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(op, GPIO.OUT)
                
                if prompt.strip() == text:
                        GPIO.output(op, (GPIO.LOW, GPIO.HIGH))
                else:
                        GPIO.output(op, (GPIO.HIGH, GPIO.LOW))
                        
                time.sleep(2)
                GPIO.output(op, (GPIO.LOW, GPIO.LOW))

finally:
        GPIO.cleanup()
