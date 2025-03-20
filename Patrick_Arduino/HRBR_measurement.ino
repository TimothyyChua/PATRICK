#include "Arduino.h"
#include <60ghzbreathheart.h>
#include <SoftwareSerial.h>

// Choose any two pins that can be used with SoftwareSerial to RX & TX
#define RX_Pin A3
#define TX_Pin A2
#define DATASIZE 30
#define DURATION 150

SoftwareSerial mySerial = SoftwareSerial(RX_Pin, TX_Pin);

// we'll be using software serial
BreathHeart_60GHz radar = BreathHeart_60GHz(&mySerial);

int heartrate_data[DATASIZE] = {0};
int breathrate_data[DATASIZE] = {0};
bool isRecording = false;
bool finishRecording = false;
int i = 0;
int j = 0;
int k = 0;
float average_heartrate = 0;
float average_breathrate = 0;

float CalculateAverage(int data[], int dataSize) {
    int sum = 0;
    int count = 0;
    for (int a = 0; a < dataSize; a++) {
        if (data[a] != 0) {  // Ignore 0 values
            sum += data[a];
            count++;
        }
    }

    float average = 0;
    if (count > 0) {
        average = (float)sum / count;
    }
    return average;
}

void setup() {
    // put your setup code here, to run once:
    Serial.begin(115200);
    mySerial.begin(115200);
    radar.ModeSelect_fuc(1);

//    Serial.println("Ready");

//    pinMode(2, OUTPUT);
//    digitalWrite(2, LOW);
}

void loop() {
    if (!isRecording) {
        memset(heartrate_data, 0, sizeof(heartrate_data));
        memset(breathrate_data, 0, sizeof(breathrate_data));
        i = 0;
        j = 0;
        k = 0;
        isRecording = true;
        finishRecording = false;
    }

    if (isRecording) {
        // Measure points
        radar.Breath_Heart();

        if (radar.sensor_report != 0x00) {
            switch (radar.sensor_report) {
                case HEARTRATEVAL:
                    if (i < DATASIZE) {
                        heartrate_data[i] = radar.heart_rate;
                        i++;
                    }
//                    Serial.print("Sensor monitored the current heart rate value is: ");
//                    Serial.println(radar.heart_rate, DEC);
                    break;

                case BREATHVAL:
                    if (j < DATASIZE) {
                        breathrate_data[j] = radar.breath_rate;
                        j++;
                    }
//                   Serial.print("Sensor monitored the current breath rate value is: ");
//                    Serial.println(radar.breath_rate, DEC);
                    break;
            }
        }
        k++;
    }

    if (k >= DURATION || i >= DATASIZE || j >= DATASIZE) {
//        Serial.println("Calculating Averages");
        average_heartrate = CalculateAverage(heartrate_data, DATASIZE);
        average_breathrate = CalculateAverage(breathrate_data, DATASIZE);
        finishRecording = true;
    }

    if (finishRecording) {
      String a_heartrate = String(average_heartrate, 2); // Convert float to String with 2 decimal places
      String a_breathrate = String(average_breathrate, 2); // Convert float to String with 2 decimal places
//        Serial.println("===================================================");
//        Serial.print("Average Heart Rate: ");
        Serial.println("Heartrate:" + a_heartrate + "," + "Breathrate:" + a_breathrate);
//        Serial.print("Average Breath Rate: ");
//        Serial.println(average_breathrate);
//        Serial.println("===================================================");
        isRecording = false;
        finishRecording = false;
    }

    delay(200);
}
