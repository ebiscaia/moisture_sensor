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
    board.on()
    adc_moisture_converted = adc_moisture_value.read_u16() * conversion_factor
    adc_battery_converted = adc_battery_value.read_u16() * conversion_factor
    if adc_moisture_converted >= 2.5:
        swapLights(red, green)
    else:
        swapLights(green, red)

    print(f"Moisture: {adc_moisture_converted} || Battery: {adc_battery_converted}")
    sleep(10)
