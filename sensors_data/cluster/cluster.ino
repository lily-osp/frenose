/*
  Generalized E-Nose System Code for 1 to 8 Clusters
  - Supports 1 to 8 clusters, each with 8 different MQ sensors.
  - Averages the readings for each sensor type across all clusters.
  - Sends the averaged data to the computer via serial communication.
  - Works with any MCU that has at least 1 analog pin (using multiplexers).
*/

// Number of clusters (1 to 8)
const int NUM_CLUSTERS = 4; // Change this value based on your setup

// Multiplexer control pins for each cluster
const int MUX_PINS[8][4] = {
    { 2, 3, 4, 5 }, // Cluster 1 control pins (S0-S3)
    { 6, 7, 8, 9 }, // Cluster 2 control pins (S0-S3)
    { 10, 11, 12, 13 }, // Cluster 3 control pins (S0-S3)
    { 14, 15, 16, 17 }, // Cluster 4 control pins (S0-S3)
    { 18, 19, 20, 21 }, // Cluster 5 control pins (S0-S3)
    { 22, 23, 24, 25 }, // Cluster 6 control pins (S0-S3)
    { 26, 27, 28, 29 }, // Cluster 7 control pins (S0-S3)
    { 30, 31, 32, 33 } // Cluster 8 control pins (S0-S3)
};

// Analog pins for multiplexer outputs
const int MUX_ANALOG[8] = { A0, A1, A2, A3, A4, A5, A6, A7 }; // Analog pins for clusters 1-8

void setup()
{
    Serial.begin(9600); // Initialize serial communication

    // Set multiplexer control pins as outputs
    for (int cluster = 0; cluster < NUM_CLUSTERS; cluster++) {
        for (int i = 0; i < 4; i++) {
            pinMode(MUX_PINS[cluster][i], OUTPUT);
        }
    }
}

void loop()
{
    // Arrays to store summed readings for each sensor type
    float mq2_sum = 0, mq3_sum = 0, mq4_sum = 0, mq6_sum = 0;
    float mq135_sum = 0, mq136_sum = 0, mq138_sum = 0, mq9_sum = 0;

    // Read data from all clusters
    for (int cluster = 0; cluster < NUM_CLUSTERS; cluster++) {
        mq2_sum += readSensor(cluster, 0); // MQ-2
        mq3_sum += readSensor(cluster, 1); // MQ-3
        mq4_sum += readSensor(cluster, 2); // MQ-4
        mq6_sum += readSensor(cluster, 3); // MQ-6
        mq135_sum += readSensor(cluster, 4); // MQ-135
        mq136_sum += readSensor(cluster, 5); // MQ-136
        mq138_sum += readSensor(cluster, 6); // MQ-138
        mq9_sum += readSensor(cluster, 7); // MQ-9
    }

    // Calculate averages
    float mq2_avg = mq2_sum / NUM_CLUSTERS;
    float mq3_avg = mq3_sum / NUM_CLUSTERS;
    float mq4_avg = mq4_sum / NUM_CLUSTERS;
    float mq6_avg = mq6_sum / NUM_CLUSTERS;
    float mq135_avg = mq135_sum / NUM_CLUSTERS;
    float mq136_avg = mq136_sum / NUM_CLUSTERS;
    float mq138_avg = mq138_sum / NUM_CLUSTERS;
    float mq9_avg = mq9_sum / NUM_CLUSTERS;

    // Send averaged data to the computer
    Serial.print(mq2_avg);
    Serial.print(","); // MQ-2
    Serial.print(mq3_avg);
    Serial.print(","); // MQ-3
    Serial.print(mq4_avg);
    Serial.print(","); // MQ-4
    Serial.print(mq6_avg);
    Serial.print(","); // MQ-6
    Serial.print(mq135_avg);
    Serial.print(","); // MQ-135
    Serial.print(mq136_avg);
    Serial.print(","); // MQ-136
    Serial.print(mq138_avg);
    Serial.print(","); // MQ-138
    Serial.println(mq9_avg); // MQ-9

    delay(1000); // Send data every second
}

// Function to read a specific sensor from a cluster
float readSensor(int cluster, int channel)
{
    selectMuxChannel(cluster, channel); // Select the channel
    return analogRead(MUX_ANALOG[cluster]); // Read the sensor value
}

// Function to select a multiplexer channel
void selectMuxChannel(int cluster, int channel)
{
    for (int i = 0; i < 4; i++) {
        digitalWrite(MUX_PINS[cluster][i], bitRead(channel, i)); // Set control pins based on channel
    }
}
