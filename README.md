# Autonomous Rover Project

## Overview
This project is an **Autonomous Rover** capable of performing **manual and autonomous navigation**, **obstacle detection**, and **object recognition**. It integrates **Raspberry Pi 3B+**, **ESP32**, and a **Pi Camera** to create a smart rover with real-time decision-making and sensor integration.

The rover is designed to be lightweight, modular, and capable of performing environmental sensing and object detection using **YOLOv8n** and the **COCO dataset**.

---

## Features
- **Manual Control:** Operate the rover via a web interface.
- **Autonomous Navigation:** Obstacle detection and avoidance using ultrasonic sensors.
- **Object Recognition:** Detect and classify objects in real-time using YOLOv8n.
- **Environmental Monitoring:** Air quality monitoring using MQ2 gas sensor.
- **Load Balancing:** Raspberry Pi handles processing and camera input; ESP32 manages peripherals and motor control.

---

## Hardware Components
| Component       | Description                                      |
|-----------------|--------------------------------------------------|
| Raspberry Pi 3B+| Main controller for camera and processing tasks |
| ESP32           | Peripheral control (motors, servos, sensors)    |
| Pi Camera       | Video feed and object recognition input         |
| Ultrasonic Sensor| Obstacle detection                              |
| MQ2 Gas Sensor  | Air quality measurement                          |
| Motor Drivers   | Control motors and servos for movement           |

---

## Software & Libraries
- **Raspberry Pi OS**
- **Python 3**
- **YOLOv8n** (Ultralytics)
- **OpenCV** for camera handling
- **ESPAsyncWebServer** for web interface
- **MQTT/HTTP** for communication between Pi and ESP32
- **Flask** or **FastAPI** (optional) for web server on Raspberry Pi

---

## System Architecture
    +-----------------+
    |  Raspberry Pi   |
    |-----------------|
    |  Pi Camera      |
    |  YOLOv8n Model |
    |  Object Detection|
    +--------+--------+
             |
             | WiFi / HTTP / MQTT
             |
    +--------v--------+
    |      ESP32      |
    |-----------------|
    | Motors & Servos |
    | Ultrasonic Sensor|
    | MQ2 Gas Sensor  |
    +-----------------+





---

## Functionality

### Manual Mode
- Control rover using a web interface.
- Commands sent to ESP32 for motor and servo actuation.

### Autonomous Mode
- Rover navigates while detecting obstacles using the ultrasonic sensor.
- YOLOv8n identifies objects in real-time.
- Gas sensor monitors environmental air quality (PPM levels).

---

## Setup Instructions

### 1. Raspberry Pi
```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pip git
pip3 install opencv-python ultralytics flask

## Web Interface
<img width="2559" height="1425" alt="Image" src="https://github.com/user-attachments/assets/4cda2831-cab2-4917-bf8a-8b51ae48c090" />
