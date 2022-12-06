#include <Servo.h>

class ASensor
{
private:
    byte pin;

public:
    ASensor(byte pin)
    {
        this->pin = pin;
    }
    int getValue()
    {
        return (analogRead(pin));
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
    Button(byte pin)
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
        if (newReading != lastReading)
        {
            lastDebounceTime = millis();
        }
        if (millis() - lastDebounceTime > debounceDelay)
        {
            state = newReading;
        }
        lastReading = newReading;
    }
    byte getState()
    {
        update();
        return state;
    }
    bool isPressed()
    {
        return (getState() == HIGH);
    }
};

class Actuator
{
private:
    byte pin;
    Servo servo;

public:
    Actuator(byte pin)
    {
        this->pin = pin;
    }
    void begin()
    {
        servo.attach(pin);
    }
    int setValue(int val)
    {
        val = map(val, 0, 1023, 0, 180);
        servo.write(val);
    }
};

// ******************************
// *         objetos            *
// ******************************
ASensor sensor(A0);
ASensor pot(A1);
Button button(7);
Actuator act(3);

// ******************************
// definicoes de variaveis fixas
// ******************************
int sensorVal;
int actuatorVal;
int buttonVal;

int buttonCounter = 0; // contador para ver se botao foi mantido pressionado
int trainingNum = 0;   // nro de estados armazenados

bool buttonPressed = false; // botao foi pressionado e solto
bool buttonHeld = false;    // botao permaneceu pressionado por um tempo (15 ciclos de 30 ms ≃ 1/2 segundo)
bool trainingDone = false;  // indicador de finalizacao da fase de treinamento

const int ELEMENT_COUNT_MAX = 50;     // tamanho maximo do vetor de treinamento
int sensorArray[ELEMENT_COUNT_MAX];   // vetor de estados do sensor
int actuatorArray[ELEMENT_COUNT_MAX]; // vetor de estados do atuador

// ******************************
// *           setup            *
// ******************************

void setup()
{
    act.begin();        // ao usar servo, preciso fazer iss no setup (conectar porta ao servo)
    Serial.begin(9600); // debug (monitor serial)
    Serial.println("running");
}

// ******************************
// *           loop             *
// ******************************

void loop()
{
    buttonVal = button.isPressed(); // le o estado do botao... se o botao estiver pressionado -> buttonVal = 1
    sensorVal = sensor.getValue();  // le o valor atual do sensor
    actuatorVal = pot.getValue();   // le o valor atual do controle (potenciometro)

    if (buttonVal)
        buttonCounter++; // para identificar o "held" de 15 ciclos
    else
        buttonCounter = 0;

    buttonHeld = (buttonVal and buttonCounter > 15);
    buttonPressed = (buttonVal and not buttonHeld);

    if (buttonHeld)
    {
        trainingDone = true;
        Serial.println("button held");
        buttonCounter = 0;
    }

    if (trainingDone)
    {
        int closestPos = 0;                            // busca pela menor diferenca nas amostras de estado
        int minDiff = abs(sensorArray[0] - sensorVal); // referencia inicial = pos[0]
        for (int i = 1; i < trainingNum; i++)
        {
            if (abs(sensorArray[i] - sensorVal) < minDiff)
            {
                minDiff = abs(sensorArray[i] - sensorVal);
                closestPos = i;
            }
        }
        act.setValue(actuatorArray[closestPos]);
    }
    else if (buttonPressed)
    {                                             // ainda estah treinando e o botao foi pressionado
        sensorArray[trainingNum] = sensorVal;     // guarda o valor do sensor
        actuatorArray[trainingNum] = actuatorVal; // guarda o valor do atuador
        trainingNum++;                            // incrementa o tamanho do vetor
    }
    else
    {                              // se ainda estah treinando, mas o botao estah solto
        act.setValue(actuatorVal); // altera o valor do atuador (muda de posicao durante o treinamento)
    }

    delay(30); // aguarda 30 ms - fim do loop
}