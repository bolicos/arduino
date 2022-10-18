const int act_num=2;
const int sen_num=1;

class ASensor { // analog sensor (ldr, temp, ...)
  private:
    byte pin;

  public:
  	ASensor() {}

  	void begin(byte pin) {
      this->pin = pin;
    }

	int getValue() {
  		return(analogRead(pin));
    }
};

class Actuator { // actuator (led or led_RGB)
  private:
  	byte pin;

  public:
    Actuator(){}

  void begin(byte pin) {
      this->pin=pin;
      pinMode(pin, OUTPUT);
    }

	int setValue(int val) {
      int map_val;
      map_val = map(val, 0, 1023, 0, 255);
      analogWrite(pin, val);
    }
};

class Button {
  private:
    byte pin;
    byte state;
    byte lastReading;
    unsigned long lastDebounceTime = 0;
    unsigned long debounceDelay = 50;

  public:
  	Button(){}

  	void begin(byte pin) {
      this->pin = pin;
      lastReading = LOW;
      init();
    }

    void init() {
      pinMode(pin, INPUT);
    }

    void update() {
      byte newReading = digitalRead(pin);
      if (newReading != lastReading) lastDebounceTime = millis();
      if (millis() - lastDebounceTime > debounceDelay) state = newReading;
      lastReading = newReading;
    }

    byte getState() {
      update();
      return state
      ;
    }

    bool isPressed() {
      return (getState() == HIGH);
    }
};

Button button;
ASensor sensor[sen_num];
ASensor pot[act_num];
Actuator act[act_num];

int buttonVal;
int sensorVal[sen_num];
int actuatorVal[act_num];
int minDiff;
int newDiff;
int trainingNum, buttonCounter = 0;
bool buttonPressed, buttonHeld, trainingDone = false;
const int ELEMENT_COUNT_MAX = 50;
int sensorArray[ELEMENT_COUNT_MAX][sen_num];
int actuatorArray[ELEMENT_COUNT_MAX][act_num];

void setup() {
  button.begin(7);

  for (int i = 0; i < sen_num; i++){
    sensor[i].begin(A0+i);
  }

  for(int i = 0; i < act_num; i++){
  	pot[i].begin(A3+i);
  	act[i].begin(9+i);
  }

  Serial.begin(9600);
  Serial.println("running");
}

void loop() {
  buttonVal = button.isPressed();

  for (int i = 0; i < sen_num; i++) {
    sensorVal[i] = sensor[i].getValue();
  }

  for(int i = 0; i < act_num; i++){
 	  actuatorVal[i] = pot[i].getValue();
  }

  if (buttonVal) buttonCounter++;
  else buttonCounter = 0;

  buttonHeld = (buttonVal and buttonCounter > 15);
  buttonPressed = (buttonVal and not buttonHeld);

  if (buttonHeld) {
	  trainingDone = true;
    Serial.println("button held");
    buttonCounter = 0;
  }

  if (trainingDone) {
    int closestPos = 0;
    minDiff = 0;

    for (int i = 0; i < sen_num; i++){
      minDiff = minDiff + abs(sensorArray[0][i] - sensorVal[i]);
    }

    for (int i = 1; i < trainingNum; i++) {
     newDiff = 0;

      for (int j = 0; j < sen_num; j++){
        newDiff = newDiff+abs(sensorArray[i][j] - sensorVal[j]);
      }

      if (newDiff < minDiff) {
        minDiff = newDiff;
        closestPos = i;
      }
    }


    for(int i = 0; i < act_num; i++){
		    act[i].setValue(actuatorArray[closestPos][i]);
    }

  } else if (buttonPressed) {
    for (int i = 0; i < sen_num; i++){
      sensorArray[trainingNum][i] = sensorVal[i];
    }

    for(int i = 0; i < act_num; i++){
      actuatorArray[trainingNum][i] = actuatorVal[i];
    }

    trainingNum++;
  } else {
    for(int i = 0; i < act_num; i++){
      act[i].setValue(actuatorVal[i]);
    }

  }

  delay(30);
}
