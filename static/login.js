document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Ngăn chặn hành động submit mặc định của form

    // Lấy giá trị từ các trường input
    var account = document.getElementById('account').value;
    var password = document.getElementById('password').value;

    // Tạo URL với query string
    var url = `http://192.168.1.12:5000/api/login?account=${encodeURIComponent(account)}&password=${encodeURIComponent(password)}`;

    // Gửi yêu cầu GET sử dụng fetch
    fetch(url)
    .then(response => response.json())
    .then(data => {
        // Hiển thị thông báo từ server
        if (data.message) {
            document.getElementById('response').innerHTML = `<p style="color: green;">${data.message}</p>`;
            localStorage.setItem('status', 'true');

            // Sau khi đăng nhập thành công, chuyển hướng về trang chính (hoặc trang khác)
            window.location.href = 'http://192.168.1.12:5000';  // Chuyển hướng về trang chính
        } else if (data.error) {
            document.getElementById('response').innerHTML = `<p style="color: red;">${data.error}</p>`;
            localStorage.setItem('status', 'false');
        }
    })
    .catch(error => {
        // Xử lý lỗi (nếu có)
        console.error('Error:', error);
    });
});


document.getElementById('signup-btn').addEventListener('click', function() {
    // Ẩn form đăng nhập và hiển thị form đăng ký
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('singup').style.display = 'block';
});

document.getElementById('login-btn').addEventListener('click', function() {
    // Hiển thị form đăng nhập và ẩn form đăng ký
    document.getElementById('singup').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
});