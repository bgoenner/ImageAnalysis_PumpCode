
import imageCapture as ic
import dataProcessing as dp

import numpy as np
import pandas as pd

captureDevice = None
videoFile = None
outputFile = None
mode = 1
totalAreaFrame = np.zeros([4], np.uint32)
cap = None
codec = 'XVID'
buffer = 1


def startMenu():

    # wait for input from terminal
    wait()

def parseTerminalInput(keyText, inputString, conditionalEvent, numArgs):

    inputCommands = inputString.split(" ")

    index = inputCommands.index(keyText)


    pass

def mainCommandMenu():

    global outputFile, captureDevice, videoFile, mode, totalAreaFrame, codec

    verbose = False

    terminalInput = ""

    while terminalInput.replace(" ", "") == "":  
 
        terminalInput = readInput()
    

        # format to string
        str(terminalInput)

        # parse input
        inputCommands = terminalInput.split(" ")

        # TODO change buffer size
        # TODO properly implement codec change
        # TODO multiple areas on single frame

        if "-c" in inputCommands or "capture" in inputCommands:
            # capture device
            # TODO make this a function
            index = inputCommands.index("-c")
            try:
                captureDevice = int(inputCommands[index + 1])
            except:
                pass
            pass

            mode = 1

        if "-a" in inputCommands or "area" in inputCommands:

            if "-a" in inputCommands and "area" in inputCommands: 
                # break from execution
                print("\nError: multiple areas defined")
            elif "-a" in inputCommands:
                index = inputCommands.index("-a")
            elif "area" in inputCommands:
                index = inputCommands.index("area")

            coord1 = np.uint32(inputCommands[index+1].split(','))
            coord2 = np.uint32(inputCommands[index+2].split(','))

            setAnalysisArea(coord1, coord2)

        if "-m" in inputCommands or "mask" in inputCommands:
            # TODO implement

            # modify mask settings
            setMask(terminalInput)
            pass

        if "-h" in inputCommands or "help" in inputCommands:
            # display help information

            helpString = "Video analysis tool V1.0\n\n" + \
                " -m or mask \t\t  mask \t set the preprossessing mask for OpenCV\n" + \
                " -a or area \t\t coord1X,coord1Y coord2X,coord2Y \t set the area for analysis\n" + \
                " -c or capture \t\t /dev/device set recording device\n" + \
                " -i or info \t\t display seetings of current session\n" + \
                " -f or file \t\t set input file" + \
                " -o of output \t set output file"

            print(helpString)

        if "-i" in inputCommands or "info" in inputCommands:
            # TODO make function

            # Display current settings
            if mode == 1:
                modeStr = "Capture"
            elif mode == 2:
                modeStr = "Video File"

            maskStr = "None"

            infoString = "Capture Device: " + str(captureDevice) + "\n" + \
                "Input File: " + str(videoFile) + "\n" + \
                "Output File: " + str(outputFile) + "\n" + \
                "Mode: " + modeStr + "\n" + \
                "Mask: " + maskStr + "\n" + \
                "Area: " + str(totalAreaFrame) + "\n"

            print(infoString + "\n")

            pass

        if "-f" in inputCommands or "file" in inputCommands:
            # TODO needs implementation
            # Parse string
            index = inputCommands.index("-f")
            videoFile = inputCommands[index + 1]

            mode = 2
            pass

        if "-o" in inputCommands or "output" in inputCommands:
            # TODO make function

            index = inputCommands.index("-o")
            outputFile = inputCommands[index + 1]
            pass
        
        if "-p" in inputCommands or "parse" in inputCommands:

            index = inputCommands.index("-p")
            parseDataFile(inputCommands[index + 1])

        if "codec" in inputCommands:
            index = inputCommands.index("codec")
            codecFormat = inputCommands[index + 1]
            setCodec(codecFormat)
            

        if inputCommands[0] == "start" and (len(inputCommands) == 1):
            # display window
            if mode == 1:
                print("Starting Capture")
                captureVideo(0)
            elif mode == 2:
                print("Playing Video")
                playVideoFile(videoFile)


        if inputCommands[0] == 'test' and (len(inputCommands) == 1):
            print("Testing capture")

            captureVideo(1)

        if (inputCommands[0] == "quit") and (len(inputCommands) is 1):
            exit()

def wait():

    # wait for input

    i_cmd = 1
    while True:
        mainCommandMenu()

def readInput():
    i_cmd = 1
    while True:
        terminalInput = input('Input [{0:d}] '.format(i_cmd))
        if terminalInput is not "":
            return terminalInput

def parseDataFile(dataFile):

    print("processing...")

    data = dp.processRiseFall(dataFile, 10, 5, 50, .90)

    # Take green data
    Gdata = pd.DataFrame()

    Gdata = data[3]

    # output csv

    savedFileName = dataFile.split(".")[0] + "_processed.csv"

    Gdata.to_csv(savedFileName)

    print("Saved:", savedFileName)

    pass

if __name__ == "__main__":

    startString = " Video analysis V1.0\n\n"

    print(startString)

    startMenu()