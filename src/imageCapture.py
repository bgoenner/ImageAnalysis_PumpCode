
import numpy as np
from matplotlib import pyplot as plt
import cv2
import pandas as pd
import time
from math import tan, pi

# global variables

captureDevice = None
videoFile = None
outputFile = None
mode = 1
totalAreaFrame = np.zeros([4], np.uint32)
cap = None
codec = 'XVID'
buffer = 1

clickOnce = False
clickStart = False
#area = np.zeros(img.shape[:2], np.uint8)

weightArray = np.zeros((256,1))

for i in range(1,256):
    weightArray[i] = i

def startMenu():

    # wait for input from terminal
    wait()

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

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global clickOnce
    global clickStart

    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(frame,(x,y),100,(255,0,0),-1)
        
        print("First position:", x, y)
        if clickOnce:
            # Resume video on second click
            clickOnce = False
            clickStart = False
            totalAreaFrame[2] = x
            totalAreaFrame[3] = y
            print("Area Changed")
        else:
            # Stop video on first click
            clickOnce = True
            clickStart = False
            totalAreaFrame[0] = x
            totalAreaFrame[1] = y


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

        if inputCommands[0] == "starts" and (len(inputCommands) == 1):
            # display window
            if mode == 1:
                print("Starting Capture")
                captureVideo(0)
            elif mode == 2:
                print("Playing Video")
                playVideoFileMulti(videoFile)

        if inputCommands[0] == 'test' and (len(inputCommands) == 1):
            print("Testing capture")

            captureVideo(1)

        if (inputCommands[0] == "quit") and (len(inputCommands) is 1):
            exit()

def setCodec(codecFormat):
    global codec
    checkCodec(codecFormat)
    codec = codecFormat

def checkCodec(codecFormat):
    pass


def setInputFile(fileName):
    pass

def setMask(text):
    # TODO implement
    pass

def setAnalysisArea(corner1, corner2):
    # set area to analyze data
    global totalAreaFrame

    totalAreaFrame = np.zeros([4], np.uint32)

    totalAreaFrame[0] = corner1[0]
    totalAreaFrame[1] = corner1[1]
    totalAreaFrame[2] = corner2[0]
    totalAreaFrame[3] = corner2[1]


def checkAreaSize(frame):
    frame_size = frame.shape[:2]
    while (totalAreaFrame[1] > frame_size[0]) or \
        (totalAreaFrame[3] > frame_size[0]) or \
        (totalAreaFrame[0] > frame_size[1]) or \
        (totalAreaFrame[2] > frame_size[1]):
        print("Area is to out of camera size.")
        print("Current size:", frame_size[0], "x", frame_size[1] )
        print("Put -a before input.")
        term = readInput()
        setAnalysisArea(term)

def setAreaMask(frame, mask = None):
    area_mask = np.zeros(frame.shape[:2], np.uint8)
    if mask is None:
        area_mask[totalAreaFrame[1]:totalAreaFrame[3], totalAreaFrame[0]:totalAreaFrame[2]] = 255
    else:
        area_mask[int(mask[1]):int(mask[3]), int(mask[0]):int(mask[2])] = 255
    return area_mask

def setAreaMaskMulti(frame, cNum, rNum, space):
    #area_mask = np.zeros(frame.shape[:2], np.uint8)
    #area_mask[mask[1]:mask[3], mask[0]:mask[2]] = 255
    #return area_mask
    # Generate mask
    areaRowSpacing = ((totalAreaFrame[3] - totalAreaFrame[1] - space[1]*(rNum-1))/rNum)
    areaColSpacing = ((totalAreaFrame[2] - totalAreaFrame[0] - space[0]*(cNum-1))/cNum)
    
    area_mask_multi = []
    i = 0
    j = 0


    for rMask in np.arange(float(totalAreaFrame[1]), float(totalAreaFrame[3]), areaRowSpacing+space[1]):
        for cMask in np.arange(float(totalAreaFrame[0]), float(totalAreaFrame[2]), areaColSpacing+space[0]):
            
            area_mask_multi.append(setAreaMask(frame, [cMask,rMask,cMask+areaColSpacing,rMask+areaRowSpacing]))
            j += 1
        i += 1

    return area_mask_multi

