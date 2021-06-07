
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

# define constants
# spots of interest
def readSpots(df, sColor, spots, bspots, replot, fig, ax):

#spots = [10,11,14,15,17,18,19,20,25,26,27,28,38,39,42,43,44,45]
        spots = [s-1 for s in spots]

        # baseline spots
        #bspots = [1,2,3,4,6,7,9,12,13,16,21,22,23,24,29,30,31,32,33,34,35,36,37,40,41]
        bspots = [s-1 for s in bspots]

        #sColor = 'R'

        # frame rate
        videoL_min = 14
        videoL_sec = 19
        videoL_Tsec = 60 * videoL_min + videoL_sec
        videoL_Tmin = videoL_Tsec/60
        # buffer average

        # load csv files

        # On windows machine
        #Test1DF = pd.read_csv("C:/Users/bg/Documents/GitHub/Image-Analysis/src/SpotTest1.csv", index_col=0)
        #Test1DF = pd.read_csv("/home/bg/Github/Image-Analysis/src/SpotTest1_2.csv")

        Test1DF = df

        
        timePerPointS = videoL_Tsec/(Test1DF.index.max() + 1)
        timePerPointM = videoL_Tmin/(Test1DF.index.max())

        timeColSec = {'timeSec':np.arange(0, videoL_Tsec, timePerPointS)}
        timeColMin = {'timeMin':np.arange(0, videoL_Tmin+timePerPointM, timePerPointM)}

        spotList = []
        
        

        for index, s in enumerate(spots):
                #spotList.append(sColor+str(s))
                #Test1DF.plot(kind='line',y=spotList)
                ax.plot(df.loc[:,sColor+str(s)])
        if replot:
                fig.canvas.draw()
        else:
                fig.show()
        plt.pause(1e-13)
        """
        baseSpotList = []

        # get initial signal and compute the deltas for the video over time
        deltaSpotDF = pd.DataFrame()

        for index, bs in enumerate(bspots):
                baseSpotList.append(sColor+str(bs))
                # calculate the delta from the first point in the plot
                deltaSpotDF = pd.concat([deltaSpotDF, \
                Test1DF.loc[:,baseSpotList[index]] \
                        .subtract(Test1DF.loc[:,baseSpotList[index]][0])], axis=1)        

        # get average deltas
        deltaSpotArr = deltaSpotDF.mean(axis=1)
        Test1DF.plot(kind='line',y=baseSpotList)
        deltaSpotArr.plot(kind='line')

        # apply deltas to the signals
        Test1_norm_DF = Test1DF.subtract(deltaSpotArr, axis=0)
        timeDF = pd.DataFrame(timeColSec, index=Test1_norm_DF.index)
        Test1_norm_DF = pd.concat([Test1_norm_DF, timeDF], axis=1)
        timeDF = pd.DataFrame(timeColMin, index=Test1_norm_DF.index)
        Test1_norm_DF = pd.concat([Test1_norm_DF, timeDF], axis=1)

        # replot the signals
        Test1_norm_DF.plot(kind='line', y=spotList, x='timeMin')
        Test1_norm_DF.plot(kind='line', y=baseSpotList, x='timeMin')
        plt.show()
        """

# calculate the rise and fall times and output the data




 

