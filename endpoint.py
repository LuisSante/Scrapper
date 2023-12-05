from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

import subprocess
import ast
import re
import pandas as pd

app = Flask(__name__)
CORS(app)

def convert_json(output):
    pattern = re.compile(r'{[^}]*}')
    matches = pattern.findall(output)
    matches = [match.replace("“", "") for match in matches]
    matches = [match.replace("”", "") for match in matches]
    matches = [match.replace("\"", "\'") for match in matches]
    matches = [match.replace("’", "'") for match in matches]
    matches = [match.replace("'m", " am") for match in matches]
    matches = [match.replace("'re", " are") for match in matches]
    matches = [match.replace("'s", " is") for match in matches]
    matches = [match.replace("'ve", " have") for match in matches]
    matches = [match.replace("n't", "nt") for match in matches]
    matches = [match.replace("'d", " did") for match in matches]
    matches = [match.replace("'ll", " will") for match in matches]
    
    matches = matches[1:-1]

    return matches

def run_spider():
    result = subprocess.run(["python", "scrapper_database/spiders/current.py"], capture_output=True, text=True)
    output = result.stderr
    matches = convert_json(output)

    json_objects = [ast.literal_eval(match) for match in matches]

    print(f"Spider executed at {datetime.now()}")

    return json_objects

# end_date = datetime.now() + timedelta(days=2) # Descomentar para la prueba de 2 dias

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(run_spider, 'interval', minutes=10)
# scheduler.add_job(run_spider, 'interval', end_date=end_date) # Complemento de linea 40

scheduler.start()

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        return jsonify({
            'result': run_spider(),
            'additional_info': ''
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