def areaEdit():
    terminalInput = ""

    while terminalInput != "exit":
        terminalInput = readInput()

        termComm = terminalInput.split(" ")

        # check for 2 coordinates
        # TODO check format
        if len(termComm) == 2:
            coord1 = termComm.split(" ")[0]
            coord2 = termComm.split(" ")[1]
            setAnalysisArea(coord1, coord2)
            return
        else:
            print("please input an area in the format xxx,xxx xxx,xxx")

def checkCaptureDevice():
    if captureDevice == None:
        print("Capture device not set")
        return False
    else:
        return True

def checkOutputFile():
    global outputFile

    if outputFile == None:
            print("Error: No output file")
            return 1
    try:
        if str(outputFile).split('.')[1] != "avi":
            print("Error: Rename output file to .avi")
            print("Current output file:", outputFile)
            return 1
    except(IndexError):
        print("Error not file type defined for output.")
        print("Default .avi format.")
        outputFile = outputFile + ".avi"
        return 0
    return 0

"""
class areaColorAnalysis():

    __init__(self):
        pass
    
    pass"""

def captureVideo(Test):
    global cap, codec

    bufferSize = 5

    if not checkCaptureDevice():
        return

    # Define capture device
    cap = cv2.VideoCapture(captureDevice)

    if not Test:
        # check for output file
        # TODO this check should be done during terminal input
        if checkOutputFile():
            return
        

        # defines output data file with same name as video file
        # TODO make directory for "project"
        dataOutputFile = outputFile[0:-3] + "csv"

        # Define the codec and create VideoWriter object
        # TODO allow codec to be changed  
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(outputFile ,fourcc, 20.0, (640,480))

    # initializes buffer and output DataFrame    
    ind = 0
    buf = 0
    imageColorArr = np.zeros([bufferSize, 3]) 
    imageColorDF = pd.DataFrame(columns= {'B', 'G', 'R'})

   
    # bind mouse event to frame
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    cv2.setMouseCallback('frame', draw_circle)

    # create an area mask
    # TODO make areas an array and allow for multiple areas on a single image
    
    checkAreaSize(frame) 
    area_mask = setAreaMask(frame)
    

    # TODO go over for ways to make functions to use with play video
    while(cap.isOpened()):
        # Capture frame-by-frame
        #wait()
        
        ret, frame = cap.read()

        # Our operations on the frame come here
        area_img = cv2.bitwise_and(frame,frame,mask = area_mask)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.imshow('area frame', area_img)

        # Stop video on click
        while clickOnce:
            cv2.waitKey(1)
            checkAreaSize(frame) 
            area_mask = setAreaMask(frame)
            pass

        if not Test:
            # frame must be BGR
            out.write(frame)

            #areaColorAnalysis(frame, area_mask)
            imageColorArr[ind,:] = histogramDataBRG(frame, area_mask, True)

            ind += 1
            #print(ind)
            if ind >= bufferSize:
                ind = 0
                millis = int(round(time.time() * 1000))
                tempDF = pd.DataFrame(imageColorArr.mean(0).reshape((1,3)), \
                    index={str(buf)}, \
                    columns= {'B', 'G', 'R'})
                imageColorDF = imageColorDF.append(tempDF) #, ignore_index=True)
                print("Buffer size:", imageColorDF.size)
                buf += 1
        elif Test:
            histogramDataBRG(frame, area_mask, True)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quiting video feed.")
            break
        
        # TODO make area modifiable during capture
        elif cv2.waitKey(1) & 0xFF == ord('i'):
            print("Main menu edit\n")
            mainCommandMenu()

        elif cv2.waitKey(1) & 0xFF == ord('a'):
            print("Area edit")
            areaEdit()
            checkAreaSize(frame)
            setAreaMask(frame)    

    if not Test:
        imageColorDF.to_csv(dataOutputFile)
        out.release()

    cap.release()
    cv2.destroyAllWindows()

