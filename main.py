# Make the value of power change through time and read the analog output

from machine import Pin, ADC
from time import sleep
import json
import network
from umqtt.simple import MQTTClient


def swapLights(light1, light2):
    light1.on()
    light2.off()


def checkCondition(measurement, threshold, light_good, light_bad):
    if measurement >= threshold:
        swapLights(light_good, light_bad)
    else:
        swapLights(light_bad, light_good)


def loadJson(file):
    with open(file) as open_file:
        return json.load(open_file)


def connectWifi(ssid, passwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, passwd)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    print(wlan.ifconfig())


def connectMQTT(client, broker, port, user, passwd):
    client = MQTTClient(client, broker, port, user, passwd)
    client.connect()
    return client


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

sleep(5)
wifi_config = loadJson("wifi.json")
mqtt_config = loadJson("mqtt.json")


# mqtt-related variables
mqtt_broker = mqtt_config["broker"]
mqtt_port = mqtt_config["port"]
mqtt_user = mqtt_config["user"]
mqtt_password = mqtt_config["password"]
mqtt_topic = mqtt_config["topic"]
mqtt_client_id = mqtt_config["client_id"]


connectWifi(wifi_config["ssid"], wifi_config["pass"])
mqtt_client = connectMQTT(
    mqtt_client_id, mqtt_broker, mqtt_port, mqtt_user, mqtt_password
)


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
    checkCondition(adc_battery_converted, 2, green_battery, red_battery)

    print(f"Moisture: {adc_moisture_converted} || Battery: {adc_battery_converted}")
    mqtt_client.publish(f"{mqtt_topic}/moisture", str(adc_moisture_converted))
    mqtt_client.publish(f"{mqtt_topic}/battery", str(adc_battery_converted))

    sleep(10)
