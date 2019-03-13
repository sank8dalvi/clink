#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time
import Adafruit_CharLCD as LCD


lcd_rs = 5
lcd_en = 6
lcd_d4 = 26
lcd_d5 = 20
lcd_d6 = 21
lcd_d7 = 16
lcd_backlight = 2
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

lcd.message('Welcome')
time.sleep(1)
GPIO.cleanup()

try:
        reader = SimpleMFRC522.SimpleMFRC522()
        id, text = reader.read()
        GPIO.cleanup()
        print(id)
        print(text)
        GPIO.setmode(GPIO.BCM)
        lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
        lcd.message(text[:16] + '\n' + text[16:])
finally:
        GPIO.cleanup()



##lcd.message('Hello\nworld!')
### Wait 5 seconds
##
##time.sleep(5.0)
##lcd.clear()
##text = raw_input("Type Something to be displayed: ")
##lcd.message(text)
##
### Wait 5 seconds
##time.sleep(5.0)
##lcd.clear()
##lcd.message('Goodbye\nWorld!')
##
##time.sleep(5.0)
##lcd.clear()
