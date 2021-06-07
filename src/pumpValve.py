from pymodbus3.client.sync import ModbusTcpClient
import matplotlib.pyplot as plt
import pandas as pd
import dataLoader as dL
import spotterCamera as sc
import ismatecpump as ip
import time

class MFoperation:

    def __init__(self):
        self.opts = pd.DataFrame()
        self.pump = []
        self.modVal = []
        self.optLength = 0


    def addOperation(self, flowDir, flowVol, flowRate, valveS, wait):
        self.opts = pd.concat([self.opts, pd.DataFrame([{'FlowDir':flowDir,'FlowVol':flowVol,'FlowRate':flowRate,'ValveState':valveS, 'time':wait}])], axis=1)
        self.opts.reset_index(drop=True)

    def runAll(self):
        for op in self.opts.index:
            self.runOpt(op)
            time.sleep(self.opts.loc[op, 'time'])

    def runOpt(self, optNum):
        # Set pump parameters
        v = self.opts.loc[optNum,'FlowDir']
        self.pump.setFlow(self.opts.loc[optNum, 'FlowRate'])
        self.pump.setVolume(self.opts.loc[optNum,'FlowVol'])
        self.pump.setDirection(self.opts.loc[optNum, 'FlowDir'])

        v = self.opts.loc[optNum, 'ValveState']

        for i, coil in enumerate(self.opts.loc[optNum, 'ValveState']):
            self.modVal.write_coil(i, coil)
        time.sleep(0.3)

        self.pump.enable()

    def setPump(self, pump):
        self.pump = pump

    def setModValve(self, modValve):
        self.modVal = modValve


# functions
def buff(s, n):
    return (pd.concat([s.shift(-i) for i in range(n)], axis=1)
              .dropna().astype(int))


# Program operations
# in ml

flowRate = '5.0'

c = 10
wc = 0.6 

Vol = [0]*5

Vol[0] = 94 / c
Vol[1] = 90 / c
Vol[2] = 276 / c
Vol[3] = 130 / c
Vol[4] = 146 / c

wait = [0]*5

# I think this is a program wait for the pumps to run its operation 
for i,v in enumerate(Vol):
    wait[i] = v


# Valve  [PH,0, W, 0, S, 0, By,0]
# Valve  [0, 1, 2, 3, 4, 5, 6, 7]
state1 = [0, 0, 0, 0, 1, 0, 1, 0] # Push and Pull
state2 = [0, 0, 1, 0, 0, 0, 1, 0] # alignment
state3 = [1, 0, 0, 0, 1, 0, 0, 0] # Association 
state4 = [0, 0, 1, 0, 0, 0, 1, 0] # Dis 1
state5 = [1, 0, 1, 0, 0, 0, 0, 0] # Dis 2

PLC_port = '192.168.0.102'

# Connect to devices

    # connect to PLC
client = ModbusTcpClient(PLC_port)
client.write_coil(1, [0])
        # Set flow rate

        # Set valves
    # connect to pump
ismatec = ip.ISMATEC()
ismatecPort = '/dev/ttyUSB0'
ismatec.connect(ismatecPort)

    # set operations

opt = MFoperation()
opt.setPump(ismatec)
opt.setModValve(client)
opt.addOperation(0, Vol[0], flowRate, state1, wait[0])
opt.addOperation(1, Vol[1], flowRate, state2, wait[1])
opt.addOperation(0, Vol[2], flowRate, state3, wait[2])
opt.addOperation(1, Vol[3], flowRate, state4, wait[3])
opt.addOperation(1, Vol[4], flowRate, state5, wait[4])
opt.runAll()
