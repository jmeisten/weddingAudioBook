import board
import digitalio
import time, threading
from Timer import Timer


class Lever:
    leverPin = 7
    leverActivated = False

    def main(self):
        pud = None
        if self.pullUp:
            pud = digitalio.Pull.UP
        else:
            pud = digitalio.Pull.UP
        lever = digitalio.DigitalInOut(board.GP16)
        lever.pull = pud
        lever.direction = digitalio.Direction.INPUT

        try:
            phonePickedUpTimer = Timer(2)
            while True: 
                readValue = lever.value
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
            print("GPIO cleaned up due to failure")

    def getActivated(self):
        return self.leverActivated

    def __init__(self, pinNumber=7, pullUp=True):
        self.leverPin = pinNumber
        self.pullUp = pullUp
        thread = threading.Thread(target=self.main, daemon=True)
        thread.start()