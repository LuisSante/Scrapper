from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
CORS(app)

def run_spider():
    result = subprocess.run(["python", "scrapper_database/spiders/spider.py"], capture_output=True, text=True)
    output = result.stderr
    # print(output)
    print(f"Spider executed at {datetime.now()}")

# end_date = datetime.now() + timedelta(days=2)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(run_spider, 'interval', minutes=1)
# scheduler.add_job(run_spider, 'interval', end_date=end_date)

scheduler.start()

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        return jsonify({
            'result': 'Scheduler is running to execute the spider every 2 minutes.',
            'additional_info': ''
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

