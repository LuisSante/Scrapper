from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['GET'])
def execute_code():
    try:
        result = subprocess.run(["python", "scrapper_database/spiders/spider.py"], capture_output=True, text=True)

        return jsonify({
            'result': result.stderr,
            'error': result.stdout
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)