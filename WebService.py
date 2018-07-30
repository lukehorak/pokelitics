import sys
import LogParserLite as lp
import os

from flask import Flask, render_template, request, redirect, Response, jsonify
import random, json
from werkzeug import secure_filename

UPLOAD_DIRECTORY = 'data/'

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='name')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
    	f = request.files['file']
    	fpath = 'data/(1)' + secure_filename(f.filename)
    	f.save(fpath)
    	# Save result file as string
    	results = lp.main(fpath)
    	return render_template("results.html", result=results)


@app.route('/api/v01/parse', methods = ['GET', 'POST'])
def list_files():
	# Example data if "get"
	if request.method == 'GET':
		test_json = open(UPLOAD_DIRECTORY + 'test_results.json', "rb")
		files = []
		for filename in os.listdir(UPLOAD_DIRECTORY):
			path = os.path.join(UPLOAD_DIRECTORY, filename)
			if os.path.isfile(path):
				files.append(filename)
				return test_json.read()
	elif request.method == 'POST':
		f = request.files['test']
		fpath = 'data/(1)' + secure_filename(f.filename)
		f.save(fpath)
		# Save result file as string
		results = lp.main(fpath)
		print ("results-->", results)
		return str(results)


if __name__ == '__main__':
	# run!
	#app.run(host='0.0.0.0', debug=True, port=8000)
	app.run()
