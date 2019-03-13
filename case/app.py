import flask
from flask import request, jsonify, render_template, url_for
from case.model.dbconfig import clinkConnect
from case.model.dbconfig import clinkClose
import uuid
from case.model.query import Query
from flask_cors import CORS

db = {
	'user': 'root',
	'password': '',
	'host': '127.0.0.1',
	'database': 'clink'
}

try:
	con = clinkConnect(db)
	cur = con.cursor()
	print("Connected")
except:
	print("Not Connected")

'''DASHBOARD Data'''


def get_pass_count():
	cur.execute(Query.getPassCount)
	return cur.fetchall()[0][0]


def get_bag_count():
	cur.execute(Query.getBagCount)
	return cur.fetchall()[0][0]


app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/')
def homepage():
	return render_template('home.html', bagCount=get_bag_count(), passCount=get_pass_count())


''''DEPARTURE'''


@app.route('/dept/gen/pid', methods=['GET'])
def gen_uid():
	uid = uuid.uuid1()
	passRfid = uuid.uuid3(uid, "caseLink")
	passDb = str(uuid.uuid5(passRfid, "caseLink").hex)
	passRfid = str(passRfid.hex)
	return jsonify({'passRfid': passRfid, 'passDb': passDb})


# write Rfid Page
@app.route('/dept/gen/idwrite')
def call_write_read():
	resp = flask.make_response(render_template('write-read.html', status = "Please Scan Tag",
						   bagCount=get_bag_count(), passCount=get_pass_count()))

	tempId = gen_uid().json
	print(tempId)
	resp.set_cookie("passDb",  tempId['passDb'])
	resp.set_cookie("passRfid", tempId['passRfid'])


	return resp


# read Rfid Page	add delay should try to use JS and modify status directly
@app.route('/dept/gen/idread')
def pid_written():
	return render_template('write-read.html',
						   status="Tag Scanned Successfully",
						   bagCount=get_bag_count(),
						   passCount=get_pass_count())


@app.route('/dept/gen/bid', methods=['GET'])
def gen_bag_id():
	uid = uuid.uuid1()
	bagRfid = uuid.uuid3(uid, "caseLink")
	bagDb = str(uuid.uuid5(bagRfid, "caseLink").hex)
	bagRfid = str(bagRfid.hex)
	# render_template('.html', bagID = bagRfid, bagCount = getBagCount(), passCount = getPassCount)
	return jsonify({'bagRfid': bagRfid, 'bagDb': bagDb})


''' todo check how values are passing. API needs passenger and Bag db IDs'''


@app.route('/dept/post/bagwt', methods=["POST"])
def post_bag_wt():
	wt = request.form['weight']
	pdb = str(request.cookies.get('passId'))
	bdb = str(request.cookies.get('bagId'))
	#print(Query.addpassbags.format(pdb, bdb, int(wt)))
	cur.execute(Query.addpassbags.format(pdb, bdb, int(wt)))
	con.commit()

	cur.execute(Query.getbags.format(pdb))
	bags = cur.fetchall()

	return render_template('addBags.html', data=bags, bagCount=get_bag_count(), passCount=get_pass_count())


''''ARRIVAL'''


@app.route('/arr/match', methods=["POST"])
def match():
	# piInputs
	bagID = request.form['bagID']
	passID = request.form['passID']
	print(bagID, passID)
	bagID = str(uuid.uuid5(uuid.UUID(bagID), "caseLink").hex)
	passID = str(uuid.uuid5(uuid.UUID(passID), "caseLink").hex)
	print(bagID, passID)
	cur.execute(Query.matchtag.format(passID, bagID))
	data = cur.fetchall()
	resp = {}
	if len(data) == 0:
		resp['status'] = False
	else:
		# todo row count
		print(data)
		cur.execute(Query.delTag.format(passID, bagID))
		cur.execute(Query.UpColl.format(passID, bagID, data[0][3]))
		con.commit()
		resp['status'] = True

	return jsonify(resp)


''''Table'''


@app.route('/popBagTable')  # All bags from db
def pop_bag_tab():
	passID = request.args.get('passID', '')  # piInput
	cur.execute(Query.gettable.format(passID))
	data = cur.fetchall()
	return render_template('tags.html',
						   data=data,
						   bagCount=get_bag_count(),
						   passCount=get_pass_count())  # add bag details html


@app.route('/AddBags')  # Current passenger bags + on add bags page
def pop_add_bag_tab():
	# passID = request.args.get('passID','')				#piInput
	cur.execute(Query.getbags.format(request.cookies.get('passDb')))
	bags = cur.fetchall()
	print(request.cookies.get('passDb'))
	return render_template('addBags.html',
						   data=bags,
						   bagCount=get_bag_count(),
						   passCount=get_pass_count())  # add passenger details html


''''CLOSE CONN'''


@app.route('/close')
def con_close():
	clinkClose(con)
	return "Closing"


app.run(host='0.0.0.0')
