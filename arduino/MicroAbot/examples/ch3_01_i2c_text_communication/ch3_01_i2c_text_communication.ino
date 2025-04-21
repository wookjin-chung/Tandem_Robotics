#include <Wire.h>
char received_char;
bool new_data = false;

void setup() {
  Wire.begin(0x08);  // Set I2C address
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);
}
void loop() {
  delay(100);
  if (new_data) {
    Serial.print("Received: ");
    Serial.println(received_char);
    new_data = false;
  }
}

void receiveEvent(int howMany) {
  while (Wire.available()) {
    received_char = Wire.read();
    new_data = true;
  }
}
void requestEvent() {
  if (received_char == 'A') {
    Wire.write('B');  // after receive 'A', return 'B'
  }
}