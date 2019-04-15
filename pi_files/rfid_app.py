#!/usr/bin/python3
import flask
from flask import request, jsonify
import RPi.GPIO as GPIO
import time
import SimpleMFRC522
from flask_cors import CORS


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

reader = SimpleMFRC522.SimpleMFRC522()

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

	while count < 5:
		if count == 5:
			break

		print('waiting to write')
		try:
			id1, temp = reader.write(tag)
			resp['success'] = 0
			resp['id'] = id1

			print(tag, temp)
			break
		except Exception as e:
			count += 1
	
	return jsonify(resp)


@app.route('/readRfid')
def read_rfid():

	resp = {'success': -1}
	count = 0
	time.sleep(2)

	while count < 5:
		try:
			print('Waiting to read')
			id1, temp = reader.read()
			print(id1, temp)
			resp['success'] = 0
			resp['id'] = temp.strip()
			break
		except Exception as e:
			count += 1

	return jsonify(resp)


app.run(host='0.0.0.0')

