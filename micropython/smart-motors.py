# Raspberry Pi Pico Board Pins
#
# Sensors pins: A0 - 31.
# Sensors (Potentiometer) pins: A1 - 32.
# Actuators (Commons) pins: 5, 6, 7 - GPIO3, GPIO4 e GPIO5.
# Button pin: 2 - GPIO1.

import time
from machine import ADC, Pin, PWM

# Constants ==========================================
BAUD_RATE = 9600
ELEMENT_COUNT_MAX = 50

PIN_BUTTON = 2
PIN_SENSORS_INIT = 31
PIN_SENSORS_POTENTIOMETER_INIT = 32
PIN_ACTUATORS_INIT = 5

TRAINING_MODE = False
SETUP = True

QTD_SENSORS = 1
QTD_ACTUATORS = 1

# Classes ==========================================
class Sensor:    
    def __init__(self, value):
        self.pin = ADC(value)

    def getValue(self):
        return self.pin.value()

class Button:
    def __init__(self, value):
        self.pin = Pin(value, Pin.IN)

    def is_pressed(self):
        return self.pin.value() == 1

class Potentiometer:
    def __init__(self, value):
        self.pin = ADC(value)

    def getValue(self):
        return self.adc.read()

class Servo:
    def __init__(self, value):
        self.pin = Pin(value, Pin.OUT)
        self.pwd = PWM(self.pin, freq=50)

    def getPosition(self):
        return self.pwd.duty()

    def setPosition(self, value):
        self.pwd.duty(value)

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
    # global TRAINING_MODE

    button_is_pressed = button.is_pressed()


# MAIN ==========================================
while True:
    if (SETUP): main()

    loop()

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