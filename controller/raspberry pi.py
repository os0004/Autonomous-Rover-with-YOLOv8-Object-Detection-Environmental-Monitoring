import cv2
import requests
import socket
import netifaces as ni # type: ignore
import RPi.GPIO as GPIO # type: ignore
import time

# GPIO setup
LED_PIN = 18  # Choose any GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Function to find laptop IP dynamically
def find_laptop_ip(port=5000):
    subnet = "192.168.172."  # Adjust if using a different network
    for i in range(1, 255):
        ip = f"{subnet}{i}"
        try:
            response = requests.get(f"http://{ip}:{port}/status", timeout=0.1)
            if response.status_code == 200:
                print(f"Laptop found at: {ip}")
                return ip
            else:
                print("nope")
        except requests.exceptions.RequestException:
            continue
    return None

# Open video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video capture")
    GPIO.output(LED_PIN, GPIO.LOW)
    exit()

# Find laptop IP dynamically
laptop_ip = find_laptop_ip()
if not laptop_ip:
    print("Error: Laptop not found!")
    GPIO.output(LED_PIN, GPIO.LOW)
    exit()

# Turn on LED to indicate streaming
GPIO.output(LED_PIN, GPIO.HIGH)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        GPIO.output(LED_PIN, GPIO.LOW)
        break

    ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])  # Reduce quality
    if not ret:
        print("Error encoding frame")
        GPIO.output(LED_PIN, GPIO.LOW)
        break

    # Send frame to Flask server
    try:
        response = requests.post(f'http://{laptop_ip}:5000/upload', files={'frame': jpeg.tobytes()})
        if response.status_code != 200:
            print(f"Error sending frame: {response.status_code}")
            GPIO.output(LED_PIN, GPIO.LOW)
    except requests.exceptions.RequestException:
        print("Error: Could not connect to the laptop server")
        GPIO.output(LED_PIN, GPIO.LOW)
        break

cap.release()
