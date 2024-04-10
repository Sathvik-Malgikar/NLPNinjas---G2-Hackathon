from flask import Flask
import json

def read_insights():
    global insights
    with open("insights.json", 'r') as file:
        insights = json.load(file)
        

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World'

# main driver function
if __name__ == '__main__':
    read_insights()
	# run() method of Flask class runs the application 
	# on the local development server.
    app.run()