def playVideoFile(videoFile):

    # TODO implement analysis of video

    # initializes buffer and output DataFrame  
    bufferSize = 5

    ind = 0
    buf = 0
    imageColorArr = np.zeros([bufferSize, 3]) 
    imageColorDF = pd.DataFrame(columns= {'B', 'G', 'R'})

    dataOutputFile = outputFile[0:-3] + "csv"

    cap = cv2.VideoCapture(videoFile)

    if checkOutputFile():
        return

    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    # bind mouse event to frame
    cv2.setMouseCallback('frame', draw_circle)
    
    checkAreaSize(frame) 
    area_mask = setAreaMask(frame)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            print("Video could not be grabbed")
            break

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',frame)

        # Stop video on first click
        while clickOnce:
            cv2.waitKey(1)
            checkAreaSize(frame) 
            area_mask = setAreaMask(frame)
            pass

        # Copies form above code 07/11/2018 9:42AM
        imageColorArr[ind,:] = histogramDataBRG(frame, area_mask, True)

        ind += 1
        #print(ind)
        if ind >= bufferSize:
            ind = 0
            millis = int(round(time.time() * 1000))
            tempDF = pd.DataFrame(imageColorArr.mean(0).reshape((1,3)), \
                index={str(buf)}, \
                columns= {'B', 'G', 'R'})
            imageColorDF = imageColorDF.append(tempDF) #, ignore_index=True)
            print("Buffer size:", imageColorDF.size)
            buf += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    imageColorDF.to_csv(dataOutputFile)

    cap.release()
    cv2.destroyAllWindows()


