from flask import Flask, render_template,jsonify,request
import sqlite3
app = Flask(__name__)

DB_PATH = 'database.db'#đường dẫn đến file cơ sở dữ liệu
#hàm định nghĩa db
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rows[0] if rows else None) if one else rows

# phần này sẽ hỏi ng dùng cấp quyền vị trí (demo)
@app.route('/send_location', methods=['POST'])
def get_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    print(f"Vị trí người dùng: {latitude}, {longitude}")
    return jsonify({'status': 'received'})
# 

#hàm GET lấy ra các nodes
@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT ID, LOCATION, TIME, DATE FROM nodes")#thêm dữ liệu cột
    rows = cursor.fetchall()
    conn.close()

    # Chuyển dữ liệu thành JSON
    nodes = []
    for row in rows:
        nodes.append({
            'id': row[0],
            'location': row[1],
            'time': row[2],
            'date': row[3]
            #thêm một cột nx ở đây
        })

    return jsonify(nodes)
#
#lấy ra 1 id
@app.route('/api/nodes/<int:id>', methods=['GET'])
def get_node(id):
    row = query_db("SELECT ID, LOCATION, TIME FROM nodes WHERE ID = ?", (id,), one=True)
    if row:
        return jsonify({'id': row[0], 'location': row[1], 'time': row[2]})
    return jsonify({'error': 'Node not found'}), 404

#
#Hàm PUT
# Cập nhật node theo ID
@app.route('/api/nodes/<int:id>', methods=['PUT'])
def update_node(id):
    data = request.get_json()
    location = data.get('location')
    time = data.get('time')

    row = query_db("SELECT * FROM nodes WHERE ID = ?", (id,), one=True)
    if not row:
        return jsonify({'error': 'Node not found'}), 404

    query_db("UPDATE nodes SET LOCATION = ?, TIME = ? WHERE ID = ?", (location, time, id))
    return jsonify({'message': 'Node updated'})
#
#hàm POST
@app.route('/api/nodes_post', methods=['POST'])
def create_node():
    data = request.get_json()
    location = data.get('location')
    time = data.get('time')
    date = data.get('date')

    if not location or not time or not date:
        return jsonify({'error': 'Missing data'}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nodes (LOCATION, TIME, DATE) VALUES (?, ?, ?)", (location, time, date))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Node created'}), 201
#
# hàm DELETE
# --- API xoá node ---
@app.route('/api/nodes/<int:id>', methods=['DELETE'])
def delete_node(id):
    row = query_db("SELECT * FROM nodes WHERE ID = ?", (id,), one=True)
    if not row:
        return jsonify({'error': 'Node not found'}), 404

    query_db("DELETE FROM nodes WHERE ID = ?", (id,))
    return jsonify({'message': 'Node deleted'})
#

@app.route('/')
def index():
    return render_template('index.html')  # chỉ hiển thị giao diện
@app.route('/login')
def about():
    return render_template('login.html')  # Trang phụ
# đoạn này sẽ dẫn đến trang muốn

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
