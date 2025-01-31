# Make the value of power change through time

from machine import Pin
from time import sleep

power = 55

# configure LED Pin as an output pin and create and led object for Pin class
# then make the led blink in an infinite loop
red = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)


def swapLights(light1, light2):
    light1.on()
    light2.off()


while True:
    for power in range(101):
        if power == 0:
            swapLights(red, green)
        if power == 50:
            swapLights(green, red)

        print(power)
        sleep(0.2)
