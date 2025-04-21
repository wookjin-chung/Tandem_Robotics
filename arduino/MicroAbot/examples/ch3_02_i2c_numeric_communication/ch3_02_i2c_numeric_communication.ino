#include <Wire.h>
int received_number;
bool new_data = false;

void setup() {
  Wire.begin(0x08);  // set I2C address
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);
}
void loop() {
  delay(100);
  if (new_data) {
    Serial.print("Received: ");
    Serial.println(received_number);
    new_data = false;
  }
}
void receiveEvent(int howMany) {
  while (Wire.available()) {
    received_number = Wire.read();
    new_data = true;
  }
}
void requestEvent() {
  int response_number = received_number + 10;  // Add 10 to the number you received
  Wire.write(response_number);
}
