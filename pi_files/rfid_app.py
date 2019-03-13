#!/usr/bin/python3
import flask
from flask import request, jsonify, render_template
import RPi.GPIO as GPIO
import time
import requests
from pi_files import SimpleMFRC522
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

op = [35, 37]

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
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(op, GPIO.OUT)
	GPIO.output(op, (GPIO.HIGH, GPIO.LOW))

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
				GPIO.output(op, (GPIO.LOW, GPIO.HIGH))
				time.sleep(2)
				GPIO.output(op, (GPIO.LOW, GPIO.LOW))
				break
			else:
				print('failed')
		except Exception as e:
			count += 1
	return jsonify(resp)


@app.route('/startScan')
def start_scan():
	"""
	Runs continuously once called

	calls /match on server to compare bag and passenger id
	and prints result on lcd
	"""

	while True:
		# lcd out scan boarding pass
		# time.sleep(2)
		id1, pass_id = reader.read()

		# time.sleep(2)
		# lcd out scan bag
		id2, bag_id = reader.read()

		data = {'bagID': bag_id.strip(), 'passID': pass_id.strip()}

		resp = requests.post('http://127.0.0.1:5000/match', data=data)

		status = resp.json()
		if status['status']:
			# lcd out 'you may pass'
			pass
		else:
			# gandalf screams "YOU SHALL NOT PASS"
			pass
		time.sleep(5)


app.run(port=4020)
