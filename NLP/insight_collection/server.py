from flask import Flask,Response
import json

from flask_cors import CORS


def read_insights(filename):
    with open("./outputs/" +filename, 'r') as file:
        data = json.load(file)
    return data
        

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	return 'Hello World'

@app.route('/aggregates/average_secondary_metrics')
def get_average_secondary_metrics():
    resp = Response()
    json_data = read_insights("average_secondary_metrics.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp

@app.route('/aggregates/votes_data')
def get_votes_data():
    resp = Response()
    json_data = read_insights("votes_aggregation.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp

@app.route('/aggregates/regionwise_rating')
def get_regionwise_rating():
    resp = Response()
    json_data = read_insights("regionwise_rating.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp


# main driver function
if __name__ == '__main__':
    
	# run() method of Flask class runs the application 
	# on the local development server.
    app.run()
