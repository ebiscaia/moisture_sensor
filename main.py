# Turn the internal led on to show that the pico is turned on

import machine

# configure LED Pin as an output pin and create and led object for Pin class
led = machine.Pin("LED", machine.Pin.OUT)

led.on()
