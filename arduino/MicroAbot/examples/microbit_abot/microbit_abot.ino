#include <MicroAbot.h>

MicroAbot abot;
void setup() {
  Serial.begin(9600);
  abot.setup();
}

void loop() {
  abot.loop();
}