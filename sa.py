from flask import Flask, render_template, jsonify
import serial
import threading
from datetime import datetime

app = Flask(__name__)  # Corrected _name_ to __name__

# Adjust this to your actual COM port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
ser = serial.Serial('COM5', 9600)

# Global variable to store sensor data
sensor_data = {"temperature": 0, "moisture": 0, "humidity": 0, "timestamp": "", "alerts": []}

# Read sensor data from serial port
def read_from_serial():
    global sensor_data
    while True:
        try:
            line = ser.readline().decode().strip()
            parts = line.split(',')
            if len(parts) == 3:
                temperature = float(parts[0])
                humidity = float(parts[1])
                moisture = int(parts[2])

                alerts = []
                if temperature > 35:
                    alerts.append("High Temperature Alert!")
                if moisture > 900:
                    alerts.append("Soil is too dry!")
                elif moisture < 300:
                    alerts.append("Soil is too wet!")

                sensor_data = {
                    "temperature": round(temperature, 2),
                    "humidity": round(humidity, 2),
                    "moisture": moisture,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "alerts": alerts
                }

                print("Data:", sensor_data)  # Debugging output

        except Exception as e:
            print("Error reading from serial:", e)

# Start the background thread for reading serial data
threading.Thread(target=read_from_serial, daemon=True).start()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    return jsonify(sensor_data)

if __name__ == '__main__':  # Corrected _name_ to __name__
    app.run(host='0.0.0.0', port=8080)
