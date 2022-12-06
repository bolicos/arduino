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

    def get_value(self):
        return self.pin.value()

class Button:
    def __init__(self, value):
        self.pin = Pin(value, Pin.IN)

    def is_pressed(self):
        return self.pin.value() == 1

class Potentiometer:
    def __init__(self, value):
        self.pin = ADC(value)

    def get_value(self):
        return self.adc.read()

class Servo:
    def __init__(self, value):
        self.pin = Pin(value, Pin.OUT)
        self.pwd = PWM(self.pin, freq=50)

    def get_position(self):
        return self.pwd.duty()

    def set_position(self, value):
        self.pwd.duty(value)

# VARIABLES ==========================================
button = Button(PIN_BUTTON)
sensors = [Sensor]
actuators = [Servo]
potentiometers = [Potentiometer]

sensors_aux = [int]
actuators_aux = [int]

sensors_saved_values = [[int]]
actuators_saved_values = [[int]]

training_counter = 0
button_counter = 0

pressed_short = False
pressed_long = False
pressed = False
done = False

# FUNCTIONS ==========================================
def sensors_init():
    print('sensors_init')
    for index in range(QTD_SENSORS):
        sen = Sensor(PIN_SENSORS_INIT + index)
        sensors.append(sen)

def actuators_init():
    print('actuators_init')
    for index in range(QTD_ACTUATORS):
        act = Servo(PIN_ACTUATORS_INIT + index)
        pot = Potentiometer(PIN_SENSORS_POTENTIOMETER_INIT + index)
        actuators.append(act)
        potentiometers.append(pot)

def setup():
    print('===========================================')
    print('Welcome!')
    sensors_init()
    actuators_init()

def loop():
    pressed_short = button.is_pressed()

    if pressed_short:
        button_counter += 1
    else:
        button_counter = 0

    if (pressed_short and button_counter > 15):
        pressed_long = True
    else:
        pressed_long = False

    if (pressed_short and not pressed_long):
        pressed = True
    else:
        pressed = False

    if (pressed_long):
        done = True
        print('Completed training!')
        button_counter = 0

    for index in range(QTD_SENSORS):
        sensors_aux[index] = sensors[index].get_value()
    for index in range(QTD_ACTUATORS):
        actuators_aux[index] = potentiometers[index].get_value()

# Conditionals
    if (done):
        diff = 0
        position = 0

        for index in range(QTD_SENSORS):
            value = abs(sensors_saved_values[0][index] - sensors_aux[index])
            diff = diff + value

        for index in range(training_counter):
            new_diff = 0

            for aux in range(QTD_SENSORS):
                value = abs(sensors_saved_values[index][aux] - sensors_aux[aux])
                new_diff = new_diff + value
            
            if (new_diff < diff):
                diff = new_diff
                position = index

        for index in range(QTD_ACTUATORS):
            value = actuators_saved_values[position][index]
            actuators[index].set_position(value)
    elif(pressed):
        for index in range(QTD_SENSORS):
            value = sensors_aux[index]
            sensors_saved_values[training_counter][index](value)

        for index in range(QTD_ACTUATORS):
            value = actuators_aux[index]
            actuators_saved_values[training_counter][index](value)

        training_counter += 1
    else:
        for index in range(QTD_ACTUATORS):
            value = actuators_aux[index]
            actuators[index].set_position(value)

# MAIN ==========================================
while True:
    if (SETUP):
        SETUP = False
        setup()

    loop()
    time.sleep(0.03)


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