import threading, sys, os, tempfile, distro
import playsound, time, datetime, json, queue
import wave
import sounddevice as sd
import soundfile as sf
import numpy 

audioBook = []
bookSize = 0
shouldRecord = False
recordingFinished = False

deviceNum = 0

if 'Mint' in distro.name(pretty=True):
    deviceNum=6
elif os.uname().nodename == 'raspberrypi':
    deviceNum=1

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
        
    def start(self,filename="temp.wav"):
        self.fileName = filename
        self.stopRecording = False
        self.thread = threading.Thread(target=self.main, daemon=False)
        self.thread.start()
        
    def stop(self):
        self.stopRecording = True
        while not self.doneRecording:
            time.sleep(.1)
        self.thread.join()

while True:
    audioRecorder = Recorder(deviceNum,48000)
    val = input("Do you want to record Y/N\n")
    if val.lower() == "y":
        shouldRecord = True
        recordingFileName = f"data/recording{bookSize}.wav"
        audioRecorder.start(recordingFileName)
        while shouldRecord:
            if keyboard.is_pressed("s"):
                print("RECORDING TERMINATED PRESSED")
                audioRecorder.stop()
                audioBook.append(recordingFileName)
                print(len(audioBook))
                shouldRecord = False