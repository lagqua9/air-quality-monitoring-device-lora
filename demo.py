from flask import Flask, render_template,jsonify,request
import sqlite3
app = Flask(__name__)

DB_PATH = 'database.db'#đường dẫn đến file cơ sở dữ liệu
#hàm định nghĩa db
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)  # Cố gắng kết nối với cơ sở dữ liệu
        conn.row_factory = sqlite3.Row  # Sử dụng row_factory để lấy kết quả dưới dạng dictionary
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None  # Nếu kết nối không thành công, trả về None
    
def check_credentials(account, password):
    conn = sqlite3.connect('database.db')  # Kết nối đến cơ sở dữ liệu
    cursor = conn.cursor()

    # Truy vấn xem tài khoản và mật khẩu có khớp trong bảng không
    cursor.execute('SELECT * FROM login WHERE account = ? AND password = ?', (account, password))
    row = cursor.fetchone()

    conn.close()

    if row:
        return True  # Tìm thấy tài khoản và mật khẩu khớp
    return False  # Không tìm thấy
# ================================
# API GET: Lấy thông tin cảm biến
# ================================
@app.route('/api/node_sensor', methods=['GET'])
def get_node_sensor():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Lấy tất cả dữ liệu từ bảng node_sensor
    cursor.execute("SELECT * FROM node_sensor")
    rows = cursor.fetchall()
    
    sensors = []
    for row in rows:
        sensors.append({
            'SLAVE_ID': row['SLAVE_ID'],
            'NODE_ID': row['NODE_ID'],
            'IP': row['IP'],
            'TEMP': row['TEMP'],
            'HUMI': row['HUMI'],
            'CO': row['CO'],
            'PM2_5': row['PM2_5'],
            'TIME_S': row['TIME_S'],
            'DATE_S': row['DATE_S']
        })
    
    conn.close()
    return jsonify(sensors)

# ================================
# API POST: Thêm thông tin cảm biến
# ================================
@app.route('/api/node_sensor', methods=['POST'])
def create_node_sensor():
    new_sensor = request.get_json()  # Lấy dữ liệu từ request
    
    # Truyền dữ liệu vào cơ sở dữ liệu
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO node_sensor (SLAVE_ID, NODE_ID, IP, TEMP, HUMI, CO, PM2_5, TIME_S, DATE_S)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (new_sensor['SLAVE_ID'], new_sensor['NODE_ID'], new_sensor['IP'], new_sensor['TEMP'], new_sensor['HUMI'], new_sensor['CO'], 
         new_sensor['PM2_5'], new_sensor['TIME_S'], new_sensor['DATE_S']))
    
    conn.commit()
    conn.close()
    return jsonify(new_sensor), 201  # Trả về dữ liệu đã thêm và mã HTTP 201

# ================================
# API PUT: Cập nhật thông tin cảm biến
# ================================
@app.route('/api/node_sensor/<int:slave_id>/<int:node_id>', methods=['PUT'])
def update_node_sensor(slave_id, node_id):
    updated_sensor = request.get_json()  # Lấy dữ liệu từ request
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE node_sensor 
        SET IP = ?, LAT = ?, LONG = ?, TEMP = ?, HUMI = ?, CO = ?, PM2_5 = ?, 
            TIME_S = ?, DATE_S = ?
        WHERE SLAVE_ID = ? AND NODE_ID = ?''', 
        (updated_sensor['IP'], updated_sensor['LAT'], updated_sensor['LONG'], 
         updated_sensor['TEMP'], updated_sensor['HUMI'], updated_sensor['CO'], 
         updated_sensor['PM2_5'], updated_sensor['TIME_S'], updated_sensor['DATE_S'], 
         slave_id, node_id))
    
    conn.commit()
    conn.close()
    
    return jsonify(updated_sensor)  # Trả về dữ liệu đã cập nhật

# ================================
# API DELETE: Xóa thông tin cảm biến
# ================================
@app.route('/api/node_sensor/<int:slave_id>/<int:node_id>', methods=['DELETE'])
def delete_node_sensor(slave_id, node_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM node_sensor WHERE SLAVE_ID = ? AND NODE_ID = ?''', 
        (slave_id, node_id))
    
    conn.commit()
    conn.close()
    
    return '', 204  # Trả về mã HTTP 204 (No Content) sau khi xóa thành công


@app.route('/api/login', methods=['GET'])
def login():
    # Lấy tham số 'account' và 'password' từ URL query string
    account = request.args.get('account')
    password = request.args.get('password')

    if not account or not password:
        return jsonify({"error": "Account and password are required"}), 400

    # Kiểm tra tài khoản và mật khẩu trong cơ sở dữ liệu
    if check_credentials(account, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/')
def index():
    return render_template('index.html')  # chỉ hiển thị giao diện
@app.route('/login')
def about():
    return render_template('login.html')  # Trang phụ
# đoạn này sẽ dẫn đến trang muốn

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
