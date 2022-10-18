import time
import network
from machine import ADC, Pin, PWM

def welcome():
    print("Welcome")

# FLASH
FLASH = Pin(0, Pin.OUT)

# D5 pin
D5 = Pin(14, Pin.OUT)
# Built-in LED
LED_BOARD = Pin(2, Pin.OUT)
# Button
D6 = Pin(12, Pin.IN, Pin.PULL_UP)
push_button = Pin(13, Pin.IN)  # 23 number pin is input


def enableLED():
    print("enableLED")
    LED_BOARD.on()
    time.sleep(0.5)

    LED_BOARD.off()
    time.sleep(0.5)


def enableServo():
    print("enableServo")
    servo = PWM(D5, freq=50)

    # duty for servo is between 40 - 115
    # servo.duty(100)

    for grau in range(1, 180):
        servo.duty(grau)
        time.sleep(0.01)

        # print the pwm details like pin, freq, duty cycle
        print(servo)

    time.sleep(2)


def enablePotentiometer():
    print("enablePotentiometer")

    potenciometro = ADC(Pin(36))
    potenciometro.atten(ADC.ATTN_11DB)
    potenciometro.width(ADC.WIDTH_12BIT)

    LED = PWM(Pin(22), 100)
    LED.duty(50)

    while True:
        leitura = potenciometro.read()
        leitura = leitura * 3.3 / 4095
        duty = int(leitura * 1023 // 3.3)
        LED.duty(duty)
        time.sleep(0.1)

def enableButton():
    print('enableButton')
    print(LED_BOARD)
    # LED_BOARD.off()

    first = D6.value()

    print(first)

    D6.irq(lambda p: print(p))

    # if first:
    #     print('Button pressed!')        
    #     LED_BOARD.on()
    #     time.sleep(0.5)
    # else:
    #     LED_BOARD.off()
    #     time.sleep(0.5)


    # elif not first and second:
    #     print('Button released!')
    #     LED_BOARD.off()

# --------------- WELCOME -------------------
while True:
    # enableLED()
    # enableServo()
    # enablePotentiometer()
    enableButton()
