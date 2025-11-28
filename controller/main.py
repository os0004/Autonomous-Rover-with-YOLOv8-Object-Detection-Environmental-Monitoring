from flask import Flask, render_template, request, Response, jsonify
from ultralytics import YOLO
import numpy as np
import requests
import torch
import cv2

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

import socket

ESP32_IP = None

def find_esp32_ip():
    try:
        return socket.gethostbyname("esp32.local")
    except socket.gaierror:
        return None
while 1:

    ESP32_IP = find_esp32_ip()

    if ESP32_IP:
        print(f"ESP32 IP Found: {ESP32_IP}")
        break
    else:
        print("ESP32 not found on network")




# Load YOLOv8 model
model = YOLO('yolov8n.pt')

print("Model loaded!")

# app = Flask(__name__)

def generate():
    global current_frame
    while True:
        if current_frame is not None:
            results = model(current_frame)
            
            # Process detections
            for result in results:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box.tolist()
                    label = f"{model.names[int(cls)]}: {conf:.2f}"
                    cv2.rectangle(current_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(current_frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Show current_frame


            ret, jpeg = cv2.imencode('.jpg', current_frame)


            if ret:
                # Convert the frame to bytes
                frame_bytes = jpeg.tobytes()
                
                # Yield the frame as part of an MJPEG stream
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


# Initialize an empty variable to store the latest frame
current_frame = None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/led/on', methods=['GET'])
def led_on():

    response = requests.get(f"http://{ESP32_IP}/led/on", timeout=1)
    data = response.text.strip()  # Ensure clean data
    print(data)

    return "OK"

@app.route('/led/off', methods=['GET'])
def led_off():

    response = requests.get(f"http://{ESP32_IP}/led/off", timeout=1)
    data = response.text.strip()  # Ensure clean data
    print(data)

    return "OK"

@app.route('/autonomous', methods=['GET'])
def autonomous():
    state = request.args.get('state')
    print(state)
    response = requests.get(f"http://{ESP32_IP}/autonomous?state={state}", timeout=1)
    data = response.text.strip()  # Ensure clean data
    print(data)

    return "OK"

@app.route('/airquality', methods=['GET'])
def air_quality():
    try:
        # Fetch data from ESP32
        response = requests.get(f"http://{ESP32_IP}/airquality", timeout=1)
        data = response.text.strip()  # Ensure clean data
        print(data)
        # Convert to JSON response
        return jsonify({"status": "success", "air_quality": float(data)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_frame():
    global current_frame
    frame_data = request.files['frame'].read()
    
    # Convert the bytes back into a frame
    np_arr = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None or frame.size == 0:
        return "Error: Received an invalid frame", 400

    # Update the current frame with the received frame
    current_frame = frame
    return "Frame received successfully", 200

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alive')
def alive():
    return "I'm alive!", 200

@app.route('/move', methods=['GET'])
def move():
    x = request.args.get('x')
    y = request.args.get('y')
    print("x: ", x, "y: ", y)
    if x and y:
        requests.get(f"http://{ESP32_IP}/move?x={x}&y={y}")
    return "OK"

@app.route('/status', methods=['GET'])
def status():
    return "Server is running", 200

@app.route('/servo', methods=['GET'])
def servo():
    pan = request.args.get('pan')
    tilt = request.args.get('tilt')
    print("pan: ", pan, "tilt: ", tilt)
    if pan and tilt:
        requests.get(f"http://{ESP32_IP}/servo?pan={pan}&tilt={tilt}")
    return "OK"

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
