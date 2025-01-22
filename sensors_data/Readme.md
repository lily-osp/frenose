# Sensors Data: Arduino Code for E-Nose System

This folder contains the Arduino code for reading data from MQ sensors in two different configurations:
1. **Single Sensor Setup**: Reads data from 8 MQ sensors directly connected to analog pins (without a multiplexer).
2. **Cluster Setup**: Reads data from multiple clusters of MQ sensors using multiplexers.

---

## **Table of Contents**
1. [Single Sensor Setup](#single-sensor-setup)
2. [Cluster Setup](#cluster-setup)
3. [Hardware Requirements](#hardware-requirements)
4. [Pinout Map](#pinout-map)
5. [Setup Instructions](#setup-instructions)
6. [How It Works](#how-it-works)
7. [Troubleshooting](#troubleshooting)

---

## **Single Sensor Setup**
The `single.ino` file is used when you have **8 MQ sensors** connected directly to the analog pins of the microcontroller (no multiplexer is used).

### **Hardware Setup**
- Connect each MQ sensor to the analog pins of the MCU as follows:
  - **MQ-2**: A0
  - **MQ-3**: A1
  - **MQ-4**: A2
  - **MQ-6**: A3
  - **MQ-135**: A4
  - **MQ-136**: A5
  - **MQ-138**: A6
  - **MQ-9**: A7

### **Code Overview**
- The code reads data from the 8 MQ sensors connected to analog pins A0-A7.
- The sensor data is sent to the computer via serial communication in CSV format.
- Data is sent every second.

### **How to Use**
1. Upload the `single.ino` code to your microcontroller.
2. Open the Serial Monitor in the Arduino IDE to view the sensor data.
3. The data will be displayed in the following format:
   ```
   MQ2,MQ3,MQ4,MQ6,MQ135,MQ136,MQ138,MQ9
   ```

---

## **Cluster Setup**
The `cluster.ino` file is used when you have **multiple clusters of MQ sensors** connected via multiplexers. Each cluster can have up to 8 MQ sensors.

### **Hardware Setup**
- Each cluster uses a **CD74HC4067** 16-channel analog multiplexer.
- Connect the multiplexer control pins (S0-S3) to the digital pins of the MCU.
- Connect the multiplexer output to one of the analog pins of the MCU.
- Each cluster can support up to 8 MQ sensors.

### **Code Overview**
- The code supports **1 to 8 clusters**, each with 8 MQ sensors.
- The readings from each sensor type are averaged across all clusters.
- The averaged data is sent to the computer via serial communication in CSV format.
- Data is sent every second.

### **How to Use**
1. Set the number of clusters in the `NUM_CLUSTERS` variable in the `cluster.ino` file.
2. Upload the `cluster.ino` code to your microcontroller.
3. Open the Serial Monitor in the Arduino IDE to view the averaged sensor data.
4. The data will be displayed in the following format:
   ```
   MQ2_avg,MQ3_avg,MQ4_avg,MQ6_avg,MQ135_avg,MQ136_avg,MQ138_avg,MQ9_avg
   ```

---

## **Hardware Requirements**
1. **Microcontroller (MCU)**:
   - Any MCU with at least **1 analog pin** (e.g., Arduino Nano, Arduino Mega, ESP32, STM32, etc.).
   - For the cluster setup, ensure the MCU has enough digital pins for multiplexer control.
2. **Sensors**:
   - **MQ-2**: LPG, propane, methane, hydrogen, smoke.
   - **MQ-3**: Alcohol, ethanol, benzene.
   - **MQ-4**: Methane, natural gas.
   - **MQ-6**: LPG, butane, propane.
   - **MQ-135**: Ammonia, benzene, alcohol, smoke, CO₂.
   - **MQ-136**: Hydrogen sulfide (H₂S).
   - **MQ-138**: Benzene, toluene, alcohol, acetone, propane, formaldehyde.
   - **MQ-9**: Carbon monoxide (CO), flammable gases.
3. **Multiplexers (Optional)**:
   - Use **CD74HC4067** (16-channel analog multiplexer) for the cluster setup.

---

## **Pinout Map**
### **Single Sensor Setup**
| Sensor | Analog Pin |
|--------|------------|
| MQ-2   | A0         |
| MQ-3   | A1         |
| MQ-4   | A2         |
| MQ-6   | A3         |
| MQ-135 | A4         |
| MQ-136 | A5         |
| MQ-138 | A6         |
| MQ-9   | A7         |

### **Cluster Setup**
| Cluster | Control Pins (S0-S3) | Analog Pin | Sensors Connected                     |
|---------|----------------------|------------|---------------------------------------|
| Cluster 1 | D2, D3, D4, D5       | A0         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |
| Cluster 2 | D6, D7, D8, D9       | A1         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |
| Cluster 3 | D10, D11, D12, D13   | A2         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |
| Cluster 4 | D14, D15, D16, D17   | A3         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |

---

## **Setup Instructions**
1. **Single Sensor Setup**:
   - Upload the `single.ino` code to your MCU.
   - Connect the sensors to the analog pins as per the pinout map.
   - Open the Serial Monitor to view the sensor data.
2. **Cluster Setup**:
   - Upload the `cluster.ino` code to your MCU.
   - Set the number of clusters in the `NUM_CLUSTERS` variable.
   - Connect the multiplexers and sensors as per the pinout map.
   - Open the Serial Monitor to view the averaged sensor data.

---

## **How It Works**
1. **Single Sensor Setup**:
   - The MCU reads data from the 8 MQ sensors connected to analog pins A0-A7.
   - The data is sent to the computer via serial communication.
2. **Cluster Setup**:
   - The MCU reads data from multiple clusters of MQ sensors using multiplexers.
   - The readings for each sensor type are averaged across all clusters.
   - The averaged data is sent to the computer via serial communication.

---

## **Troubleshooting**
1. **No Data Received**:
   - Check the COM port and ensure the MCU is connected.
2. **Incorrect Readings**:
   - Calibrate the sensors and check connections.
3. **Multiplexer Issues**:
   - Ensure the multiplexer control pins are correctly connected.
