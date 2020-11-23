from RPi import GPIO
import time

class lcd:
    def __init__(self, E = 20 , RS= 21 ,D0 = 16, D1 = 12, D2 = 25, D3 = 24, D4 = 23, D5 = 26, D6 = 19, D7 = 13):
        self.__pin = [D0, D1, D2, D3, D4, D5, D6, D7]
        self.__e = E
        self.__rs = RS
        self.init_GPIO()
        self.init_LCD()

    def init_GPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.setup([self.__e, self.__rs], GPIO.OUT)


    def init_LCD(self):
        self.send_instruction(0b00111000)
        self.send_instruction(0b00001111)
        self.send_instruction(0b00000001)
        self.send_instruction(0b0000001100)


    def set_data_bits(self, byte):
        for i in range(8):
            bit = (byte >> i) & 1
            GPIO.output(self.__pin[i], bit)

    def send_instruction(self, data_byte):
        GPIO.output(self.__e, 1)
        GPIO.output(self.__rs, 0)
        self.set_data_bits(data_byte)
        GPIO.output(self.__e, 0)
        time.sleep(0.01)

    def send_character(self, data_byte):
        GPIO.output(self.__e, 1)
        GPIO.output(self.__rs, 1)
        self.set_data_bits(data_byte)
        GPIO.output(self.__e, 0)
        time.sleep(0.01)

    def write_message(self, message):
        for k in message:
            self.send_character(ord(k))

    def second_row(self):
        self.send_instruction(0b11000000)

    def last_place(self):
        self.send_instruction(0b11111)








