from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # chỉ hiển thị giao diện
@app.route('/login')
def about():
    return render_template('login.html')  # Trang phụ
# đoạn này sẽ dẫn đến trang muốn

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
