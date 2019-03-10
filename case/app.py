import flask
from flask import request, jsonify, render_template
from case.DB.dbcon import Connect
import uuid
from case.DB.query import Query
import hashlib

global con

db = {
	'user' : 'root',
	'password' : '',
 	'host' : '127.0.0.1',
  	'database' : 'clink'
}

try:
	con = Connect.clinkConnect(db)
	cur = con.cursor()
	print("Connected")
except:
	print("")

app = flask.Flask(__name__)
app.config["DEBUG"] = True

class Departure:
	global passDb, bagDb

	@app.route('/dept/gen/pid' , methods =['GET'])
	def genUid(self):
		uid = uuid.uuid1()
		passDb = str(uuid.uuid3(uid,"caseLink").hex)
		passRfid = passDb								#requires hashing
		render_template('.html' , passId = passRfid )	#passing passenger rfid to html
		return passRfid

	@app.route('/dept/gen/bid' , methods =['GET'])
	def genBagid(self):
		uid = uuid.uuid1()
		bagDb = str(uuid.uuid3(uid, "caseLink").hex)
		bagRfid = bagDb  								# requires hashing
		render_template('.html', bagID = bagRfid)  		# passing bag rfid to html
		return bagRfid

	@app.route('/dept/post/bagwt', methods = ["POST"])
	def postBagWT(self):
		wt = request.form['weight']						#HTML input name="weight"
		cur.execute(Query.addpassbags.format(passDb, bagDb, wt))				#uploads passenger to databse


class Arrival:
	@app.route('/arr/match', methods = ["POST"])
	def match(self,passID,bagID):
		cur.execute(Query.matchtag.format(passID,bagID))		#update after Hashing added
		if cur.rowcount == 0 :
			return False
		else:
			cur.execute(Query.delTag.format(passID, bagID))
			cur.execute(Query.UpColl.format(passID, bagID))
			return True


class UI:
	''''Table'''
	@app.route('/populateTable')
	def popTab():
		cur.execute(Query.gettable)
		data = cur.fetchall()
		render_template('.html', data = data)			#add passenger details html


app.run()