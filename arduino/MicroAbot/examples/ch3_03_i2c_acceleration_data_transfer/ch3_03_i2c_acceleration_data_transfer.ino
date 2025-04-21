#include <Wire.h>
volatile int receivedData = 0;  // Variable to store received data

void setup() {
  Wire.begin(0x08);              // Set I2C address
  Wire.onRequest(requestEvent);  // Set data request event
  Wire.onReceive(receiveEvent);  // Set data receive event
  Serial.begin(9600);
}

void loop() {
  delay(100);
}

void requestEvent() {
  // Send the received data
  Wire.write((byte*)&receivedData, sizeof(receivedData));
}

void receiveEvent(int howMany) {
  if (howMany >= sizeof(receivedData)) {
    receivedData = 0;
    for (int i = 0; i < howMany; i++) {
      char c = Wire.read();  // Read the received data
      if (c >= '0' && c <= '9') {
        receivedData = receivedData * 10 + (c - '0');  // Convert ASCII number to integer
      }
    }
    Serial.print("Received data: ");
    Serial.println(receivedData);  // Print the received data to the serial monitor
  }
}
