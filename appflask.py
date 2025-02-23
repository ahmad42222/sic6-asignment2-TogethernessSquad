from flask import Flask, request, jsonify

app = Flask(__name__)

# Simpan data sementara
data_store = []

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()  # Ambil data JSON dari ESP32
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        data_store.append(data)  # Simpan data ke dalam list
        print("Data diterima:", data)

        return jsonify({"message": "Data berhasil diterima!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk melihat data yang sudah tersimpan
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
