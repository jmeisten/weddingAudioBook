import RPi.GPIO as GPIO
import time, threading
from Timer import Timer


class Lever:
    leverPin = 7
    leverActivated = False

    def main(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.leverPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

    def __init__(self, pinNumber=7):
        self.leverPin = pinNumber
        thread = threading.Thread(target=self.main, daemon=True)
        thread.start()