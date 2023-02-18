import RPi.GPIO as GPIO
import time

testPin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(testPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True: 
        readValue = GPIO.input(testPin)
        if readValue == 1:
            print("low")
        else:
            print("high")
        time.sleep(.2)
except Exception as e:
    print(e)
    GPIO.cleanup()
    print("GPIO cleaned up due to failure")