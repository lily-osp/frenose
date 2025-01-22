# Dummy Data Generator for E - Nose System

This folder contains the `dummy_generator.ino` file, which generates random sensor values for testing purposes. This code is useful when you want to simulate sensor data without having physical MQ sensors connected to your microcontroller.

---

## **Table of Contents**
1. [Introduction](#introduction)
2. [How It Works](#how-it-works)
3. [Setup Instructions](#setup-instructions)
4. [Output Format](#output-format)
5. [Troubleshooting](#troubleshooting)

---

## **Introduction**
The `dummy_generator.ino` file is designed to simulate the behavior of an E-Nose system by generating random values for 8 MQ sensors. This is particularly useful for:
- Testing the Python (Qt) interface without physical sensors.
- Debugging and development when sensors are not available.
- Simulating different scenarios for machine learning model training.

---

## **How It Works**
- The code generates random values between 0 and 1023 for each of the 8 MQ sensors.
- The values are sent to the computer via serial communication in CSV format.
- Data is sent every second.

### **Sensors Simulated**
- **MQ-2**: Simulates LPG, propane, methane, hydrogen, and smoke.
- **MQ-3**: Simulates alcohol, ethanol, and benzene.
- **MQ-4**: Simulates methane and natural gas.
- **MQ-6**: Simulates LPG, butane, and propane.
- **MQ-135**: Simulates ammonia, benzene, alcohol, smoke, and CO₂.
- **MQ-136**: Simulates hydrogen sulfide (H₂S).
- **MQ-138**: Simulates benzene, toluene, alcohol, acetone, propane, and formaldehyde.
- **MQ-9**: Simulates carbon monoxide (CO) and flammable gases.

---

## **Setup Instructions**
1. **Upload the Code**:
   - Open the `dummy_generator.ino` file in the Arduino IDE.
   - Upload the code to your microcontroller.
2. **Open Serial Monitor**:
   - Open the Serial Monitor in the Arduino IDE.
   - Set the baud rate to **9600**.
3. **View Dummy Data**:
   - The dummy data will be displayed in the Serial Monitor every second.

---

## **Output Format**
The dummy data is sent in CSV format, with each sensor value separated by a comma. The output looks like this:
```
MQ2,MQ3,MQ4,MQ6,MQ135,MQ136,MQ138,MQ9
```
Example:
```
512,300,800,450,700,200,900,600
```

---

## **Troubleshooting**
1. **No Data Received**:
   - Ensure the correct COM port is selected in the Arduino IDE.
   - Check that the baud rate is set to **9600**.
2. **Incorrect Data**:
   - The data is randomly generated, so values will vary. If you need consistent data for testing, modify the code to generate fixed values.
