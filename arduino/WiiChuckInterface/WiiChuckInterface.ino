#include "Wire.h"
#include "./WiiChuck.h"

#include <math.h>

#define MAXANGLE 90
#define MINANGLE -90

WiiChuck nunchuk1 = WiiChuck();
WiiChuck nunchuk2 = WiiChuck();

//Transistor base pins
int NUNCHUK1 = 8;
int NUNCHUK2 = 9;

int DELAY = 5;

void setup() {
  Serial.begin(115200);
  
  //Turn both Nunchuks on for init
  digitalWrite(NUNCHUK1, HIGH);
  digitalWrite(NUNCHUK2, LOW);
  nunchuk1.begin();
  nunchuk1.update();
  delay(DELAY);
  
  digitalWrite(NUNCHUK1, LOW);
  digitalWrite(NUNCHUK2, HIGH);
  nunchuk2.begin();
  nunchuk2.update();
  delay(DELAY);
  
}

void loop() {
  
  //Nunchuk 1
  delay(DELAY);
  digitalWrite(NUNCHUK1, HIGH);
  digitalWrite(NUNCHUK2, LOW);
  nunchuk1.update();
  
  int roll1 = nunchuk1.readRoll();
  int y1 = nunchuk1.readAccelY();
  
  //Nunchuk 2
  delay(DELAY);
  digitalWrite(NUNCHUK1, LOW);
  digitalWrite(NUNCHUK2, HIGH);
  nunchuk2.update();
  
  int roll2 = nunchuk2.readRoll();
  int y2 = nunchuk2.readAccelY();
  
  Serial.print(roll1);
  Serial.print(",");  
  Serial.print(y1);
  Serial.print("|");
  Serial.print(roll2);
  Serial.print(",");  
  Serial.print(y2);
  Serial.print("\n");
}
