from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)

while True:
    a = sensor.get_accel_data()
    print(f"x: {a['x']:.2f}  y: {a['y']:.2f}  z: {a['z']:.2f}")
    time.sleep(0.5)
