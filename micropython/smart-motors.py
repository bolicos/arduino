# Raspberry Pi Pico Board Pins
#
# Sensors pins: A0 - 31.
# Sensors (Potentiometer) pins: A1 - 32.
# Actuators (Commons) pins: 5, 6, 7 - GPIO3, GPIO4 e GPIO5.
# Button pin: 2 - GPIO1.

import time
from machine import ADC, Pin, PWM, Signal

# Constants ==========================================
BAUD_RATE = 9600
ELEMENT_COUNT_MAX = 50

PIN_BUTTON = 2
PIN_SENSORS_INIT = 31
PIN_SENSORS_POTENTIOMETER_INIT = 32
PIN_ACTUATORS_INIT = 5

TRAINING_MODE = False

QTD_SENSORS = 1
QTD_ACTUATORS = 1

# Classes ==========================================
class Sensor:    
    def __init__(self, value):
        self.pin = ADC(value)

    def getValue(self):
        self.pin.value()

class Button:
    def __init__(self, value):
        self.pin = Pin(value, Pin.IN)

    def is_pressed(self):
        return self.pin.value() == 1

class Potentiometer:
    def __init__(self, value):
        self.pin = ADC(value)

    def setPosition(self):
        self.pin.value()

class Servo:
    def __init__(self, value):
        self.pin = Pin(value, Pin.OUT)
        self.pwd = PWM(self.pin, freq=50)

    def getPosition(self):
        self.pwd.dutty()

    def setPosition(self, value):
        self.pwd.dutty(value)

# VARIABLES ==========================================
button = Button(PIN_BUTTON)
sensores = []
actuators = []
potentiometers = []

# FUNCTIONS ==========================================
def sensors_init():
    print('sensors_init')
    for index in range(QTD_SENSORS):
        sen = Sensor(PIN_SENSORS_INIT + index -1)
        sensores.append(sen)

def actuators_init():
    print('actuators_init')
    for index in range(QTD_ACTUATORS):
        act = Servo(PIN_ACTUATORS_INIT + index -1)
        pot = Potentiometer(PIN_SENSORS_POTENTIOMETER_INIT + index -1)
        actuators.append(act)
        potentiometers.append(pot)

def main():
    print('===========================================')
    print('Welcome!')
    sensors_init()
    actuators_init()

def loop():
    global TRAINING_MODE

    main()

    button_is_pressed = button.is_pressed()

    is_change_mode = training_mode_button.is_pressed()

    if (is_change_mode): led.invert()
    if (led.pin.value() == 1): TRAINING_MODE = True
    else: TRAINING_MODE = False

    time.sleep(0.1)
    print(TRAINING_MODE)

    if (TRAINING_MODE):
        print('TRAINING_MODE')


# MAIN ==========================================
while True:
    loop()






# ==========================================    CONVENCOES PYTHON  ==========================================
# Módulos/pacotes               =   caracteres minúsculos                   =   projetopython
# Métodos/funções/variáveis     =   minúsculos_separados_por_underlines     =   variavel_aleatoria
# Globais/constantes            =   maiúsculos_separados_por_underlines     =   CONSTANTE
# Classes                       =   Iniciais Maiúsculas                     =   NormalDistribution