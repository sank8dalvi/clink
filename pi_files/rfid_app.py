#!/usr/bin/python3
import flask
from flask import request, jsonify, render_template
import RPi.GPIO as GPIO
import SimpleMFRC522
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

op = [35, 37]

reader = SimpleMFRC522.SimpleMFRC522()

@app.route('/')
def homepage():
    return 'hello_world'

@app.route('/writeRfid', methods=['POST'])
def writeRfid():
    tag = request.form['id'] #tag to be written
    resp = {'success' : -1}
    count = 0
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(op, GPIO.OUT)
    GPIO.output(op, (GPIO.HIGH, GPIO.LOW))
    while True:
        if count == 5:
            break
        
        print('waiting to write')
        try:
            __, temp = reader.write(tag)
            print('confirm')
            _, data = reader.read()
            if data.strip() == tag and __ == _ :
                resp['success'] = 0
                GPIO.output(op, (GPIO.LOW, GPIO.HIGH))
                time.sleep(2)
                GPIO.output(op, (GPIO.LOW, GPIO.LOW))
                break
            else:
                print('failed')
        except Exception as e:
            count += 1
    return jsonify(resp)
    

app.run(port=4020)
##
##try:
##        text = input('New data:')
##        print("Now place your tag to write")
##        reader.write(text)
##        print("Written")
##         
##        while True:
##                _, prompt = reader.read()
##                
##                GPIO.setmode(GPIO.BOARD)
##                GPIO.setup(op, GPIO.OUT)
##                
##                if prompt.strip() == text:
##                        GPIO.output(op, (GPIO.LOW, GPIO.HIGH))
##                else:
##                        GPIO.output(op, (GPIO.HIGH, GPIO.LOW))
##                        
##                time.sleep(2)
##                GPIO.output(op, (GPIO.LOW, GPIO.LOW))
##
##finally:
##        GPIO.cleanup()
