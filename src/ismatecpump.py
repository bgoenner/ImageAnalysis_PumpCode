import serial
import time

class ISMATEC:


    def __init__(self):
        self.pump = []
        self.direction = 1
        pass

    def setFlow(self, flowRate, units='ml/min'):
        time.sleep(0.2)
        self.pump.write('1L\r'.encode('utf-8'))
        splitStr = str(flowRate).split('.')
        addZero0 = 1 - len(splitStr[0])
        addZero1 = 3 - len(splitStr[1])
        flowRate = '0'*addZero0 + str(flowRate).replace('.','') + '0'*addZero1
        time.sleep(0.2)
        self.pump.write(('1!'+flowRate+'\r').encode('utf-8'))
        time.sleep(0.2)
        self.pump.write('1!\r'.encode('utf-8'))
        time.sleep(0.2)
        self.getFlow()
        pass

    def setDirection(self, dir):
        self.direction = dir
        if self.direction:
            time.sleep(0.2)
            self.pump.write('1J\r'.encode('utf-8'))
        else:
            time.sleep(0.2)
            self.pump.write('1K\r'.encode('utf-8'))
        pass

    def setVolume(self, volume, units='ul'):
        time.sleep(0.2)
        self.pump.write('1O\r'.encode('utf-8'))
        if units.lower() == 'ul':
            volume = volume
        elif units.lower() == 'ml':
            volume = volume * 1000
        addZeroes = 3 - len(str(volume))
        volume = '0'*addZeroes + str(volume) + '00'
        commandStr = ('1['+volume+'\r')
        time.sleep(0.2)
        self.pump.write(commandStr.encode('utf-8'))
        self.getResponse()
        pass

    def enable(self):
        time.sleep(0.2)
        self.pump.write('1H\r'.encode('utf-8'))
        time.sleep(0.2)
        self.getResponse()

        self.pump.write('1-\r'.encode('utf-8'))
        self.getResponse()

    def disable(self):
        time.sleep(0.2)
        self.pump.write('1I\r'.encode('utf-8'))

    def connect(self, dev, timeout=1000):
        self.pump = serial.Serial(dev,timeout=timeout)
        pass

    def getFlow(self):
        time.sleep(0.1)
        self.pump.write('1!\r'.encode('utf-8'))
        time.sleep(0.1)
        response = ''
        nextchr = ''
        eol = b'\r'
        leneol = len(b'\r')
        while True:
            nextchr = self.pump.read(size=1)
            if nextchr:
                response += nextchr.decode('utf-8')
                if response[-leneol:].encode('utf-8') == b'\r':
                    break
            else:
                break
        print(response)

    def getResponse(self):
        time.sleep(0.1)
        self.pump.write('1!\r'.encode('utf-8'))
        time.sleep(0.1)
        response = ''
        nextchr = ''
        eol = b'\r'
        leneol = len(b'\r')
        while True:
            nextchr = self.pump.read(size=1)
            if nextchr:
                response += nextchr.decode('utf-8')
                if response[-leneol:].encode('utf-8') == b'\r':
                    break
            else:
                break
        print(response)

