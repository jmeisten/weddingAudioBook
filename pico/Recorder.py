
import audiobusio
import audiocore
import board
import array
import time
import math
import queue
import threading
import soundFile as sf

class Recorder:
    started = False
    device = 0
    samplerate = 0
    q = queue.Queue(-1)
    stopRecording = False
    failed = False
                              
    def clearBuffer(self):
        self.q.empty()
        self.textHeard=""
        
    def isStarted(self):
        return self.started

    def errorOccured(self):
        return self.failed

    def main(self):
        try:       
            self.doneRecording = False   

            # Make sure the file is opened before recording anything:
            with sf.SoundFile(self.fileName,samplerate=self.samplerate, mode='x',
                                    channels=2) as file:
                with audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=self.samplerate, bit_depth=self.bit_depth) as mic:
                    while not self.stopRecording:
                        b = array.array("H",[0] *200)
                        mic.record(b,len(b))
                        map(self.q.put, b) 
                        file.write(self.q.get())               
                    self.doneRecording = True
        except Exception as e:
            print(e)
            self.failed = True
            print("Something happened with the microphone. Check logs")
        
    
    def __init__(self,sr=48000, bit_depth=16):
        self.samplerate = sr
        self.bit_depth = bit_depth
        
    def start(self,filename="/sd/temp.wav"):
        if not "/sd/" in filename:
            filename = "/sd/" + filename
        self.fileName = filename
        self.stopRecording = False
        self.thread = threading.Thread(target=self.main, daemon=False)
        self.thread.start()
        
    def stop(self):
        self.stopRecording = True
        while not self.doneRecording:
            time.sleep(.1)
        self.thread.join()
