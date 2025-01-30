# Set a value for power and turn one of the leds accordingly

import machine

power = 49

# configure LED Pin as an output pin and create and led object for Pin class
# then make the led blink in an infinite loop
red = machine.Pin(4, machine.Pin.OUT)
green = machine.Pin(5, machine.Pin.OUT)

if power > 50:
    light = green
else:
    light = red

light.on()
