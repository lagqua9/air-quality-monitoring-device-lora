 // Tạo bản đồ tại vị trí lat, lng
 var map = L.map('map').setView([21.0285, 105.8542], 20); // vĩ độ, kinh độ, zoom// Hà Nội

 // Thêm layer bản đồ từ OpenStreetMap
 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '© OpenStreetMap contributors'
 }).addTo(map);

 // // Thêm 1 marker mẫu
 // L.marker([21.0285, 105.8542])
 //     .addTo(map)
 //     .bindPopup('Vị trí trạm đo không khí')
 //     .openPopup();
