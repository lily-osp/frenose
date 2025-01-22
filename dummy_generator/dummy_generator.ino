/*
  Arduino Code for E-Nose System (Dummy Data)
  - Generates random sensor values for testing purposes.
  - Sends the dummy data to the computer via serial communication.
*/

void setup()
{
    Serial.begin(9600); // Initialize serial communication at 9600 baud rate
    randomSeed(analogRead(0)); // Seed the random number generator
}

void loop()
{
    // Generate random sensor values (8 sensors)
    int mq2 = random(0, 1024); // MQ-2: Random value between 0 and 1023
    int mq3 = random(0, 1024); // MQ-3: Random value between 0 and 1023
    int mq4 = random(0, 1024); // MQ-4: Random value between 0 and 1023
    int mq6 = random(0, 1024); // MQ-6: Random value between 0 and 1023
    int mq135 = random(0, 1024); // MQ-135: Random value between 0 and 1023
    int mq136 = random(0, 1024); // MQ-136: Random value between 0 and 1023
    int mq138 = random(0, 1024); // MQ-138: Random value between 0 and 1023
    int mq9 = random(0, 1024); // MQ-9: Random value between 0 and 1023

    // Send dummy data to the computer
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
