from flask import Flask, render_template,jsonify,request
import sqlite3
app = Flask(__name__)

DB_PATH = 'database.db'#đường dẫn đến file cơ sở dữ liệu
#hàm định nghĩa db
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH, timeout = 10)
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

    cursor.execute("SELECT ID, LOCATION, TIME, DATE, LAT, LONG FROM nodes")#thêm dữ liệu cột
    rows = cursor.fetchall()
    conn.close()

    # Chuyển dữ liệu thành JSON
    nodes = []
    for row in rows:
        nodes.append({
            'id': row[0],
            'location': row[1],
            'time': row[2],
            'date': row[3],
            'lat': row[4],
            'long': row[5]
            #thêm một cột nx ở đây
        })

    return jsonify(nodes)
#
# GETlấy ra 1 id
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
    date = data.get('date')
    lat = data.get('lat')
    long = data.get('long')
    row = query_db("SELECT * FROM nodes WHERE ID = ?", (id,), one=True)
    if not row:
        return jsonify({'error': 'Node not found'}), 404

    query_db("UPDATE nodes SET LOCATION = ?, TIME = ?, DATE = ?, LAT = ?, LONG = ? WHERE ID = ?", (location, time, id, date, lat, long))
    return jsonify({'message': 'Node updated'})
#
#hàm POST
@app.route('/api/nodes_post', methods=['POST'])
def create_node():
    data = request.get_json()
    location = data.get('location')
    time = data.get('time')
    date = data.get('date')
    lat = data.get('lat')
    long = data.get('long')

    if not location or not time or not date:
        return jsonify({'error': 'Missing data'}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nodes (LOCATION, TIME, DATE, LAT, LONG) VALUES (?, ?, ?, ?, ?)", (location, time, date, lat, long))
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

# API PUT để cập nhật bảng slaves
@app.route('/update_slave/<int:id>', methods=['PUT'])
def update_slave(id):
    # Lấy dữ liệu từ request (yêu cầu client gửi dữ liệu JSON)
    data = request.get_json()

    node_id = data.get('NODE_ID')
    sensor_temp = data.get('SENSOR_TEMP')
    sensor_humi = data.get('SENSOR_HUMI')
    sensor_co = data.get('SENSOR_CO')
    pm_2_5 = data.get('PM_2_5')
    time = data.get('TIME')
    date = data.get('DATE')

    # Cập nhật dữ liệu vào bảng slaves
    query = """
        UPDATE slaves
        SET NODE_ID = ?, SENSOR_TEMP = ?, SENSOR_HUMI = ?, SENSOR_CO = ?, PM_2_5 = ?, TIME = ?, DATE = ?
        WHERE ID = ?
    """
    query_db(query, (node_id, sensor_temp, sensor_humi, sensor_co, pm_2_5, time, date, id))
    
    return jsonify({"message": "Data updated successfully"}), 200

# API GET để lấy dữ liệu của một slave theo ID
@app.route('/api/slave/<int:id>', methods=['GET'])
def get_slave(id):
    # Truy vấn dữ liệu từ bảng slaves theo ID
    query = "SELECT * FROM slaves WHERE ID = ?"
    row = query_db(query, [id], one=True)

    # Kiểm tra xem có dữ liệu không
    if row is None:
        return jsonify({"message": "Slave not found"}), 404
    
    # Chuyển kết quả thành JSON
    slave_data = {
        "ID": row[0],
        "NODE_ID": row[1],
        "SENSOR_TEMP": row[2],
        "SENSOR_HUMI": row[3],
        "SENSOR_CO": row[4],
        "PM_2_5": row[5],
        "TIME": row[6],
        "DATE": row[7]
    }

    return jsonify(slave_data), 200

# API GET để lấy tất cả dữ liệu từ bảng slaves
@app.route('/api/slaves', methods=['GET'])
def get_all_slaves():
    # Truy vấn tất cả dữ liệu từ bảng slaves
    query = "SELECT * FROM slaves"
    rows = query_db(query)

    # Nếu không có dữ liệu trong bảng
    if not rows:
        return jsonify({"message": "No slaves found"}), 404

    # Chuyển tất cả các kết quả thành JSON
    all_slaves = []
    for row in rows:
        slave_data = {
            "ID": row[0],
            "NODE_ID": row[1],
            "SENSOR_TEMP": row[2],
            "SENSOR_HUMI": row[3],
            "SENSOR_CO": row[4],
            "PM_2_5": row[5],
            "TIME": row[6],
            "DATE": row[7]
        }
        all_slaves.append(slave_data)

    return jsonify(all_slaves), 200
#
# API POST để thêm dữ liệu vào bảng slaves
@app.route('/api/add_slave', methods=['POST'])
def add_slave():
    # Lấy dữ liệu từ request (yêu cầu client gửi dữ liệu JSON)
    data = request.get_json()

    node_id = data.get('NODE_ID')
    sensor_temp = data.get('SENSOR_TEMP')
    sensor_humi = data.get('SENSOR_HUMI')
    sensor_co = data.get('SENSOR_CO')
    pm_2_5 = data.get('PM_2_5')
    time = data.get('TIME')
    date = data.get('DATE')

    query = """
        INSERT INTO slaves (NODE_ID, SENSOR_TEMP, SENSOR_HUMI, SENSOR_CO, PM_2_5, TIME, DATE)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    query_db(query, (node_id, sensor_temp, sensor_humi, sensor_co, pm_2_5, time, date))
    
    return jsonify({"message": "Data added successfully"}), 201

# API DELETE để xóa dữ liệu của một slave theo ID
@app.route('/api/delete_slave/<int:id>', methods=['DELETE'])
def delete_slave(id):
    query = "DELETE FROM slaves WHERE ID = ?"
    query_db(query, [id])

    return jsonify({"message": "Slave deleted successfully"}), 200

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
