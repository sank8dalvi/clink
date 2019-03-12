import flask
from flask import request, jsonify, render_template, url_for
from case.model.dbconfig import clinkConnect
from case.model.dbconfig import clinkClose
import uuid
from case.model.query import Query

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

'''DASHBOARD Data'''
def getPassCount():
	cur.execute(Query.getPassCount)
	return (cur.fetchall()[0][0])

def getBagCount():
	cur.execute(Query.getBagCount)
	return (cur.fetchall()[0][0])

getPassCount()
getBagCount()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def homepage():
	return render_template('index.html',bagCount = getBagCount(), passCount = getPassCount())


''''DEPARTURE'''
@app.route('/dept/gen/pid' , methods =['GET'])
def genUid():
	uid = uuid.uuid1()
	passRfid = uuid.uuid3(uid,"caseLink")
	passDb = str(uuid.uuid5(passRfid,"caseLink").hex)
	passRfid = str(passRfid.hex)
	# render_template('.html' , passId = passRfid, bagCount = getBagCount(), passCount = getPassCount)	#passing passenger rfid to html
	return jsonify({'passRfid' : passRfid , 'passDb' : passDb})

@app.route('/dept/gen/bid' , methods =['GET'])
def genBagid():
	uid = uuid.uuid1()
	bagRfid = uuid.uuid3(uid, "caseLink")
	bagDb = str(uuid.uuid5(bagRfid,"caseLink").hex)
	bagRfid = str(bagRfid.hex)
	# render_template('.html', bagID = bagRfid, bagCount = getBagCount(), passCount = getPassCount)  		# passing bag rfid to html
	return jsonify({'bagRfid' : bagRfid , 'passDb' : bagDb})

@app.route('/dept/post/bagwt', methods = ["POST"])
#@app.route('/', methods = ["POST"])
def postBagWT():
	wt = request.form['weight']						#HTML input name="weight"
	#pdb = request.p['pdb']
	#bdb = request.p['bdb']
	#cur.execute(Query.addpassbags.format(pdb, bdb, wt))				#uploads passenger to databse
	cur.execute(Query.addpassbags.format("23","32",int(wt)))
	#return render_template('.html', wt= wt, bagCount = getBagCount(), passCount = getPassCount)

''''ARRIVAL'''
@app.route('/arr/match', methods = ["POST"])
def match():
	bagID = request.args.get('bagID','')
	passID = request.args.get('passID', '')
	bagID = str(uuid.uuid5(uuid.UUID(bagID), "caseLink").hex)
	passID = str(uuid.uuid5(uuid.UUID(passID), "caseLink").hex)
	cur.execute(Query.matchtag.format(passID,bagID))
	if cur.rowcount == 0 :
		return False
	else:
		cur.execute(Query.delTag.format(passID, bagID))
		cur.execute(Query.UpColl.format(passID, bagID))
		return True

''''Table'''
@app.route('/popBagTable')										#All bags from db
def popBagTab():
	cur.execute(Query.gettable)
	data = cur.fetchall()
	return render_template('tags.html', data = data, bagCount = getBagCount(), passCount = getPassCount())			#add bag details html

@app.route('/popPassTable')										#Current passenger bags + on add bags page
def popPassTab():
	cur.execute(Query.getbags)
	bags = cur.fetchall()
	#return render_template('.html', bags = bags, bagCount = getBagCount(), passCount = getPassCount())			#add passenger details html

''''CLOSE'''
@app.route('/close')
def conClose():
	clinkClose(con)
	return("Closing")
app.run()