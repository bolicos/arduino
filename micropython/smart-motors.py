import time
from machine import ADC, Pin, PWM, Signal

# Constants ==========================================
TRAINING_MODE = False
BUILD_LED_PIN = 25
LED_PIN = 7
POTENTIOMETER_PI = 
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
        # self.pin = Pin(value, Pin.OUT)
        self.pwd = ADC(28)

    def setPosition(self):
        self.pwd.value()

class Servo:
    def __init__(self, value):
        self.pin = Pin(value, Pin.OUT)
        self.pwd = PWM(self.pin, freq=50)

    def setPosition(self):
        self.pwd.value()

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


# MAIN ==========================================
while True:
    loop()






# ==========================================    CONVENCOES PYTHON  ==========================================
# Módulos/pacotes               =   caracteres minúsculos                   =   projetopython
# Métodos/funções/variáveis     =   minúsculos_separados_por_underlines     =   variavel_aleatoria
# Globais/constantes            =   maiúsculos_separados_por_underlines     =   CONSTANTE
# Classes                       =   Iniciais Maiúsculas                     =   NormalDistribution