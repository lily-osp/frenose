# E-Nose Project: Detecting and Classifying Smells Using MQ Sensors and Machine Learning

---

## **Table of Contents**
1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Hardware Requirements](#hardware-requirements)
4. [Pinout Map](#pinout-map)
5. [Software Requirements](#software-requirements)
6. [Setup Instructions](#setup-instructions)
7. [How It Works](#how-it-works)
8. [Python (Qt) Interface Features](#python-qt-interface-features)
9. [Arduino Code](#arduino-code)
10. [Training the Model](#training-the-model)
11. [Real-Time Inference](#real-time-inference)
12. [Adding New Smells](#adding-new-smells)
13. [Troubleshooting](#troubleshooting)
14. [Future Enhancements](#future-enhancements)
15. [License](#license)
16. [Folder Structure](#folder-structure)

---

## **Introduction**
The **E-Nose Project** is a system designed to detect and classify smells using an array of **MQ gas sensors** and a **machine learning model**. The system consists of:
- A **microcontroller (MCU)** to read sensor data.
- A **Python (Qt) interface** to record data, train a model, and perform real-time inference.

This project is ideal for applications such as:
- Environmental monitoring.
- Industrial safety.
- Food quality control.
- Home safety (e.g., gas leak detection).

---

## **Project Overview**
The E-Nose system works as follows:
1. **Sensor Data Acquisition**:
   - The MCU reads data from the MQ sensors and sends it to the computer via serial communication.
2. **Data Recording and Filtering**:
   - The Python (Qt) interface records 150 data points per smell and filters them down to 25 points to minimize errors.
3. **Model Training**:
   - The recorded data is used to train an **Artificial Neural Network (ANN)** model.
4. **Real-Time Inference**:
   - The trained model is used to classify smells in real-time based on sensor data.

---

## **Hardware Requirements**
1. **Microcontroller (MCU)**:
   - Any MCU with at least **1 analog pin** (e.g., Arduino Nano, Arduino Mega, ESP32, STM32, etc.).
   - If using more than 1 cluster, ensure the MCU has enough digital pins for multiplexer control.
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
   - Use **CD74HC4067** (16-channel analog multiplexer) if the MCU has limited analog pins.
4. **Connections**:
   - Connect each MQ sensor to the multiplexer (if used) or directly to the MCU’s analog pins.
   - Power the sensors using the 5V and GND pins of the MCU.

---

## **Pinout Map**
### **For Arduino Mega**
| Multiplexer | Control Pins (S0-S3) | Analog Pin | Sensors Connected                     |
|-------------|----------------------|------------|---------------------------------------|
| MUX 1       | D2, D3, D4, D5       | A0         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |
| MUX 2       | D6, D7, D8, D9       | A1         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |
| MUX 3       | D10, D11, D12, D13   | A2         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |
| MUX 4       | D14, D15, D16, D17   | A3         | 1 × MQ-2, 1 × MQ-3, 1 × MQ-4, 1 × MQ-6, 1 × MQ-135, 1 × MQ-136, 1 × MQ-138, 1 × MQ-9 |

### **For Other MCUs**
- Use the same structure, but adjust the pin numbers based on your MCU’s pinout.

---

## **Software Requirements**
1. **Arduino IDE**:
   - To upload the code to the MCU.
2. **Python 3.x**:
   - To run the Python (Qt) interface.
3. **Python Libraries**:
   - Install the required libraries using:
     ```bash
     pip install pyserial numpy pandas scikit-learn PyQt5 matplotlib
     ```

---

## **Setup Instructions**
1. **Upload Arduino Code**:
   - Open the Arduino IDE.
   - Copy and paste the provided Arduino code.
   - Upload the code to the MCU.
2. **Run Python (Qt) Interface**:
   - Open the Python script on your computer.
   - Run the script using:
     ```bash
     python enose_gui.py
     ```
3. **Connect MCU to Computer**:
   - Connect the MCU to the computer via USB.
   - Ensure the correct COM port is selected in the Python script.

---

## **How It Works**
1. **Sensor Data Acquisition**:
   - The MCU reads data from the MQ sensors and sends it to the computer.
2. **Data Recording**:
   - The Python interface records 150 data points for each smell.
3. **Data Filtering**:
   - The recorded data is filtered down to 25 points to minimize errors.
4. **Model Training**:
   - The filtered data is used to train an ANN model.
5. **Real-Time Inference**:
   - The trained model classifies smells in real-time based on sensor data.

---

## **Python (Qt) Interface Features**
1. **Add New Smell Library**:
   - Record and save data for new smells.
2. **Train Model**:
   - Train an ANN model using the recorded data.
3. **Import/Export Model**:
   - Save and load trained models.
4. **Real-Time Inference**:
   - Classify smells in real-time.
5. **Data Logging**:
   - Log sensor data and predictions.
6. **Real-Time Graph**:
   - Visualize sensor data in real-time.

---

## **Arduino Code**
The Arduino code reads data from the MQ sensors and sends it to the computer via serial communication. Refer to the provided Arduino code for details.

---

## **Training the Model**
1. **Record Data**:
   - Use the "Add New Smell Library" feature to record data for each smell.
2. **Train Model**:
   - Click the "Train Model" button to train the ANN model.
3. **Evaluate Model**:
   - The model's accuracy is displayed after training.

---

## **Real-Time Inference**
1. **Start Logging**:
   - Click the "Start Logging" button to begin real-time inference.
2. **View Predictions**:
   - The predicted class is displayed in the GUI.

---

## **Adding New Smells**
1. **Click "Add New Smell Library"**:
   - Enter the name of the new smell.
2. **Record Data**:
   - The system will record 150 data points for the new smell.
3. **Save Data**:
   - Save the filtered data to a CSV file.

---

## **Troubleshooting**
1. **No Data Received**:
   - Check the COM port and ensure the MCU is connected.
2. **Low Accuracy**:
   - Ensure sufficient data is recorded for each smell.
3. **Sensor Errors**:
   - Calibrate the sensors and check connections.

---

## **Future Enhancements**
1. **Advanced Filtering**:
   - Implement more sophisticated filtering techniques.
2. **Data Visualization**:
   - Add real-time plotting of sensor data.
3. **Mobile App**:
   - Develop a mobile app for remote monitoring.

---

## **License**
This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it as needed.

---

## **Folder Structure**
The project is organized as follows:
```
- Readme.md
- enose_gui.py
- dummy_generator (folder)
     - dummy_generator.ino
- sensors_data (folder)
    - single (folder)
        - single.ino
    - cluster (folder)
        - cluster.ino
```

- **`Readme.md`**: This file, containing the project documentation.
- **`enose_gui.py`**: The Python (Qt) interface for data recording, model training, and real-time inference.
- **`dummy_generator`**: Contains the `dummy_generator.ino` file, which simulates sensor data for testing purposes.
- **`sensors_data`**: Contains Arduino code for reading sensor data.
  - **`single`**: Contains `single.ino`, which reads data from multiple sensors (1 sensor per type) without multiplexer.
  - **`cluster`**: Contains `cluster.ino`, which reads data from multiple sensors using a multiplexer.

---
