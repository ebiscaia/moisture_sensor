# Make the value of power change through time and read the analog output

from machine import Pin, ADC
from time import sleep
import json
import network
import umail

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


def send_email(server, port, enc, user, passwd, recipients):
    for recipient in recipients:
        smtp = umail.SMTP(server, port, ssl=enc)  # Gmail's SSL port
        smtp.login(user, passwd)
        # for recipient in recipients:
        smtp.to(recipient)
        smtp.write("From:" + "RPi Pico" + "<" + user + ">\n")
        smtp.write("To: " + recipient + "\n")
        smtp.write("Subject:" + "Hello from Pico" + "\n")
        smtp.write(
            f"""
        Dear {recipient},

        Don't forget to water the plants.
        """
        )
        smtp.send()
        smtp.quit()


sleep(5)
wifi_config = loadJson("wifi.json")
email_config = loadJson("email.json")

# email-related variables
sender_email = email_config["user"]
sender_pass = email_config["pass"]
smtp_server = email_config["server"]
smtp_port = email_config["port"]
smtp_enc = email_config["tls"]
recipient_emails = email_config["recipients"]


connectWifi(wifi_config["ssid"], wifi_config["pass"])
send_email(
    smtp_server, smtp_port, smtp_enc, sender_email, sender_pass, recipient_emails
)
# send a test email


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
    sleep(10)
