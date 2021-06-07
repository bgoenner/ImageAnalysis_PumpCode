"""
Thie file contains the operations to process the incoming video data. 

Author: Brady Goenner
"""

import pandas as pd
import numpy as np
import os

def getData():
    pass

def processRiseFall(dataRef, n, m, thresh, settleP = 0.9):

    

    # open file
    cwd = os.getcwd()
    data = pd.read_csv(os.path.join(cwd, dataRef))[1:]

    RiseFallTime = [None] * 4

    colIndex = 0

    columnsData = ["Start_Index", "Delta_Index", "STD", "Average_value", "Start_conc", "End_conc", "RiseFall"]

    for col in data:

    # n intital sample

    # m RiseFall change sample size

    # State machine to determine rise and fall of data

        critDelta = 5

        startIndex = 0

        passFrame = n

        i = 0
        test_std = []
        test_avg = []

        RiseFallTime[colIndex] = pd.DataFrame(columns=columnsData)
        

        RiseFall = False

        index = 0
        passFrame = n
        startIndex = 0
        dataTableIndex = 0

        colData = data[col]

        

        for dataPoint in colData:
            
            

            std = colData[startIndex:index].std()
        
            avg = colData[startIndex:index].mean()

            index = index + 1

            if passFrame:
                passFrame = passFrame - 1

            if RiseFall == False:

                if (avg < 1.0) & \
                ((avg - float(dataPoint)) < 2) | \
                (std < 0.2):
                    pass
                elif (abs(dataPoint - avg) > std * 2): #3 Sigma outlier detection
                    # sample m more points
                    

                    RiseFall = True
                    prevPoint = dataPoint

                    # Store current std
                    # Store current avg
                    test_std = (std)
                    test_avg = (avg)


                    start_avg = avg
                    start = dataPoint
                    startIndex = index

                    pass

                else:
                    # abs(dataPoint - avg) <= std

                    # calculate new average and std
                    pass

            elif RiseFall == True:

                if abs(dataPoint - start_avg) * (1 - settleP) > abs(dataPoint - prevPoint):

                    # sample m more points
                    passFrame = m

                    RiseFall = False
                    
                    # calc riseFall time
                    if start > dataPoint:
                        RFText = "Fall"
                        
                    elif start < dataPoint:
                        RFText = "Rise"
                        
                    if ((index - startIndex) > 1) & (abs(dataPoint - start) > thresh):
                        dataTableIndex = dataTableIndex + 1
                        RiseFallTime[colIndex] = RiseFallTime[colIndex].append(pd.DataFrame({columnsData[0]:[index], \
                            columnsData[1]:[(index - startIndex)], \
                            columnsData[2]:[test_std], \
                            columnsData[3]:[test_avg], \
                            columnsData[4]:[start], \
                            columnsData[5]:[dataPoint], 
                            columnsData[6]:[RFText]}, \
                            index= {dataTableIndex} ))


                    startIndex = index

                else:
                    # Still rise / fall
                    prevPoint = dataPoint
                    pass

        colIndex = colIndex + 1

    # Export data

    # Rise/Fall Time | Rise/Fall 

    return RiseFallTime
