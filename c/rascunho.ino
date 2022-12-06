// Arduino UNO Board Pins
//
// Sensors pins: A0, A1, A2.
// Sensors (Potentiometer) pins: A3, A4, A5.
// Actuators (Commons) pins: 9, 10, 11.
// Button pin: 7.

const int BAUD_RATE = 9600;
const int ELEMENT_COUNT_MAX = 50;

const int PIN_BUTTON = 7;
const int PIN_ACTUATORS_INIT = 9;
const unsigned int PIN_SENSORS_INIT = A0;
const unsigned int PIN_SENSORS_POTENTIOMETER_INIT = A3;

const int QTD_ACTUATORS = 1;
const int QTD_SENSORS = 1;

class Sensor
{
private:
  byte pin;

public:
  Sensor() {}

  void begin(byte pin)
  {
    this->pin = pin;
  }

  int getValue()
  {
    return analogRead(pin);
  }
};

class Actuator
{
private:
  byte pin;

public:
  Actuator() {}

  void begin(byte pin)
  {
    this->pin = pin;
    pinMode(pin, OUTPUT);
  }

  int setValue(int val)
  {
    analogWrite(pin, val);
  }
};

class Button
{
private:
  byte pin;
  byte state;
  byte lastReading;
  unsigned long lastDebounceTime = 0;
  unsigned long debounceDelay = 50;

public:
  Button() {}

  void begin(byte pin)
  {
    this->pin = pin;
    lastReading = LOW;
    init();
  }

  void init()
  {
    pinMode(pin, INPUT);
  }

  void update()
  {
    byte newReading = digitalRead(pin);

    if (newReading != lastReading) lastDebounceTime = millis();
    if (millis() - lastDebounceTime > debounceDelay) state = newReading;

    lastReading = newReading;
  }

  byte getState()
  {
    update();
    return state;
  }

  bool isPressed()
  {
    bool isStateHigh = getState() == HIGH;
    return isStateHigh;
  }
};

Button button;
Sensor sensors[QTD_SENSORS];
Sensor potentiometers[QTD_ACTUATORS];
Actuator actuators[QTD_ACTUATORS];

int minDiff;
int newDiff;
int isPressedButton;
int sensorValue[QTD_SENSORS];
int actuatorValue[QTD_ACTUATORS];
int trainingQtd, buttonCounter = 0;
int sensorArray[ELEMENT_COUNT_MAX][QTD_SENSORS];
int actuatorArray[ELEMENT_COUNT_MAX][QTD_ACTUATORS];

bool buttonPressed, buttonHeld, trainingDone = false;

void setup()
{
  button.begin(PIN_BUTTON);

  for (int index = 0; index < QTD_SENSORS; index++)
  {
    sensors[index].begin(PIN_SENSORS_INIT + index);
  }

  for (int index = 0; index < QTD_ACTUATORS; index++)
  {
    potentiometers[index].begin(PIN_SENSORS_POTENTIOMETER_INIT + index);
    actuators[index].begin(PIN_ACTUATORS_INIT + index);
  }

  Serial.begin(BAUD_RATE);
  Serial.println("Setup");
}

void loop()
{
  isPressedButton = button.isPressed();

  for (int index = 0; index < QTD_SENSORS; index++)
  {
    sensorValue[index] = sensors[index].getValue();
  }

  for (int index = 0; index < QTD_ACTUATORS; index++)
  {
    actuatorValue[index] = potentiometers[index].getValue();
  }

  if (isPressedButton) buttonCounter++;
  else buttonCounter = 0;

  buttonHeld = (isPressedButton and buttonCounter > 15);
  buttonPressed = (isPressedButton and not buttonHeld);

  if (buttonHeld)
  {
    trainingDone = true;
    Serial.println("Button Held");
    buttonCounter = 0;
  }

  if (trainingDone)
  {
    int closestPos = 0;
    minDiff = 0;

    for (int index = 0; index < QTD_SENSORS; index++)
    {
      minDiff = minDiff + abs(sensorArray[0][index] - sensorValue[index]);
    }

    for (int index = 1; index < trainingQtd; index++)
    {
      newDiff = 0;

      for (int auxiliar = 0; auxiliar < QTD_SENSORS; auxiliar++)
      {
        newDiff = newDiff + abs(sensorArray[index][auxiliar] - sensorValue[auxiliar]);
      }

      if (newDiff < minDiff)
      {
        minDiff = newDiff;
        closestPos = index;
      }
    }

    for (int index = 0; index < QTD_ACTUATORS; index++)
    {
      actuators[index].setValue(actuatorArray[closestPos][index]);
    }
  }
  else if (buttonPressed)
  {
    for (int index = 0; index < QTD_SENSORS; index++)
    {
      sensorArray[trainingQtd][index] = sensorValue[index];
    }

    for (int index = 0; index < QTD_ACTUATORS; index++)
    {
      actuatorArray[trainingQtd][index] = actuatorValue[index];
    }

    trainingQtd++;
  }
  else
  {
    for (int index = 0; index < QTD_ACTUATORS; index++)
    {
      actuators[index].setValue(actuatorValue[index]);
    }
  }

  delay(30);
}
