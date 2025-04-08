
import socket
socket.getaddrinfo = lambda *args, **kwargs: [
    ai for ai in socket.__dict__['getaddrinfo'](*args, **kwargs)
    if ai[0] == socket.AF_INET
]

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

# Flask setup
app = Flask(__name__)
CORS(app)

# Supabase REST config

SUPABASE_URL = 'https://aabrngetuhjtiwzbpxyu.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhYnJuZ2V0dWhqdGl3emJweHl1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwNTI3MDgsImV4cCI6MjA1OTYyODcwOH0.bV9xzubVfIJDomKkevaDCdbt-3xug3gjfHk4OP0JT6M'

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

@app.route('/')
def home():
    return "🩸 Blood Donor Management System API is running."

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    required = ['name', 'age', 'gender', 'bloodgroup', 'contact', 'city']
    if not all(data.get(field) for field in required):
        return jsonify({"error": "Please fill all fields."}), 400

    try:
        res = requests.post(f"{SUPABASE_URL}/rest/v1/donors", headers=HEADERS, json=data)
        if res.status_code in [200, 201]:
            return jsonify({"message": "✅ Donor registered successfully!"}), 201
        return jsonify({"error": res.json()}), res.status_code

    except Exception as e:
        print("Supabase error:", e)
        return jsonify({"error": "❌ Registration failed."}), 500

@app.route('/donors', methods=['GET'])
def get_donors():
    city = request.args.get('city')
    query = f"?city=eq.{city}" if city else ""
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/donors{query}", headers=HEADERS)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cities')
def get_cities():
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/donors?select=city", headers=HEADERS)
        cities = sorted({d['city'] for d in res.json() if d.get('city')})
        return jsonify(cities)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/donors')
def get_donors_by_city():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not provided"}), 400
    try:
        res = requests.get(
            f"{SUPABASE_URL}/rest/v1/donors?city=eq.{city}&select=name,bloodgroup,contact",
            headers=HEADERS
        )
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
