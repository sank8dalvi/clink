#!/usr/bin/python3
import flask
from flask import request, jsonify, render_template
import RPi.GPIO as GPIO
import time
import requests
import SimpleMFRC522
from flask_cors import CORS
import importlib


app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

op = [35, 37]

lcd_rs = 5
lcd_en = 6
lcd_d4 = 26
lcd_d5 = 20
lcd_d6 = 21
lcd_d7 = 16
lcd_backlight = 2
lcd_columns = 16
lcd_rows = 2



@app.route('/writeRfid', methods=['POST'])
def write_rfid():
	"""
	Called by web to write on the rfid card


	success : 	-1 if failed to write, 0 if succeeded to write
	id : id of the rfid card if write succeeds
	"""

	tag = request.form['id']  # tag to be written
	resp = {'success': -1}
	count = 0

	GPIO.cleanup()
	reader = SimpleMFRC522.SimpleMFRC522()

	# this loop isn't perfect
	while True:
		if count == 5:
			break

		print('waiting to write')
		try:
			id1, temp = reader.write(tag)
			print('confirm')
			id2, data = reader.read()
			if data.strip() == tag and id1 == id2:
				resp['success'] = 0
				resp['id'] = id2
				time.sleep(2)		
				break
			else:
				print('failed')
		except Exception as e:
			count += 1
	GPIO.cleanup()
	
	return jsonify(resp)


def printLCD(text):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        import Adafruit_CharLCD as LCD
        lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

        lcd.message(text)
        time.sleep(1)
        GPIO.cleanup()


@app.route('/readRfid')
def read_rfid():
	reader = SimpleMFRC522.SimpleMFRC522()
	resp = {'success': -1}
	count = 0
	while True:
		if count == 5:
			break

		print('waiting to write')
		try:
			id1, temp = reader.read()
			print('confirm')
			id2, data = reader.read()
			if id1 == id2:
				resp['success'] = 0
				resp['id'] = data
				break
			else:
				print('failed')
		except:
			count += 1
	GPIO.cleanup()

	return jsonify(resp)


@app.route('/startScan')
def start_scan():
	"""
	Runs continuously once called

	calls /match on server to compare bag and passenger id
	and prints result on lcd
	"""

	server = 'http://192.168.1.35:5000/'

	while True:
		# print scan pass
		try:
			requests.post(server + 'arr/extract', data={'title': "Scan CaseLink Card", 'code': 0})
			reader = SimpleMFRC522.SimpleMFRC522()
			id1, pass_id = reader.read()
			print("Read pass", pass_id)

			requests.post(server + 'arr/extract', data={'title': "Scan CaseLink Tag", 'code': 1})
			time.sleep(1.5)
			# lcd out scan bag
			printLCD("Scan bag")
			print("Scan bag")
			reader = SimpleMFRC522.SimpleMFRC522()
			id2, bag_id = reader.read()
			print("Read bag", bag_id)

			data = {'bagID': bag_id.strip(), 'passID': pass_id.strip()}
			print(data)
			resp = requests.post(server + 'arr/match', data=data)

			status = resp.json()
			print(status)
			if status['status']:
				# lcd out 'you may pass'
				printLCD('you may pass')
			else:
				# gandalf screams "YOU SHALL NOT PASS"
				printLCD("YOU SHALL\nNOT PASS")
			time.sleep(3)
		except:
			print("error occurred")
			pass




# GPIO.cleanup()
	# while True:
	# 	# lcd out scan boarding pass
	# 	print("Scan pass")
	# 	printLCD("Scan pass")
	# 	reader = SimpleMFRC522.SimpleMFRC522()
	# 	id1, pass_id = reader.read()
	#
	# 	print("Read pass", pass_id)
	#
	# 	time.sleep(2)
	# 	# lcd out scan bag
	# 	printLCD("Scan bag")
	# 	print("Scan bag")
	# 	reader = SimpleMFRC522.SimpleMFRC522()
	# 	id2, bag_id = reader.read()
	# 	print("Read bag", bag_id)
	#
	# 	data = {'bagID': bag_id.strip(), 'passID': pass_id.strip()}
	# 	print(data)
	# 	resp = requests.post('http://192.168.1.35:5000/arr/match', data=data)
	# 	# print(resp.text)
	# 	status = resp.json()
	# 	print(status)
	# 	if status['status']:
	# 		# lcd out 'you may pass'
	# 		printLCD('you may pass')
	# 	else:
	# 		# gandalf screams "YOU SHALL NOT PASS"
	# 		printLCD("YOU SHALL\nNOT PASS")
	# 	time.sleep(5)



app.run(host='0.0.0.0')

