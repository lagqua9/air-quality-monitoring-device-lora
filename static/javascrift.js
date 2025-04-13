 // Tạo bản đồ tại vị trí lat, lng
//  var map = L.map('map').setView([21.0285, 105.8542], 20); // vĩ độ, kinh độ, zoom// Hà Nội

//  // Thêm layer bản đồ từ OpenStreetMap
//  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//      attribution: '© OpenStreetMap contributors'
//  }).addTo(map);

 // // Thêm 1 marker mẫu
 // L.marker([21.0285, 105.8542])
 //     .addTo(map)
 //     .bindPopup('Vị trí trạm đo không khí')
 //     .openPopup();

navigator.geolocation.getCurrentPosition(function(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    // Gửi vị trí lên server Flask
    fetch('/send_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude: lat, longitude: lon })
    });
});
const URL_API ='http://192.168.1.12:5000/api/node_sensor'
// Hàm lấy dữ liệu từ API và vẽ biểu đồ ECharts
async function fetchDataAndRenderChart() {
    try {
        const response = await fetch(URL_API);
        const data = await response.json();  // Giả sử API trả về dữ liệu JSON

        // Lấy 5 giá trị cuối của CO và thời gian
        const coValues = data.slice(-5).map(item => item.CO);
        const timeLabels = data.slice(-5).map(item => item.TIME_S);

        // Tạo biểu đồ CO với ECharts
        var chartDom = document.getElementById('co_chart');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
            title: {
                text: 'CO',
                textAlign: 'center',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: timeLabels  // Sử dụng thời gian làm trục X
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: coValues,  // Dữ liệu CO
                    type: 'line',
                    smooth: true
                }
            ]
        };

        myChart.setOption(option);
    } catch (error) {
        console.error('Lỗi khi lấy dữ liệu từ API:', error);
    }
}

async function temp() {
    try {
        const response = await fetch(URL_API);
        const data = await response.json();  // Giả sử API trả về dữ liệu JSON

        // Lấy 5 giá trị cuối của CO và thời gian
        const coValues = data.slice(-5).map(item => item.TEMP);
        const timeLabels = data.slice(-5).map(item => item.TIME_S);

        // Tạo biểu đồ CO với ECharts
        var chartDom = document.getElementById('temp_chart');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
            title: {
                text: 'TEMP',
                textAlign: 'center',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: timeLabels  // Sử dụng thời gian làm trục X
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: coValues,  // Dữ liệu CO
                    type: 'line',
                    smooth: true
                }
            ]
        };

        myChart.setOption(option);
    } catch (error) {
        console.error('Lỗi khi lấy dữ liệu từ API:', error);
    }
}


async function humi() {
    try {
        const response = await fetch(URL_API);
        const data = await response.json();  // Giả sử API trả về dữ liệu JSON

        // Lấy 5 giá trị cuối của CO và thời gian
        const coValues = data.slice(-5).map(item => item.HUMI);
        const timeLabels = data.slice(-5).map(item => item.TIME_S);

        // Tạo biểu đồ CO với ECharts
        var chartDom = document.getElementById('humi_chart');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
            title: {
                text: 'HUMI',
                textAlign: 'center',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: timeLabels  // Sử dụng thời gian làm trục X
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: coValues,  // Dữ liệu CO
                    type: 'line',
                    smooth: true
                }
            ]
        };

        myChart.setOption(option);
    } catch (error) {
        console.error('Lỗi khi lấy dữ liệu từ API:', error);
    }
}

async function pm2_5() {
    try {
        const response = await fetch(URL_API);
        const data = await response.json();  // Giả sử API trả về dữ liệu JSON

        // Lấy 5 giá trị cuối của CO và thời gian
        const coValues = data.slice(-5).map(item => item.PM2_5);
        const timeLabels = data.slice(-5).map(item => item.TIME_S);

        // Tạo biểu đồ CO với ECharts
        var chartDom = document.getElementById('pm2_5_chart');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
            title: {
                text: 'PM2_5',
                textAlign: 'center',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: timeLabels  // Sử dụng thời gian làm trục X
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: coValues,  // Dữ liệu CO
                    type: 'line',
                    smooth: true
                }
            ]
        };

        myChart.setOption(option);
    } catch (error) {
        console.error('Lỗi khi lấy dữ liệu từ API:', error);
    }
}
// Gọi hàm để lấy dữ liệu và vẽ biểu đồ khi trang được tải
fetchDataAndRenderChart();
temp();
humi();
pm2_5();
setInterval(fetchDataAndRenderChart, 2000);
setInterval(temp, 2000);
setInterval(humi,2000);
setInterval(pm2_5,2000);