import sys
import serial
import serial.tools.list_ports
import numpy as np
import pandas as pd
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QComboBox,
    QLineEdit,
    QHBoxLayout,
    QGridLayout,
    QTabWidget,
    QStatusBar,
    QProgressBar,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import joblib
import pyqtgraph as pg

# Global variables
arduino = None  # Serial connection to Arduino
model = None  # Trained ANN model
is_logging = False  # Flag to enable/disable logging
log_data = []  # List to store logged data
smell_libraries = {}  # Dictionary to store smell libraries (key: smell name, value: data)

# Create the "smell_data" directory if it doesn't exist
if not os.path.exists("smell_data"):
    os.makedirs("smell_data")


class E_NoseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the GUI layout and components."""
        self.setWindowTitle("E-Nose System")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("icon.png"))  # Replace with your icon file

        # Apply a modern style
        self.setStyleSheet(self.get_stylesheet())

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Tab widget for different sections
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Initialize tabs
        self.init_control_tab()
        self.init_visualization_tab()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Timer to update the GUI with new predictions
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sensor_data)
        self.timer.start(1000)  # Update every 1 second

        # Initialize data history for plotting
        self.data_history = [[] for _ in range(8)]  # 8 sensors
        self.time_history = []

    def get_stylesheet(self):
        """Return the stylesheet for the application."""
        return """
            QMainWindow { background-color: #2E3440; }
            QLabel { color: #ECEFF4; font-size: 14px; }
            QPushButton { background-color: #4C566A; color: #ECEFF4; border: none; padding: 10px; font-size: 14px; border-radius: 5px; }
            QPushButton:hover { background-color: #5E81AC; }
            QTextEdit { background-color: #3B4252; color: #ECEFF4; border: 1px solid #4C566A; font-size: 14px; border-radius: 5px; }
            QComboBox, QLineEdit { background-color: #3B4252; color: #ECEFF4; border: 1px solid #4C566A; padding: 5px; font-size: 14px; border-radius: 5px; }
            QTabWidget::pane { border: 1px solid #4C566A; background-color: #3B4252; }
            QTabBar::tab { background-color: #4C566A; color: #ECEFF4; padding: 10px; font-size: 14px; border: 1px solid #4C566A; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; }
            QTabBar::tab:selected { background-color: #5E81AC; }
            QProgressBar { background-color: #3B4252; color: #ECEFF4; border: 1px solid #4C566A; border-radius: 5px; text-align: center; }
            QProgressBar::chunk { background-color: #5E81AC; border-radius: 5px; }
        """

    def init_control_tab(self):
        """Initialize the Control tab."""
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)

        # COM port selection
        self.com_port_label = QLabel("Select COM Port:")
        self.tab1_layout.addWidget(self.com_port_label)

        self.com_port_combo = QComboBox()
        self.refresh_com_ports()
        self.tab1_layout.addWidget(self.com_port_combo)

        # Baud rate selection
        self.baud_rate_label = QLabel("Enter Baud Rate:")
        self.tab1_layout.addWidget(self.baud_rate_label)

        self.baud_rate_input = QLineEdit("9600")  # Default baud rate
        self.tab1_layout.addWidget(self.baud_rate_input)

        # Connect/Disconnect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        self.tab1_layout.addWidget(self.connect_button)

        # Labels for sensor data and predictions
        self.sensor_label = QLabel("Sensor Data: None")
        self.prediction_label = QLabel("Predicted Class: None")
        self.tab1_layout.addWidget(self.sensor_label)
        self.tab1_layout.addWidget(self.prediction_label)

        # Text box for logs
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.tab1_layout.addWidget(self.log_text)

        # Buttons for control
        self.control_buttons_layout = QHBoxLayout()
        self.add_control_buttons()
        self.tab1_layout.addLayout(self.control_buttons_layout)

        # Progress bar for recording data
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(150)  # 150 data points
        self.progress_bar.setValue(0)
        self.tab1_layout.addWidget(self.progress_bar)

        # Add tab 1 to the tab widget
        self.tabs.addTab(self.tab1, "Control")

    def add_control_buttons(self):
        """Add control buttons to the Control tab."""
        buttons = [
            ("Train Model", self.train_model),
            ("Import Model", self.import_model),
            ("Export Model", self.export_model),
            ("Start Logging", self.toggle_logging),
            ("Add New Smell Library", self.add_smell_library),
            ("Import Smell Data", self.import_smell_data),
        ]

        for text, callback in buttons:
            button = QPushButton(text)
            button.clicked.connect(callback)
            self.control_buttons_layout.addWidget(button)
            if text == "Start Logging":
                self.log_button = button  # Initialize log_button

    def init_visualization_tab(self):
        """Initialize the Visualization tab."""
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2_layout)

        # PyQtGraph plot widget for real-time data visualization
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("#3B4252")
        self.plot_widget.setLabel("left", "Sensor Value")
        self.plot_widget.setLabel("bottom", "Time")
        self.plot_widget.showGrid(x=True, y=True)
        self.tab2_layout.addWidget(self.plot_widget)

        # Add tab 2 to the tab widget
        self.tabs.addTab(self.tab2, "Visualization")

    def refresh_com_ports(self):
        """Refresh the list of available COM ports."""
        self.com_port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.com_port_combo.addItem(port.device)

    def toggle_connection(self):
        """Connect or disconnect from the Arduino."""
        global arduino
        if arduino and arduino.is_open:
            arduino.close()
            self.connect_button.setText("Connect")
            self.status_bar.showMessage("Disconnected from Arduino.")
        else:
            com_port = self.com_port_combo.currentText()
            baud_rate = int(self.baud_rate_input.text())
            try:
                arduino = serial.Serial(com_port, baud_rate)
                self.connect_button.setText("Disconnect")
                self.status_bar.showMessage(
                    f"Connected to Arduino on {com_port} at {baud_rate} baud."
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to connect: {str(e)}")

    def update_sensor_data(self):
        """Update the GUI with new sensor data and perform inference."""
        if arduino and arduino.is_open and arduino.in_waiting:
            line = arduino.readline().decode("utf-8").strip()
            try:
                sensor_data = list(map(float, line.split(",")))
            except ValueError:
                self.log_text.append(f"Invalid sensor data: {line}")
                return

            if len(sensor_data) != 8:
                self.log_text.append(f"Invalid sensor data length: {len(sensor_data)}")
                return

            self.sensor_label.setText(f"Sensor Data: {sensor_data}")

            if model:
                sensor_data = np.array(sensor_data).reshape(1, -1)
                predicted_class = model.predict(sensor_data)[0]
                self.prediction_label.setText(f"Predicted Class: {predicted_class}")

                if is_logging:
                    # Get the current timestamp
                    timestamp = (
                        QDateTime.currentDateTime().toMSecsSinceEpoch() / 1000.0
                    )  # Convert to seconds
                    log_data.append(
                        [timestamp] + sensor_data.tolist()[0] + [predicted_class]
                    )
                    self.log_text.append(
                        f"Sensor Data: {sensor_data.tolist()}, Predicted Class: {predicted_class}"
                    )
                    self.update_graph(timestamp, sensor_data)

    def update_graph(self, timestamp, sensor_data):
        """Update the data points graph with new sensor data using pyqtgraph."""
        if not is_logging:
            return

        if sensor_data.shape[1] != 8:
            self.log_text.append(f"Invalid sensor data length: {sensor_data.shape[1]}")
            return

        # Append new data to the history
        self.time_history.append(timestamp)  # Use the actual timestamp
        for i in range(8):  # 8 sensors
            self.data_history[i].append(sensor_data[0][i])  # Append new data point

        # Limit the history to the last 25 points
        if len(self.time_history) > 25:
            self.time_history.pop(0)  # Remove the oldest time point
            for i in range(8):
                self.data_history[i].pop(
                    0
                )  # Remove the oldest data point for each sensor

        # Clear the plot and plot the updated data
        self.plot_widget.clear()
        colors = ["r", "g", "b", "c", "m", "y", "k", "w"]  # Colors for each sensor
        sensors = ["MQ-2", "MQ-3", "MQ-4", "MQ-6", "MQ-135", "MQ-136", "MQ-138", "MQ-9"]
        for i in range(8):
            self.plot_widget.plot(
                self.time_history, self.data_history[i], pen=colors[i], name=sensors[i]
            )

    def toggle_logging(self):
        """Toggle logging on/off."""
        global is_logging
        is_logging = not is_logging
        self.log_button.setText("Stop Logging" if is_logging else "Start Logging")
        self.status_bar.showMessage(
            "Logging started." if is_logging else "Logging stopped."
        )

        if not is_logging:
            self.plot_widget.clear()
            self.time_history = []
            self.data_history = [[] for _ in range(8)]

    def train_model(self):
        """Train the model using the loaded smell libraries or saved data."""
        if not smell_libraries:
            QMessageBox.warning(
                self, "No Data", "No smell libraries or saved data loaded!"
            )
            return

        try:
            # Combine data from all smell libraries
            X = []
            y = []
            for smell_name, data in smell_libraries.items():
                X.extend(data)
                y.extend([smell_name] * len(data))

            # Convert to numpy arrays
            X = np.array(X)
            y = np.array(y)

            # Normalize the data
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Train a Random Forest Classifier (you can switch to other models like SVM or MLP)
            global model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Evaluate the model using cross-validation
            cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
            cv_accuracy = np.mean(cv_scores)

            # Evaluate on the test set
            y_pred = model.predict(X_test)
            test_accuracy = accuracy_score(y_test, y_pred)
            classification_rep = classification_report(y_test, y_pred)

            # Show the results to the user
            result_message = (
                f"Model trained successfully!\n"
                f"Cross-Validation Accuracy: {cv_accuracy * 100:.2f}%\n"
                f"Test Set Accuracy: {test_accuracy * 100:.2f}%\n"
                f"Classification Report:\n{classification_rep}"
            )
            QMessageBox.information(self, "Training Complete", result_message)

        except Exception as e:
            QMessageBox.critical(
                self, "Training Failed", f"An error occurred during training: {str(e)}"
            )

    def import_model(self):
        """Import a pre-trained model from a file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Import Model", "", "Model Files (*.pkl)"
        )
        if file_name:
            global model
            model = joblib.load(file_name)
            QMessageBox.information(
                self, "Model Imported", "Model successfully imported!"
            )

    def export_model(self):
        """Export the trained model to a file."""
        if model:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Export Model", "", "Model Files (*.pkl)"
            )
            if file_name:
                joblib.dump(model, file_name)
                QMessageBox.information(
                    self, "Model Exported", "Model successfully exported!"
                )
        else:
            QMessageBox.warning(self, "No Model", "No model to export!")

    def add_smell_library(self):
        """Record and save a new smell library."""
        smell_name, ok = QInputDialog.getText(
            self, "Add New Smell", "Enter smell name:"
        )
        if ok and smell_name:
            self.log_text.append(
                f"Recording 150 data points for smell: {smell_name}..."
            )
            recorded_data = []
            self.progress_bar.setValue(0)

            for i in range(150):
                while arduino and arduino.in_waiting == 0:
                    QApplication.processEvents()

                if arduino and arduino.in_waiting:
                    line = arduino.readline().decode("utf-8").strip()
                    sensor_data = list(map(float, line.split(",")))

                    if len(sensor_data) != 8 or any(np.isnan(sensor_data)):
                        self.log_text.append(
                            "Invalid sensor data detected. Skipping this point..."
                        )
                        continue

                    recorded_data.append(sensor_data)
                    self.log_text.append(f"Recorded: {sensor_data}")
                    self.progress_bar.setValue(i + 1)
                    QApplication.processEvents()

            if len(recorded_data) == 150:
                filtered_data = []
                for i in range(0, 150, 6):
                    chunk = recorded_data[i : i + 6]
                    avg_point = np.mean(chunk, axis=0).tolist()
                    filtered_data.append(avg_point)

                file_name = os.path.join("smell_data", f"{smell_name}.csv")
                pd.DataFrame(filtered_data).to_csv(file_name, index=False)
                smell_libraries[smell_name] = filtered_data
                self.log_text.append(
                    f"Smell library '{smell_name}' saved to {file_name}."
                )
            else:
                self.log_text.append("Recording failed. Please try again.")

    def import_smell_data(self):
        """Import smell data from a CSV file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Import Smell Data", "", "CSV Files (*.csv)"
        )
        if file_name:
            try:
                smell_name = os.path.splitext(os.path.basename(file_name))[0]
                data = pd.read_csv(file_name).values.tolist()
                smell_libraries[smell_name] = data
                self.log_text.append(
                    f"Smell data for '{smell_name}' imported successfully."
                )
                QMessageBox.information(
                    self,
                    "Import Successful",
                    f"Smell data for '{smell_name}' imported successfully.",
                )
            except Exception as e:
                self.log_text.append(f"Failed to import smell data: {str(e)}")
                QMessageBox.critical(
                    self, "Import Failed", f"Failed to import smell data: {str(e)}"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = E_NoseGUI()
    window.show()
    sys.exit(app.exec_())
