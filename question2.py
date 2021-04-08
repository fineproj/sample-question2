import flask
from flask import request,jsonify
import requests
import json
from datetime import datetime
from time import strftime,gmtime

app = flask.Flask(__name__)
app.config["DEBUG"] = True
time_format = "%Y-%m-%dT%H:%M:%SZ"

url = 'https://gitlab.com/-/snippets/2094509/raw/master/sample_json_2.json'
r = requests.get(url)
data = r.content
system_data = json.loads(data)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Home</h1>"

@app.route('/api/produnit/all', methods=['GET'])
def api_all():
    return jsonify(system_data)

@app.route('/api/produnit', methods=['GET'])
def api_time():
    if 'start_time'in request.args:
        start_time = datetime.strptime(str(request.args['start_time']),time_format)
    
    if 'end_time'in request.args:
        end_time = datetime.strptime(str(request.args['end_time']),time_format)

    result = {}

    runtime = 0
    downtime = 0

    for data in system_data:
        current_time = datetime.strptime(str(data['time']),"%Y-%m-%d %H:%M:%S")      
        if(start_time <= current_time <= end_time):
            if runtime<=1021:
                runtime = runtime + data['runtime']
            else:
                downtime = downtime + data['runtime']

    
    utilisation = round((runtime/(runtime + downtime)) * 100,2)
    runtime = strftime('%Hh:%Mm:%Ss',gmtime(runtime))
    downtime = strftime('%Hh:%Mm:%Ss',gmtime(downtime))

    result['runtime'] = runtime
    result['downtime'] = downtime
    result['utilisation'] = utilisation


    return jsonify(result)
app.run()

