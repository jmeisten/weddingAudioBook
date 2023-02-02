import RPi.GPIO as GPIO
import time

testPin = 7

GPIO.setup(testPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(testPin) == GPIO.LOW:
        print("low")
    else:
        print("high")