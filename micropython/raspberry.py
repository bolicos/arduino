import time
from machine import ADC, Pin, PWM

# --------------- INIT -------------------
def welcome(): print('Welcome the Raspberry Pi Pico Pinout')

# --------------- VARIABLES -------------------
ENABLE = True
LED_BOARD = Pin(25, Pin.OUT) # Built-in LED
LED = Pin(7, Pin.OUT) # External LED
BUTTON_1 = Pin(9, Pin.IN, Pin.PULL_DOWN) # Button 1
BUTTON_2 = Pin(10, Pin.IN, Pin.PULL_DOWN) # Button 2

# =============== FUNCTIONS ===============
def enableLED(led):
    led.on()
    time.sleep(0.5)

def disableLED(led):
    led.off()
    time.sleep(0.5)

def isActiveButton(button):
    print('BUTTON')
    enable = button.value()
    return enable

def enableLEDByButton():
    print('======== FUNCTION =========')
    isEnabled = isActiveButton(BUTTON_1)
    isDisabled = isActiveButton(BUTTON_2)

    if isEnabled:
        enableLED(LED)
        print('ENABLE')
    if isDisabled:
        disableLED(LED)
        print('DISABLE')

def home():
    BUTTON_1.irq(trigger = Pin.IRQ_RISING, handler = enableLEDByButton())
    BUTTON_2.irq(trigger = Pin.IRQ_FALLING, handler = enableLEDByButton())

# =============== MAIN ===============
while ENABLE:
    # enableLED(LED)
    # isActiveButton(BUTTON_1)
    enableLEDByButton()
    # home()
