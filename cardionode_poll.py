import sys
sys.path.insert(0, '/home/aman/max30102')
import max30102
import time
from datetime import datetime
from mpu6050 import mpu6050

m = max30102.MAX30102()
imu = mpu6050(0x68)

print("timestamp,ir,red,accel_x,accel_y,accel_z")

errors = 0

while True:
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    try:
        red, ir = m.read_sequential()
        ir_val, red_val = ir[0], red[0]
    except OSError:
        ir_val, red_val = None, None
        errors += 1

    try:
        a = imu.get_accel_data()
        ax, ay, az = a['x'], a['y'], a['z']
    except OSError:
        ax = ay = az = None
        errors += 1

    print(f"{ts},{ir_val},{red_val},{ax},{ay},{az}")
    time.sleep(0.5)
