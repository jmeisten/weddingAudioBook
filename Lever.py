import RPi.GPIO as GPIO
import time, threading
from Timer import Timer


class Lever:
    leverPin = 7
    leverActivated = False

    def main(self):
        GPIO.setmode(GPIO.BOARD)
        pud = None
        if self.pullUp:
            pud = GPIO.PUD_UP
        else:
            pud = GPIO.PUD_DOWN
        GPIO.setup(self.leverPin, GPIO.IN, pull_up_down=pud)

        try:
            phonePickedUpTimer = Timer(2)
            while True: 
                readValue = GPIO.input(self.leverPin)
                if readValue == 1:
                    self.leverActivated = False
                    phonePickedUpTimer.setActive(False)
                elif readValue == 0:
                    if not phonePickedUpTimer.active:
                        phonePickedUpTimer.start()
                    elif phonePickedUpTimer.isExpired:
                        self.leverActivated = True
                time.sleep(.1)
        except Exception as e:
            print(e)
            GPIO.cleanup()
            print("GPIO cleaned up due to failure")

    def getActivated(self):
        return self.leverActivated

    def __init__(self, pinNumber=7, pullUp=True):
        self.leverPin = pinNumber
        self.pullUp = pullUp
        thread = threading.Thread(target=self.main, daemon=True)
        thread.start()