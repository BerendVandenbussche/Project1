class tempSensor:
    @staticmethod
    def read_temprature(address):
        W1_PATH = '/sys/bus/w1/devices/{0}/w1_slave'.format(address)
        degree_sign = u'\N{DEGREE SIGN}'
        with open(W1_PATH, 'r') as file:
            for line in file:
                position = line.find("t=")
                if position > -1:
                    subtract = line[position:]
                    t_str = subtract[2:-1]
                    temp = int(t_str)/1000

                    #print("got: {}".format(subtract))
                    return temp