def playVideoFileMulti(videoFile):

    global cap 
    # TODO implement analysis of video

    # initializes buffer and output DataFrame  
    bufferSize = 2

    ind = 0
    buf = 0
    imageColorArr = np.zeros([bufferSize, 1, 3]) 
    imageColorDF = pd.DataFrame()
    tempDF = pd.DataFrame(index=[int(0)])

    dataOutputFile = outputFile[0:-4]

    cap = cv2.VideoCapture(videoFile)

    if checkOutputFile():
        return

    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    # bind mouse event to frame
    cv2.setMouseCallback('frame', draw_circle)
    
    checkAreaSize(frame) 
    area_mask_multi = []
    area_mask_multi = setAreaMask(frame)

    cv2.imshow('frame',frame)

    a = 0

    playVideo = False
    transf = False
    cols,rows,f = frame.shape
    cNum = 1
    rNum = 1
    space = 0
    
    imageColorArr = np.zeros([bufferSize, 3]) 
    imageColorDF = pd.DataFrame(columns= {'B0', 'G0', 'R0'})
    while(cap.isOpened()):
        
        if playVideo:
            ret, frame = cap.read()

            if not ret:
                print("Video could not be grabbed")
                break

            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if transf:
                frame = cv2.warpAffine(frame,RotM,(cols,rows))
            cv2.imshow('frame',frame)

            # Stop video on first click
            while clickOnce:
                cv2.waitKey(1)
                checkAreaSize(frame)
                area_mask_multi = setAreaMaskMulti(frame, cNum, rNum, space)
                imageColorArr = np.zeros([rNum*cNum, bufferSize, 3])
                
            
            # Copies form above code 07/11/2018 9:42AM
            for index, areaframe in enumerate(area_mask_multi):
                imageColorArr[index, ind, :] = histogramDataBRG(frame, areaframe, True)
                area_img = cv2.bitwise_and(frame,frame,mask = areaframe)
                cv2.imshow('area frame', area_img)
                
                #print(ind)
                if ind >= bufferSize-1:
                    millis = int(round(time.time() * 1000))
                    tempDF = pd.concat([tempDF, pd.DataFrame(imageColorArr[index,:,:].mean(0).reshape((1,3)), \
                        index=[int(buf)], \
                        columns= {'B'+str(index), 'G'+str(index), 'R'+str(index)})], axis=1)
                     #, ignore_index=True)
                    if index == (imageColorArr.shape[0] - 1):
                        imageColorDF = imageColorDF.append(tempDF)
                        ind = -1
                        print("Buffer size:", imageColorDF.size)
                        buf += 1
                        tempDF = pd.DataFrame(index=[int(buf)])
            
            ind += 1
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv2.waitKey(1) & 0xFF == ord('m'):
            print("Measure distance")
        if cv2.waitKey(1) & 0xFF == ord('t'):
            print('transform image, in fomrat xxx,xxx')
            transfP = str(readInput()).split(',')

            # get image shape
            rows,cols,f = frame.shape
            ang = tan(float(transfP[1])/float(transfP[0])) * 180 / pi
            RotM = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
            transf = True
            frame = cv2.warpAffine(frame,RotM,(cols,rows))
            cv2.imshow('frame',frame)
            
        if cv2.waitKey(1) & 0xFF == ord('p'):
            playVideo = not playVideo
            if playVideo:
                print("starting video")
                time.sleep(1)
            else:
                print("Pause video")
                time.sleep(1)
            return playVideo
            pass

        if cv2.waitKey(1) & 0xFF == ord('a'):
            # add mask area
            pass
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # add multi mask area
            
            # Select Area
            
            # enter columns
            print("Enter number of columns")
            cNum = int(readInput())
            # enter rows
            print("Enter number of rows")
            rNum = int(readInput())
            # enter spacing
            print("Enter pixel spacing in format xxx,xxx")
            spaceStr = readInput()
            space = spaceStr.split(',')

            space[0] = int(space[0])
            space[1] = int(space[1])

            area_mask_multi = setAreaMaskMulti(frame, cNum, rNum, space)

            imageColorArr = np.zeros([rNum*cNum, bufferSize, 3])
        if cv2.waitKey(1) & 0xFF == ord('r'):
            area_mask_review = np.zeros(frame.shape[:2], np.uint8)
            for index, areaframe in enumerate(area_mask_multi):
                area_mask_review += areaframe
            area_img = cv2.bitwise_and(frame, frame, mask = area_mask_review)
            cv2.imshow('area review frame', area_img)
        return
        

        
    imageColorDF.to_csv(dataOutputFile + '.csv')
    cap.release()
    cv2.destroyAllWindows()

def getAreaFrame(img, mask=None):
    pass



def histogramDataBRG(img, mask = None, display = True):
    #for i,col in enumerate(color):
    hist_height = 64
    hist_width = 256
    nbins = 256
    bin_width = int(hist_width/nbins)
    color = ('b','g','r')

    hB = np.zeros((hist_height,hist_width))
    hG = np.zeros((hist_height,hist_width))
    hR = np.zeros((hist_height,hist_width))
    histMean = np.zeros((256,1))
    colorAvg = np.zeros([3])

    data = (hB, hG, hR)

    for i,col in enumerate(color):
        # Calculates histogram and normalizes
        hist_raw = cv2.calcHist([img],[i],mask,[nbins],[0,256])
        cv2.normalize(hist_raw,hist_raw,64,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_raw))

        avg_hist = np.int32(np.around(np.sum(np.multiply(hist, weightArray)) / hist.sum()))  #, weights=wieghtArray)

        if display:
            for x,y in enumerate(hist):
                cv2.rectangle(data[i],(x*bin_width,y),(x*bin_width + bin_width-1,hist_height),(255),-1)

            cv2.rectangle(data[i], (avg_hist*bin_width, 0), (avg_hist*bin_width + bin_width-1, hist_height), (0), -1)
            # displays historam data
            #data[i] = np.flipud(data[i])

            cv2.imshow("Histogram " + str(col), data[i])

        colorAvg[i] = avg_hist
    return colorAvg


if __name__ == "__main__":

    startString = " Video analysis V1.0\n\n"

    print(startString)

    startMenu()

