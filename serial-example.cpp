void setup(){
	// setup code here
}

void loop(){
	if (Serial.available()) {
	  input = Serial.read() – ‘0’;
		//do stuff with the input here
	}
	delay(500);
}

