from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

import subprocess
import os
import json
import pandas as pd

app = Flask(__name__)
CORS(app)

def run_spider():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    jsonl_file_path = os.path.join(current_dir, 'current.jsonl')

    with open(jsonl_file_path, 'w') as file:
        file.write('')

    # result = subprocess.run(["scrapy", "runspider" , "scrapper_database/spiders/spider.py"], capture_output=True, text=True)
    result = subprocess.run(["scrapy", "runspider" , "scrapper_database/spiders/current.py", "-o" , "current.jsonl"], capture_output=True, text=True)
    output = result.stderr

    print(output)

    json_data = []
    with open(jsonl_file_path, 'r' , encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            json_object = json.loads(line)
            json_data.append(json_object)

    print(f"Spider executed at {datetime.now()}")

    return json_data

# end_date = datetime.now() + timedelta(days=2) # Descomentar para la prueba de 2 dias

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(run_spider, 'interval', minutes=1)
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

