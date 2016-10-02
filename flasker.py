from flask import Flask, request, jsonify
from imageSearch_1 import *


app = Flask(__name__)

@app.route('/<string:query>', methods=['GET'])
def index(query):
	return jsonify(mainToRun(query))

if __name__ == "__main__":
	app.run(debug=True, port=8080)