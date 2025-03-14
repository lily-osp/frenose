/*
  Arduino Code for E-Nose System (Real Sensor Data)
  - Reads data from 8 MQ sensors connected to analog pins A0-A7.
  - Sends the sensor data to the computer via serial communication.
*/

void setup()
{
    Serial.begin(9600); // Initialize serial communication at 9600 baud rate
}

void loop()
{
    // Read sensor data from analog pins
    int mq2 = analogRead(A0); // MQ-2
    int mq3 = analogRead(A1); // MQ-3
    int mq4 = analogRead(A2); // MQ-4
    int mq6 = analogRead(A3); // MQ-6
    int mq135 = analogRead(A4); // MQ-135
    int mq136 = analogRead(A5); // MQ-136
    int mq138 = analogRead(A6); // MQ-138
    int mq9 = analogRead(A7); // MQ-9

    // Send sensor data to the computer
    Serial.print(mq2);
    Serial.print(","); // MQ-2
    Serial.print(mq3);
    Serial.print(","); // MQ-3
    Serial.print(mq4);
    Serial.print(","); // MQ-4
    Serial.print(mq6);
    Serial.print(","); // MQ-6
    Serial.print(mq135);
    Serial.print(","); // MQ-135
    Serial.print(mq136);
    Serial.print(","); // MQ-136
    Serial.print(mq138);
    Serial.print(","); // MQ-138
    Serial.println(mq9); // MQ-9

    delay(1000); // Send data every second
}
