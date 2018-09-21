from flask import Flask
from flask import request
import pymongo
import json
import time
from bson import BSON
from bson import json_util

app = Flask(__name__)

mongo = pymongo.MongoClient('mongodb://sergio:Mongo123@cluster0-shard-00-00-aebc3.gcp.mongodb.net:27017,cluster0-shard-00-01-aebc3.gcp.mongodb.net:27017,cluster0-shard-00-02-aebc3.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true', maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'arqui_usac')
col = pymongo.collection.Collection(db, 'garage')
colpass = pymongo.collection.Collection(db, 'pass')

@app.route('/<pass_ins>',methods=['GET','POST'])
def hola_mundo(pass_ins=None): 
	if request.method=='POST':
		var = request.form['operacion']
		if var=="1":
			nueva=request.form['password']
			colpass.find_one_and_replace({'user':'root'},{'password':nueva})
			pass
		else:
			last=''
			json_val='{ "datos":[ '
			for reg in col.find():
	   			json_val+=json.dumps(reg,sort_keys=True, indent=4, default=json_util.default)
	   			json_val=json_val+',\n'
	   			last=json.dumps(reg,sort_keys=True, indent=4, default=json_util.default)
	   		json_val=json_val+str(last)
	   		json_val=json_val+']}'

			return json_val

	if request.method=='GET':
		consulta=colpass.find_one();
		print consulta['password']
		print pass_ins
		print "fin"
		#pass_ins=request.form['password']
		if consulta['password']==pass_ins:
			reg_ins={
				"State":"correct",
				"Date":time.strftime("%H:%M:%S"),
				"Time":time.strftime("%d/%m/%y")}
			col.insert_one(reg_ins).inserted_id	
			return "1"
			pass
		else:
			reg_ins={
				"State":"incorrect",
				"Date":time.strftime("%H:%M:%S"),
				"Time":time.strftime("%d/%m/%y")}
			col.insert_one(reg_ins).inserted_id	
			return "0"
		pass
	print "f"
	return 'Nuevo Pass'


if __name__ == '__main__': 
	app.run(debug="True")
