# Make the value of power change through time and read the analog output

from machine import Pin, ADC
from time import sleep

# configure LED Pin as an output pin and create and led object for Pin class
# then make the led blink in an infinite loop
board = Pin("LED", Pin.OUT)
red = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

adc_moisture_value = ADC(27)
adc_battery_value = ADC(28)
conversion_factor = 3.3 / 65536


def swapLights(light1, light2):
    light1.on()
    light2.off()


while True:
    sleep(10)
