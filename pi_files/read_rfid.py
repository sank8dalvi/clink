
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
