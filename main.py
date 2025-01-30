# Turn an external led to show that the Pico is powered on

import machine

# configure LED Pin as an output pin and create and led object for Pin class
# then make the led blink in an infinite loop
led = machine.Pin(4, machine.Pin.OUT)

led.on()
