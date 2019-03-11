import flask
from flask import request, jsonify, render_template
from case.model.dbconfig import clinkConnect
from case.model.dbconfig import clinkClose
import uuid
from case.model.query import Query
import hashlib
import base64

db = {
	'user' : 'root',
	'password' : '',
 	'host' : '127.0.0.1',
  	'database' : 'clink'
}

try:
	con = clinkConnect(db)
	cur = con.cursor()
	print("Connected")
except:
	print("Not Connected")

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def homepage():
	return render_template('index.html')


''''DEPARTURE'''

@app.route('/dept/gen/pid' , methods =['GET'])
def genUid():
	uid = uuid.uuid1()
	passDb = str(uuid.uuid3(uid,"caseLink").hex)
	passRfid = passDb								#requires hashing
	# render_template('.html' , passId = passRfid )	#passing passenger rfid to html
	return jsonify({'passRfid' : passRfid , 'passDb' : passDb})

@app.route('/dept/gen/bid' , methods =['GET'])
def genBagid():
	uid = uuid.uuid1()
	bagDb = str(uuid.uuid3(uid, "caseLink").hex)
	bagRfid = bagDb  								# requires hashing
	# render_template('.html', bagID = bagRfid)  		# passing bag rfid to html
	return jsonify({'bagRfid' : bagRfid , 'passDb' : bagDb})

@app.route('/dept/post/bagwt', methods = ["POST"])
#@app.route('/', methods = ["POST"])
def postBagWT():
	wt = request.form['weight']						#HTML input name="weight"
	#pdb = request.p['pdb']
	#bdb = request.p['bdb']
	#cur.execute(Query.addpassbags.format(pdb, bdb, wt))				#uploads passenger to databse
	cur.execute(Query.addpassbags.format("23","32",int(wt)))
	#return render_template('.html', wt= wt)

''''ARRIVAL'''
@app.route('/arr/match', methods = ["POST"])
def match(passID,bagID):
	cur.execute(Query.matchtag.format(passID,bagID))		#update after Hashing added
	if cur.rowcount == 0 :
		return False
	else:
		cur.execute(Query.delTag.format(passID, bagID))
		cur.execute(Query.UpColl.format(passID, bagID))
		return True

''''Table'''
@app.route('/populateTable')
def popTab():
	cur.execute(Query.gettable)
	data = cur.fetchall()
	return render_template('tags.html', data = data)			#add passenger details html

''''CLOSE'''
@app.route('/close')
def conClose():
	clinkClose(con)
	return("Closing")
app.run()