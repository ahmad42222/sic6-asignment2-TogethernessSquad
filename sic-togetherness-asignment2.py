from machine import Pin, time_pulse_us
import network
import utime as time
import dht
import urequests as requests

# Konfigurasi API
DEVICE_ID = "sic6-togetherness-squad"
WIFI_SSID = "F"
WIFI_PASSWORD = "q12345678"
UBIDOTS_TOKEN = "BBUS-k2NJrQUkSnRsTMTQ089853FikiuDIx"
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}"
FLASK_URL = "http://192.168.0.103:5000/data"  # Sesuaikan dengan IP Flask Anda

DHT_PIN = Pin(14)
dht_sensor = dht.DHT11(DHT_PIN)

# Konfigurasi Sensor Ultrasonic
TRIG_PIN = Pin(12, Pin.OUT)
ECHO_PIN = Pin(13, Pin.IN)

# Koneksi WiFi
def connect_wifi():
    wifi_client = network.WLAN(network.STA_IF)
    wifi_client.active(True)
    wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

    timeout = 10
    while not wifi_client.isconnected() and timeout > 0:
        print("Mencoba koneksi...")
        time.sleep(1)
        timeout -= 1

    if wifi_client.isconnected():
        print("WiFi Terhubung!")
        print(wifi_client.ifconfig())
        return True
    else:
        print("Gagal terhubung ke WiFi!")
        return False

# Membaca Data jarak dari sensor Ultrasonik
def read_distance():
    TRIG_PIN.off()
    time.sleep_us(2)
    TRIG_PIN.on()
    time.sleep_us(10)
    TRIG_PIN.off()

    pulse_duration = time_pulse_us(ECHO_PIN, 1, 30000)  # Timeout 30ms
    if pulse_duration < 0:
        return -1  # Gagal membaca jarak
    
    distance = (pulse_duration * 0.0343) / 2  # Konversi ke cm
    return round(distance, 2)

# Mngirim data ke Ubidots
def send_to_ubidots(temperature, humidity, distance):
    max_distance = 100  # Misalnya 100 cm adalah kosong
    level = max(0, min(100, (max_distance - distance) * 100 / max_distance))  # Konversi ke persentase
    
    data = {"temp": temperature, "humidity": humidity, "distance": distance,"level": level }
    headers = {"Content-Type": "application/json", "X-Auth-Token": UBIDOTS_TOKEN}
    
    try:
        response = requests.post(UBIDOTS_URL, json=data, headers=headers, timeout=5)
        
        if response.status_code in [200, 201]:
            print("[UBIDOTS] Data berhasil dikirim!")
        else:
            print("[UBIDOTS] Gagal mengirim data!")
    
    except Exception as e:
        print("[UBIDOTS] Gagal mengirim data!")


# Mengirim data ke Flask
def send_to_flask(temperature, humidity, distance):
    max_distance = 100  # Misalnya 100 cm adalah kosong
    level = max(0, min(100, (max_distance - distance) * 100 / max_distance))  # Konversi ke persentase
    
    data = {"temp": temperature, "humidity": humidity, "distance": distance,"level": level }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(FLASK_URL, json=data, headers=headers, timeout=5)  
        
        if response.status_code == 200:
            print("[FLASK] Data berhasil dikirim!")
        else:
            print("[FLASK] Gagal mengirim data!")
    
    except Exception as e:
        print("[FLASK] Gagal mengirim data!")


# Menghubungkan ke WiFi
if connect_wifi():
    while True:
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            distance = read_distance()
            max_distance = 100  # Misalnya 100 cm adalah kosong
            level = max(0, min(100, (max_distance - distance) * 100 / max_distance))  # Konversi ke persentase

            print(f"Suhu: {temperature}°C, Kelembaban: {humidity}%, Jarak: {distance} cm, Volume: {level}%")

            # Mengirim ke Ubidots & Flask
            send_to_ubidots(temperature, humidity, distance)
            send_to_flask(temperature, humidity, distance)
        except Exception as e:
            print("Kesalahan membaca sensor:", str(e))

        time.sleep(5)
