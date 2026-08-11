# CardioNode — AI-Powered Wearable Biosignal Monitor

A wrist-worn biosignal acquisition device built on a Raspberry Pi Zero 2W. Reads
photoplethysmography (PPG) and motion data from medical-grade sensor modules,
extracts heart rate and heart rate variability through a Python signal
processing pipeline, and runs on-device anomaly detection.

**Status:** Phase 1 complete — dual-sensor I2C acquisition verified.

---

## Hardware

| Component | Role | I2C Address |
|---|---|---|
| Raspberry Pi Zero 2W | Host controller, Python runtime | — |
| MAX30102 | Red/IR optical PPG sensor (heart rate, SpO2) | `0x57` |
| MPU6050 | 3-axis accelerometer + gyroscope (motion, artifact rejection) | `0x68` |

Both sensors share a single I2C bus on GPIO2 (SDA) and GPIO3 (SCL).

### Wiring

| Pi Pin | Signal | MAX30102 | MPU6050 |
|---|---|---|---|
| 1 | 3.3V | VIN | — |
| 17 | 3.3V | — | VCC |
| 6 | GND | GND | — |
| 9 | GND | — | GND |
| 3 | SDA | SDA | SDA |
| 5 | SCL | SCL | SCL |

Pins 3 and 5 are shared between both sensors via soldered splice junctions.
The MAX30102 `INT` pin is unconnected — the driver polls the FIFO pointers
rather than using interrupt-driven acquisition.

**Never connect either sensor to pins 2 or 4 (5V).** Both modules are 3.3V logic.

---

## Setup

Enable I2C via `sudo raspi-config` → Interface Options → I2C, then verify:

```bash
i2cdetect -y 1
```

Both `57` and `68` should appear in the address grid.

### Dependencies

```bash
sudo apt install git python3-smbus python3-numpy -y
pip install mpu6050-raspberrypi --break-system-packages
```

The MAX30102 driver is **not available on PyPI** and must be cloned:

```bash
cd ~
git clone https://github.com/doug-burrell/max30102.git
```

`cardionode_poll.py` adds this path at runtime via `sys.path.insert()`. Adjust
the hardcoded path if you clone elsewhere.

---

## Scripts

| File | Purpose |
|---|---|
| `cardionode_poll.py` | Combined polling loop — logs timestamp, IR, red, and accelerometer x/y/z |
| `mpu_test.py` | Standalone accelerometer verification (tilt test) |

### Running

```bash
python3 cardionode_poll.py
```

Outputs CSV-formatted rows to stdout. `Ctrl+C` to stop.

---

## Verified Results

**MAX30102 optical response**

| Condition | IR (counts) |
|---|---|
| No finger (dark baseline) | ~540–660 |
| Finger present | ~140,000 |

The ~260× increase confirms both LEDs and the photodiode are functional.
The pulsatile (AC) component riding on this DC level is the PPG waveform.

**MPU6050 tilt response** — gravity vector transfers correctly between axes on
rotation; vector magnitude holds near 9.8 m/s² at rest.

**Stability** — 55 minutes of continuous dual-sensor logging with zero I2C
errors and no dropped reads.

---

## Known Limitations

These are documented deliberately. Each is a target for a later phase.

**Sample rate.** The polling loop runs at roughly 3.9 s/iteration rather than the
intended 0.5 s, because `read_sequential()` blocks while the sensor FIFO fills.
Peak detection requires a far higher sample rate — this loop will be restructured
around a threaded reader in Phase 2.

**SpO2 is uncalibrated.** Steady-state readings cluster near 99.8%, which is
implausibly high. The driver ships with generic ratio-to-saturation coefficients
and has not been validated against a reference oximeter. Treat SpO2 output as
uncalibrated until Phase 2 validation.

**Invalid-sample sentinels.** The driver emits `SpO2: -999` when the red/IR ratio
falls outside a valid window. These are not measurements and must be filtered
before any statistical analysis. Physically impossible values (e.g. 27%, 57%)
also appear on motion-corrupted windows.

**Startup transient.** The first ~15 seconds of any run are invalid while the
100-sample calculation buffer fills. Discard.

**Smoothed BPM is unsuitable for HRV.** The driver returns a 4-sample rolling
mean. HRV (RMSSD) requires raw beat-to-beat RR intervals, which will be derived
from peak detection on the raw IR stream in Phase 2.

**Reflectance geometry.** LEDs and photodiode sit on the same face, so the sensor
measures backscattered rather than transmitted light. This is inherently noisier
and more motion-sensitive than the transmissive geometry used in clinical
fingertip oximeters.

**Mechanical fragility.** Connections are friction-fit Dupont jumpers on
hand-soldered splice junctions. Stable when undisturbed, but vulnerable to
physical movement — migration to soldered perfboard is planned for Phase 4.

**Reproducibility.** The project currently depends on a manually cloned external
repository and a hardcoded path. A setup script and `requirements.txt` are
planned for Phase 5.

---

## Roadmap

- [x] **Phase 1 — Hardware foundations.** Dual-sensor I2C acquisition, stable logging
- [ ] **Phase 2 — Signal processing.** Bandpass filtering, peak detection, BPM and RMSSD extraction, CSV data logger, validation against a reference oximeter
- [ ] **Phase 3 — Machine learning.** Activity classification and personal-baseline anomaly detection, deployed on-device
- [ ] **Phase 4 — Dashboard.** Flask API + Chart.js live monitoring, perfboard migration, battery and enclosure
- [ ] **Phase 5 — Portfolio.** Technical write-up, demo video, reproducible setup

---

## Stack

Python · NumPy · SciPy · pandas · scikit-learn · TensorFlow Lite · Flask · Chart.js
