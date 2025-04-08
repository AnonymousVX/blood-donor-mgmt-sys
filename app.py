
# IPv4-only DNS fix
import socket
orig_getaddrinfo = socket.getaddrinfo
def ipv4_only_getaddrinfo(*args, **kwargs):
    return [ai for ai in orig_getaddrinfo(*args, **kwargs) if ai[0] == socket.AF_INET]
socket.getaddrinfo = ipv4_only_getaddrinfo

# Flask + PostgreSQL
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

# Flask app setup
app = Flask(__name__)
CORS(app)

# Supabase PostgreSQL DB credentials (IPv4-Compatible Host)
DB_HOST = 'aws-0-ap-south-1.pooler.supabase.com'
DB_NAME = 'postgres'
DB_USER = 'postgres.aabrngetuhjtiwzbpxyu'
DB_PASSWORD = 'VEDANTrj@0016'
DB_PORT = '5432'

# Connect to Supabase PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    print("✅ Database connection established.")
except Exception as e:
    print("❌ Database connection failed:", e)
    exit(1)

# -------------------- ROUTES -------------------- #

@app.route('/')
def home():
    return "🩸 Blood Donor Management System API is running."

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    bloodgroup = data.get('bloodgroup')
    contact = data.get('contact')
    city = data.get('city')

    if not all([name, age, gender, bloodgroup, contact, city]):
        return jsonify({"error": "Please fill all fields."}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO donors (name, age, gender, bloodgroup, contact, city)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, age, gender, bloodgroup, contact, city))
        conn.commit()
        return jsonify({"message": "✅ Donor registered successfully!"}), 201

    except Exception as e:
        conn.rollback()  # Important: reset failed transaction state
        print("Database error:", e)
        return jsonify({"error": "❌ Something went wrong."}), 500

@app.route('/donors', methods=['GET'])
def get_donors():
    city = request.args.get('city')
    try:
        with conn.cursor() as cur:
            if city:
                cur.execute("SELECT * FROM donors WHERE city = %s", (city,))
            else:
                cur.execute("SELECT * FROM donors")
            donors = cur.fetchall()

        donor_list = [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "bloodgroup": row[4],
                "contact": row[5],
                "city": row[6]
            } for row in donors
        ]
        return jsonify(donor_list)

    except Exception as e:
        conn.rollback()
        print("Error fetching donors:", e)
        return jsonify({"error": "Failed to fetch donors."}), 500

@app.route('/api/cities')
def get_cities():
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT city FROM donors ORDER BY city;")
            rows = cur.fetchall()
        cities = [row[0] for row in rows]
        return jsonify(cities)

    except Exception as e:
        conn.rollback()
        print("Error fetching cities:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/donors')
def get_donors_by_city():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not provided"}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name, bloodgroup, contact FROM donors WHERE city = %s", (city,))
            donors = cur.fetchall()

        donor_list = [
            {"name": d[0], "bloodgroup": d[1], "contact": d[2]}
            for d in donors
        ]
        return jsonify(donor_list)

    except Exception as e:
        conn.rollback()
        print("Error fetching city donors:", e)
        return jsonify({"error": str(e)}), 500

# -------------------- MAIN -------------------- #

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)  # already done

# Add this at the end:
if __name__ == "__main__":
    app.run()
