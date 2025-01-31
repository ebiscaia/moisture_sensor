# Make the value of power change through time and read the analog output

from machine import Pin, ADC
from time import sleep

# configure LED Pin as an output pin and create and led object for Pin class
# then make the led blink in an infinite loop
red = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

adc_value = ADC(28)


def swapLights(light1, light2):
    light1.on()
    light2.off()


while True:
    for power in range(101):
        if power == 0:
            swapLights(red, green)
        if power == 50:
            swapLights(green, red)

        print(f"Power: {power} | ADC: {adc_value.read_u16()}")
        sleep(0.2)
