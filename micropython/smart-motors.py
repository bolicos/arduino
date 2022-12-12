
# Raspberry Pi Pico v3 Board Pins
#
# Sensors pins: A0 - 31.
# Sensors (Potentiometer) pins: A1 - 32.
# Actuators (Commons) pins: 5, 6, 7 - GPIO3, GPIO4 e GPIO5.
# Button pin: 2 - GPIO1.

from machine import ADC, Pin, PWM
import time

# Constants ==========================================
BAUD_RATE = 9600
ELEMENT_COUNT_MAX = 50

PIN_BUTTON = 2
PIN_SENSORS_INIT = 26
PIN_SENSORS_POTENTIOMETER_INIT = 27
PIN_ACTUATORS_INIT = 3

TRAINING_MODE = False
SETUP = True

QTD_SENSORS = 1
QTD_ACTUATORS = 1

# Classes ==========================================
class Sensor:    
    def __init__(self, value):
        self.pin = Pin(value, Pin.IN)
        self.adc = ADC(self.pin)

    def get_value(self):
        return self.adc.read_u16()

class Button:
    def __init__(self, value):
        self.pin = Pin(value, Pin.IN)

    def is_pressed(self):
        return self.pin.value() == 1

class Potentiometer:
    def __init__(self, value):
        self.pin = Pin(value, Pin.IN)
        self.adc = ADC(self.pin)

    def get_value(self):
        return self.adc.read_u16()

class Servo:
    def __init__(self, value):
        self.pin = Pin(value, Pin.OUT)
        self.pwd = PWM(self.pin)
        self.pwd.freq(50)

    def get_position(self):
        return self.pwd.duty_ns()

    def set_position(self, value):
        self.pwd.duty_ns(value)
        
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
        global sensors
        sen = Sensor(PIN_SENSORS_INIT + index)
        sensors[index] = sen

def actuators_init():    
    print('actuators_init')
    for index in range(QTD_ACTUATORS):
        global actuators
        global potentiometers
        act = Servo(PIN_ACTUATORS_INIT + index)
        pot = Potentiometer(PIN_SENSORS_POTENTIOMETER_INIT + index)
        actuators[index] = act
        potentiometers[index] = pot

def setup():
    print('===========================================')
    print('Welcome!')
    sensors_init()
    actuators_init()

def loop():
    global pressed_short

    pressed_short = button.is_pressed()

    if pressed_short:
        global button_counter
        button_counter += 1
    else:
        global button_counter
        button_counter = 0

    if (pressed_short and button_counter > 15):
        global pressed_long
        pressed_long = True
    else:
        global pressed_long
        pressed_long = False

    if (pressed_short and not pressed_long):
        global pressed
        pressed = True
    else:
        global pressed
        pressed = False

    if (pressed_long):
        global done
        global button_counter

        done = True
        print('Completed training!')
        button_counter = 0

    for index in range(QTD_SENSORS):
        global sensors_aux
        sensors_aux[index] = sensors[index].get_value()
    for index in range(QTD_ACTUATORS):
        global actuators_aux
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


