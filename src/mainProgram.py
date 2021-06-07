
# program imports

from pymodbus3.client.sync import ModbusTcpClient
import matplotlib.pyplot as plt
import pandas as pd
import dataLoader as dL
import spotterCamera as sc
import ismatecpump as ip
import time


captureDevice = 0

numFrames = 5

bufferSize = 100

    # connect to camera
spotCam = sc.spotterCamera()
        # Open video
spotCam.setCaptureDevice(captureDevice)
spotCam.readVideo()
spotCam.configSettings()
        # video should open a stream that can be called by the plotting function
playVideo = False
buf = 0

dfGraph = pd.DataFrame()



fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])

while playVideo:
    df, playVideo = spotCam.analyzeFrames(numFrames, buf)
    buf += 1    
    dfGraph = pd.concat([dfGraph, df], axis=0)
    if len(dfGraph.index) % 5 == 0:
        fig.clear()
        ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
        dL.readSpots(dfGraph, 'B', [1, 2, 3], [4, 5, 6], True, fig, ax)
    elif len(dfGraph.index) % 6 == 0:
        #dL.readSpots(dfGraph, 'B', [1, 2, 3], [4, 5, 6], False, fig, ax)
        pass
        

# Start graph


# Start operations
    # Set valves
    # Set flow rate
    # Set 

spotCam.close()
print("Finished recording")