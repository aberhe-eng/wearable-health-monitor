# AI-Powered Wearable Health Monitor
A Raspberry Pi-based wearable device that reads real-time biometric data 
and uses on-device machine learning to detect health anomalies.
## What it does
- Reads heart rate, SpO2 (blood oxygen), and motion data from medical-grade sensors
- Processes signals in Python to extract heart rate variability (HRV)
- Runs an ML anomaly detection model entirely on-device
- Streams live data to a companion web dashboard accessible from any phone
## Tech stack
- Hardware: Raspberry Pi Zero 2W, MAX30102, MPU6050
- Language: Python
- ML: scikit-learn, TensorFlow Lite
- Dashboard: Flask + Chart.js
