import time
from machine import ADC, Pin, PWM, Signal

# Constants ==========================================
TRAINING_MODE = False
BUILD_LED_PIN = 25
LED_PIN = 7
POTENTIOMETER_PI = 5
TRAINING_MODE_BUTTON = 9
CONFIRM_BUTTON = 10

# Classes ==========================================
class Led:    
    def __init__(self, value):
        self.pin = Pin(value, Pin.OUT)
        self.signal = Signal(self.pin, invert=False)

    def enable(self):
        self.signal.on()

    def disable(self):
        self.signal.off()

    def invert(self):
        print(self.signal.value())

class Button:
    def __init__(self, value):
        self.pin = Pin(value, Pin.IN)

    def is_pressed(self):
        return self.pin.value() == 1

class Potentiometer:
    def __init__(self, value):
        self.adc = ADC(value)

    def getValue(self):
        return self.adc.read()

class Servo:
    def __init__(self, value):
        self.pin = Pin(value, Pin.OUT)
        self.pwd = PWM(self.pin, freq=50)

    def getPosition(self):
        self.pwd.duty()

    def setPosition(self, value):
        self.pwd.duty(value)

class Ldr:
    def __init__(self, value):
        self.adc = ADC(value)

    def getValue(self):
        return self.adc.read()

# FUNCTIONS ==========================================
def main():
    print('===========================================')
    print('Welcome!')

def loop():
    global TRAINING_MODE

    main()

    led = Led(LED_PIN)
    training_mode_button = Button(TRAINING_MODE_BUTTON)

    is_change_mode = training_mode_button.is_pressed()

    if (is_change_mode): led.invert()
    if (led.pin.value() == 1): TRAINING_MODE = True
    else: TRAINING_MODE = False

    time.sleep(0.1)
    print(TRAINING_MODE)

    if (TRAINING_MODE):
        print('TRAINING_MODE')

def servo():
    servo = Servo(POTENTIOMETER_PI)
    servo.setPosition(40)
    servo.setPosition(77)
    servo.setPosition(115)

def led():
    led = Led(2)
    led.enable()
    led.disable()

def ldr():
    ldr = Ldr(0)
    value = ldr.getValue()
    print(value)
    time.sleep(0.2)

def potentiometer():
    ldr = Potentiometer(0)
    value = ldr.getValue()
    print(value)
    time.sleep(0.2)


# MAIN ==========================================
while True:
    main()
    # loop()
    # servo()
    # led()
    # ldr()
    # potentiometer()






# ==========================================    CONVENCOES PYTHON  ==========================================
# Módulos/pacotes               =   caracteres minúsculos                   =   projetopython
# Métodos/funções/variáveis     =   minúsculos_separados_por_underlines     =   variavel_aleatoria
# Globais/constantes            =   maiúsculos_separados_por_underlines     =   CONSTANTE
# Classes                       =   Iniciais Maiúsculas                     =   NormalDistribution


# D0 = GPIO_16
# D1 = GPIO_5
# D2 = GPIO_4
# D3 = GPIO_0
# D4 = GPIO_2
# D5 = GPIO_14
# D6 = GPIO_12
# D7 = GPIO_13
# D8 = GPIO_15
# RX = GPIO_3
# TX = GPIO_1