import threading, sys, os, tempfile
import time, json, queue
from Recorder import Recorder
from Lever import Lever
import board
import audiocore
import audiobusio
import digitalio
from SDReader import SDReader

sd = SDReader()
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

lever = Lever(pinNumber=pinNumber,pullUp=invert)
print("ready to record")

def play(fileLocation="sounds//welcome.wav"):
    f = open(fileLocation, "rb")
    wav = audiocore.WaveFile(f)
    a = audiobusio.I2SOut(board.D1, board.D0, board.D9)
    print("playing")
    a.play(wav)
    while a.playing:
        pass
    a.deinit()
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