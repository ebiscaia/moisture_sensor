# Turn the internal led on to show that the pico is turned on

import machine
import time

# configure LED Pin as an output pin and create and led object for Pin class
# then make the led blink in an infinite loop
led = machine.Pin("LED", machine.Pin.OUT)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
