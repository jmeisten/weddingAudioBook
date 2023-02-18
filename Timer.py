import time
import threading

class Timer:
    startTime = 0.0
    duration = 0
    isExpired = False
    elp = 0.0
    active = False

    def start(self,t=time.time()):
        self.startTime = t
        self.active = True
        self.activated = True

    def setActive(self, active):
        self.active = active

    def checkExpired(self):
        elapsedTime  = time.time() - self.startTime
        self.elp = elapsedTime
        if elapsedTime < self.duration:
            self.isExpired = False
        else:
            self.isExpired = True
    
    def main(self):
        while True:
            self.checkExpired()
            time.sleep(.01)
    
    def __init__(self,dur):
        self.duration = dur
        thread = threading.Thread(target=self.main, daemon=True)
        thread.start()