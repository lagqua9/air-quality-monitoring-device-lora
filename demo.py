from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# --- DATABASE FUNCTIONS ---
def insert_data(name, value):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data (name, value) VALUES (?, ?)", (name, value))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- ROUTES ---
@app.route('/')
def index():
    data = get_all_data()
    return render_template('index.html', data=data)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({'status': 'error', 'message': 'Thiếu dữ liệu'}), 400

    insert_data(data['name'], data['value'])
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
