import threading, sys, os, tempfile
import time, json, queue
import pygame
import sounddevice as sd
import soundfile as sf
from Lever import Lever

settings = None
if os.path.exists("settings.json"):
    with open("settings.json") as f:
        settings = json.load(f)

if settings is None:
    print("Settings file not present")
    exit()



audioBook = []
bookSize = 0
shouldRecord = False
recordingFinished = False

deviceNum = settings["micInfo"]["devNum"]
sr = settings["micInfo"]["sampleRate"]
channels = settings["micInfo"]["channels"]
pinNumber = settings["pinInfo"]["number"]
invert = settings["pinInfo"]["invert"]

bookSize = len(os.listdir("data"))

class Recorder:
    started = False
    device = 0
    samplerate = 0
    q = queue.Queue(-1)
    stopRecording = False
                              
    def clearBuffer(self):
        self.q.empty()
        self.textHeard=""
        
    def isStarted(self):
        return self.started
    
    def callback(self,indata, frames, time, status):
        self.q.put(indata.copy())
        if status:
            print("ERR: ",status, file=sys.stderr)
            self.clearBuffer()
            
    def main(self):
        try:       
            self.doneRecording = False   
            if self.samplerate is None:
                device_info = sd.query_devices(self.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                self.samplerate = int(device_info['default_samplerate'])
            if self.fileName is None:
                self.fileName = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                                suffix='.wav', dir='')

            # Make sure the file is opened before recording anything:
            with sf.SoundFile(self.fileName,samplerate=self.samplerate, mode='x',
                                    channels=2) as file:
                with sd.InputStream(samplerate=self.samplerate, blocksize = 90000, device=self.device,
                                    channels=2, callback=self.callback):
                    
                    while not self.stopRecording:
                        file.write(self.q.get())                            
                    self.doneRecording = True
        except Exception as e:
            started = False
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            print(e, " Line number: ", lineno)
            print("Something happened with the microphone. Check logs")
        
    
    def __init__(self,dev='/dev/sound0',sr=48000):
        self.device = dev
        self.samplerate = sr
        
    def start(self,filename="/sd/temp.wav"):
        self.fileName = filename
        self.stopRecording = False
        self.thread = threading.Thread(target=self.main, daemon=False)
        self.thread.start()
        
    def stop(self):
        self.stopRecording = True
        while not self.doneRecording:
            time.sleep(.1)
        self.thread.join()

lever = Lever(pinNumber=pinNumber,pullUp=invert)
pygame.mixer.init()
print("ready to record")

def play(fileLocation):
    pygame.mixer.music.load(fileLocation)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    return

while True:
    if lever.getActivated():
        shouldRecord = True
        recordingFileName = f"data/recording{bookSize+1}.wav"
        play("sounds//welcome.wav")
        audioRecorder = Recorder(deviceNum,sr)
        audioRecorder.start(recordingFileName)
        play("sounds//beep.wav")
        print("Start your messege")
        while shouldRecord:
            if not lever.getActivated():
                print("RECORDING TERMINATED")
                audioRecorder.stop()
                audioBook.append(recordingFileName)
                bookSize+=1
                print(bookSize)
                shouldRecord = False
                print("ready to record")