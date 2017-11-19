/*
  Arduino Starter Kit example
  Project 9 - Motorized Pinwheel

  This sketch is written to accompany Project 9 in the Arduino Starter Kit

  Parts required:
  - 10 kilohm resistor
  - pushbutton
  - motor
  - 9V battery
  - IRF520 MOSFET
  - 1N4007 diode

  created 13 Sep 2012
  by Scott Fitzgerald

  http://www.arduino.cc/starterKit

  This example code is part of the public domain.
*/

// named constants for the switch and motor pins
const int motorPinR1 =  9; // the number of the motor pin
const int motorPinR2 =  10; // the number of the motor pin

const int motorPinL1 =  5; // the number of the motor pin
const int motorPinL2 =  3; // the number of the motor pi

int switchState = 0;  // variable for reading the switch's status

void robotStop() {
  Serial.begin(9600);
  analogWrite(motorPinR1, 0);
  analogWrite(motorPinR2, 0);
  
  analogWrite(motorPinL1, 0);
  analogWrite(motorPinL2, 0);
}

void setup() {
  // initialize the motoas an output:
  pinMode(motorPinR1, OUTPUT);
  pinMode(motorPinR2, OUTPUT);
  
  pinMode(motorPinL1, OUTPUT);
  pinMode(motorPinL2, OUTPUT);
  
  robotStop();
}

void moveRForward(float speed) {
  float k = (255 * speed) / 2;
  analogWrite(motorPinR1, (255/2) + k);
  analogWrite(motorPinR2, (255/2) - k);
}

void moveLForward(float speed) {
  float k = (255 * speed) / 2;
  analogWrite(motorPinL1, (255/2) + k);
  analogWrite(motorPinL2, (255/2) - k);
}

void moveRBackward(float speed) {
  moveRForward(-1 * speed);
}

void moveLBackward(float speed) {
  moveLForward(-1 * speed);
}

void moveForward(float speed) {
  moveRForward(speed);
  delay(10);
  moveLForward(speed);
  delay(10);
}

void moveBackward(float speed) {
  moveRBackward(speed);
  delay(10);
  moveLBackward(speed);
  delay(10);
}

void turnLeft(float speed) {
  moveRForward(speed);
  delay(10);
  moveLBackward(speed);
  delay(10);
}

void turnRight(float speed) {
  moveLForward(speed);
  delay(10);
  moveRBackward(speed);
  delay(10);
}

void forward(int i) {
  moveForward(0.4);
  delay(500);
  robotStop();
}

void back(int i) {
  moveBackward(0.4);
  delay(500);
  robotStop();
}

void left(int i) {
  turnLeft(0.4);
  delay(350);
  robotStop();
}

void right(int i) {
  turnRight(0.4);
  delay(350);
  robotStop();
}

void loop() {
  if (Serial.available()) {
	  int input = Serial.read(); // ascii of '0'
	  if(input == 1) {
	    forward(1);
	  } else if (input == 2) {
	    back(1);
	  } else if (input == 3) {
	    right(1);
	  } else if (input == 4) {
	    left(1);
	  }
		//do stuff with the input here
	}
  delay(500);
}
