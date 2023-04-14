import machine
import sdcard
import uos

class SDReader:

    def read(self, filename=""):
        data = None
        filename = "/sd/" + filename
        with open(filename,"r") as f:
            data = f.read()
        return data

    def write(self, filename, data):
        if filename is None or data is None:
            return False
        filename = "/sd/" + filename
        with open(filename, "w") as f:
            f.write(data)
        return True

    def __init__(self,clk=10,cs=9,mosi=11,miso=8):
        self.cs =  machine.Pin(cs, machine.Pin.OUT)

        # Intialize SPI peripheral (start with 1 MHz)
        spi = machine.SPI(1,
                        baudrate=1000000,
                        polarity=0,
                        phase=0,
                        bits=8,
                        firstbit=machine.SPI.MSB,
                        sck=machine.Pin(clk),
                        mosi=machine.Pin(mosi),
                        miso=machine.Pin(miso))

        # Initialize SD card
        self.sd = sdcard.SDCard(spi, cs)

        # Mount filesystem
        self.vfs = uos.VfsFat(self.sd)
        uos.mount(self.vfs, "/sd")