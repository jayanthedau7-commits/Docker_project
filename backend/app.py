from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import pymongo

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

client = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)

db = client.test

collection = db['Flask_tutorial']

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')


def get_current_time_info():
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return day_of_week, current_time


@app.route('/')
def home():
    day_of_week, current_time = get_current_time_info()
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)


@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)
    
    # Task 2: Error handling with try/except
    try:
        # Basic validation check
        name = form_data.get('name', '').strip()
        email = form_data.get('email', '').strip()
        
        if not name or not email:
            raise ValueError("Name and Email fields cannot be empty!")
            
        # MongoDB insertion
        collection.insert_one(form_data)
        print("Data inserted successfully:", form_data)
        
        # Task 2: Redirect to dedicated success page
        return redirect(url_for('success'))
        
    except Exception as e:
        print(f"Error occurred during insertion: {e}")
        day_of_week, current_time = get_current_time_info()
        # Gracefully render error on the form page without redirecting
        return render_template(
            'index.html',
            day_of_week=day_of_week,
            current_time=current_time,
            error=f"Submission failed: {str(e)}",
            form_data=form_data
        ), 400


@app.route('/success')
def success():
    # Dedicated success template
    return render_template('success.html')


@app.route('/view')
def view():
    data = list(collection.find())

    for item in data:
        del item['_id']

    return {'data': data}


# Task 1: Flask '/api' endpoint that reads data from backend file and serves it as JSON
@app.route('/api')
def api():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to read data file: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)