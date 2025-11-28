🚀 Autonomous Rover with YOLOv8 Object Detection & Environmental Monitoring

This project is a hybrid autonomous rover system built using Raspberry Pi 3B+ and ESP32, designed for object detection, navigation, and air-quality monitoring. The rover supports both manual control through a web interface and autonomous obstacle avoidance, making it ideal for robotics, IoT, and computer vision applications.

🔧 Tech Stack
Hardware

Raspberry Pi 3B+ (1GB RAM)

ESP32 Dev Module

Pi Camera

Ultrasonic Sensor (HC-SR04)

MQ2 Gas Sensor

Motor Driver + Servo Motors

Software

Python

YOLOv8n (Ultralytics)

COCO Dataset

ESPAsyncWebServer (ESP32)

HTML/CSS/JS (Web UI)

⚙️ System Architecture

The project uses a distributed processing model:

Raspberry Pi (High-Level Processing)

Runs YOLOv8n for real-time object detection

Handles Pi Camera feed

Performs inference and recognition

Sends high-level commands or alerts

ESP32 (Low-Level Control)

Controls motors, servos, and movement

Manages ultrasonic sensor

Reads MQ2 gas sensor data

Hosts web dashboard using ESPAsyncWebServer

This separation ensures smooth performance even on low-power hardware.

🧠 Key Features
✔ Real-Time Object Detection

YOLOv8n trained on COCO dataset

Live detection through Pi Camera

Displays class labels & bounding boxes

Supports recognition for navigation decisions

✔ Autonomous Navigation

Ultrasonic sensor for obstacle detection

Automated braking & directional decision-making

Hybrid mode: Autonomous + Manual

✔ Manual Control Interface

ESP32 hosts a responsive web dashboard

Control motors & servo angles

Real-time sensor readings

No external app required

✔ Air Quality Monitoring

MQ2 sensor integration

PPM calculation for smoke/flammable gases

Alerts triggered on threshold levels

📊 Output

Live object detection stream

Web-based rover controls

Gas-level monitoring dashboard

Obstacle avoidance logs

📁 Project Structure
/RaspberryPi/
   ├── vision.py
   ├── yolov8_engine/
   ├── requirements.txt

/ESP32/
   ├── main.ino
   ├── webserver/
   ├── motor_driver/
