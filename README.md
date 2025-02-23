# IoT Monitoring System dengan ESP32, Ubidots, dan Flask

Projek ini merupakan Tugas dari Program SIC6 dimana kelompok kami membuat sistem pemantauan berbasis IoT menggunakan ESP32 yang dilengkapi dengan sensor DHT11 (suhu & kelembaban) dan sensor ultrasonik HC-SR04 (jarak/ketinggian air). Data dari sensor dikirim ke Ubidots untuk visualisasi dalam dashboard serta ke server lokal Flask untuk penyimpanan dan analisis lebih lanjut.

## Fitur Utama
- Mengukur suhu dan kelembaban menggunakan **DHT11**
- Mengukur ketinggian air menggunakan **HC-SR04**
- Mengirim data ke **Ubidots** untuk ditampilkan dalam dashboard
- Mengirim data ke **Flask API** untuk penyimpanan lokal
- Menampilkan status sensor berdasarkan nilai sensor

## Perangkat Keras yang Dibutuhkan
- **ESP32**
- **Sensor DHT11**
- **Sensor Ultrasonik HC-SR04**
- **Koneksi WiFi**

## Instalasi dan Konfigurasi

### 1. Persiapan ESP32
#### a. Instalasi MicroPython di ESP32
1. Flash firmware MicroPython ke ESP32.
2. Gunakan **Thonny IDE** untuk mengunggah kode ke ESP32.

#### b. Instalasi Library di MicroPython
Gunakan pustaka bawaan **MicroPython**, pastikan pustaka berikut tersedia:
- `machine`
- `network`
- `urequests`
- `utime`
- `dht`

#### c. Konfigurasi Kode ESP32
Ubah bagian berikut sesuai dengan jaringan dan token Ubidots Anda:
```python
DEVICE_ID = "sic6-togetherness-squad"
WIFI_SSID = "F"
WIFI_PASSWORD = "q12345678"
UBIDOTS_TOKEN = "BBUS-k2NJrQUkSnRsTMTQ089853FikiuDIx"
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}"
FLASK_URL = "http://192.168.0.103:5000/data"  # Sesuaikan dengan IP Flask Anda
```

### 2. Menjalankan Server Flask
#### a. Instalasi Flask
```bash
pip install flask
```
#### b. Jalankan Server
1. Buat file `app.py` dengan kode berikut:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = []

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    data_store.append(data)
    return jsonify({"status": "success", "message": "Data received"})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(data_store)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```
2. Jalankan server dengan perintah:
```bash
python app.py
```

### 3. Menguji dengan Postman
- Kirim data ke Flask API menggunakan Postman:
  - **Method:** `POST`
  - **URL:** `http://192.168.1.13:5000/data`
  - **Body (JSON):**
  ```json
  {
    "device_id": "esp32-togethernesssuad",
    "temperature": 25,
    "humidity": 60,
    "distance": 10
  }
  ```
- Ambil data tersimpan:
  - **Method:** `GET`
  - **URL:** `http://192.168.1.13:5000/data`

## Konfigurasi Dashboard Ubidots
1. Buat **Device** baru di Ubidots.
2. Tambahkan **Variables**: `temperature`, `humidity`, `distance`, `status`.
3. Buat **Dashboard** dengan widget:
   - **Line Chart** untuk suhu & kelembaban
   - **Gauge** untuk jarak/ketinggian air
   - **Indicator** untuk status sensor

## Kesimpulan
Proyek ini memungkinkan monitoring lingkungan secara real-time dengan ESP32, mengirimkan data ke Ubidots untuk visualisasi, dan ke server Flask untuk penyimpanan lokal. Sistem ini dapat diperluas dengan menambahkan fitur lain seperti notifikasi dan kontrol otomatis.

---
### Lisensi
Proyek ini bersifat open-source, silakan gunakan dan modifikasi sesuai kebutuhan.

