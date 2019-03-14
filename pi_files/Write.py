#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
        text = raw_input('New data:')
        print("Now place your tag to write")
        id, t = reader.write(text)
        print("Written")
	print(id)
	print(t)
finally:
        GPIO.cleanup()

