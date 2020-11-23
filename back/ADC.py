import spidev
import math
spi = spidev.SpiDev()

class ADCSPI:
    def __init__(self, kloksnelheid, bytes_in=0):
        self.__bytes_in = bytes_in
        self.__max_speed = kloksnelheid


    def return_light(self):
        spi.open(0, 0)
        spi.max_speed_hz = self.__max_speed
        self.bytes_out = [0b00000001, 0b10010000, 0]
        self.bytes_in = spi.xfer2(self.bytes_out)
        spi.close()
        #print(bytes_in)
        int1 = self.bytes_in[1]
        int2 = self.bytes_in[2]
        byte = int1 << 8 | int2
        #print(byte)
        percentage = byte / 1023 * 100
        lichtsterkte= 100 - percentage
        return lichtsterkte
