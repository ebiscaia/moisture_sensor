# Make the value of power change through time and read the analog output

from machine import Pin, ADC
from time import sleep

# configure LED Pin as an output pin and create and led object for Pin class
# then make the led blink in an infinite loop
board = Pin("LED", Pin.OUT)
red_moisture = Pin(4, Pin.OUT)
green_moisture = Pin(5, Pin.OUT)
red_battery = Pin(15, Pin.OUT)
green_battery = Pin(14, Pin.OUT)

adc_moisture_value = ADC(27)
adc_battery_value = ADC(26)
conversion_factor = 3.3 / 65536


def swapLights(light1, light2):
    light1.on()
    light2.off()


def checkCondition(measurement, threshold, light_good, light_bad):
    if measurement >= threshold:
        swapLights(light_good, light_bad)
    else:
        swapLights(light_bad, light_good)


while True:
    board.on()
    adc_moisture_converted = 3.3 - adc_moisture_value.read_u16() * conversion_factor
    adc_battery_converted = adc_battery_value.read_u16() * conversion_factor
    # if adc_moisture_converted <= 0.8:
    #     swapLights(red_moisture, green_moisture)
    # else:
    #     swapLights(green_moisture, red_moisture)
    # if adc_battery_converted <= 1:
    #     swapLights(red_battery, green_battery)
    # else:
    #     swapLights(green_battery, red_battery)
    checkCondition(adc_moisture_converted, 0.8, green_moisture, red_moisture)
    checkCondition(adc_battery_converted, 1, green_battery, red_battery)

    print(f"Moisture: {adc_moisture_converted} || Battery: {adc_battery_converted}")
    sleep(10)
