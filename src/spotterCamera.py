import numpy as np
from matplotlib import pyplot as plt
import cv2
import pandas as pd
import time
from math import tan, pi

class spotterCamera:
    def __init__(self):
        
        self.clickOnce = False
        self.playVideo = False
        self.cap = []
        self.videoFile = ''
        self.outputFile = 'Output'

        self._totalAreaFrame = np.zeros([4], np.uint32)
        self._codec = 'XVID'
        self._transf = False
        self._multiColumns = 1
        self._multiRows = 1
        self._space = [0,0]
        self._frame = []
        self._RotMatrix = cv2.getRotationMatrix2D((0,0),0,1)
        self._area_mask_multi = []
        self.weightArray = np.zeros((256,1))
        for i in range(1,256):
            self.weightArray[i] = i

        pass

    def setCaptureDevice(self, dev):
        self.cap = cv2.VideoCapture(dev)
        ret,self._frame = self.cap.read()


    def readVideo(self):
        cv2.imshow('frame',self._frame)
        cv2.setMouseCallback('frame', self.draw_circle)
        rows,cols,f = self._frame.shape
                
        while True:
            ret, self._frame = self.cap.read()
            cv2.imshow('frame',self._frame)
            self._frame = cv2.warpAffine(self._frame,self._RotMatrix,(cols,rows))
            if cv2.waitKey(30) & 0xFF == ord('q'):
                print('Quit read video')
                return False

    def readSingleFrame(self):
        cv2.imshow('frame',self._frame)
        cv2.setMouseCallback('frame', self.draw_circle)
        while True:
            if cv2.waitKey(30) & 0xFF == ord('q'):
                print('Exit single frame')
                return False


    def configSettings(self):
        # get a single frame
        ret, self._frame = self.cap.read()
        cv2.imshow('frame',self._frame)
        cv2.setMouseCallback('frame', self.draw_circle)
        print('Single frame. Take measurements or press q to continue')
        self.readSingleFrame()
        setMask = True
        while setMask:
            print('Set the image transformation')
            self.setTransformationCommand()
            print('Set the image mask area')
            self.setAreaMaskCommand()       
            print('Set eh image mask properties')
            setMask = self.setMaskCommand()
        cv2.destroyAllWindows()
            

    def setMaskCommand(self):
        print("Enter number of columns")
        self._multiColumns = int(self.readInput())
        # enter rows
        print("Enter number of rows")
        self._multiRows = int(self.readInput())
        # enter spacing
        print("Enter pixel spacing in format xxx,xxx")
        spaceStr = self.readInput()
        self._space = spaceStr.split(',')
        self.checkAreaSize()
        self.setAreaMask()

        return self.previewMask()

    def previewMask(self):
        area_mask_review = np.zeros(self._frame.shape[:2], np.uint8)
        # add all frames together
        for index, areaframe in enumerate(self._area_mask_multi):
            area_mask_review += areaframe
            pass
        # read current frame with mask
        area_img = cv2.bitwise_and(self._frame, self._frame, mask = area_mask_review)
        cv2.imshow('area review frame', area_img)
        while True:
            if cv2.waitKey(30) & 0xFF == ord('s'):
                time.sleep(2)
                return False
            if cv2.waitKey(30) & 0xFF == ord('r'):
                time.sleep(2)
                return True

    def setTransformation(self, transfP):
        # get image shape
        rows,cols,f = self._frame.shape
        if not (float(transfP[0]) == float(0)):
            ang = tan(float(transfP[1])/float(transfP[0])) * 180 / pi
        
        else:
            ang = 0
        self._RotMatrix = cv2.getRotationMatrix2D((cols/2,rows/2),ang,1)
        self._transf = True
        self._frame = cv2.warpAffine(self._frame,self._RotMatrix,(cols,rows))
        
        cv2.imshow('frame',self._frame)
        self.readSingleFrame()


    def setTransformationCommand(self):
        print('transform image, in fomrat xxx,xxx')
        transfP = str(self.readInput()).split(',')
        self.setTransformation(transfP)

    def setAreaMaskCommand(self):
        ret, self.frame = self.cap.read()
        cv2.imshow('frame',self._frame)
        cv2.setMouseCallback('frame', self.draw_circle)
        while not self.clickOnce:
                cv2.waitKey(30)

        while self.clickOnce:
                cv2.waitKey(30)
        self.checkAreaSize()
        self.setAreaMask()


    def areaMask(self, frame, mask = None):
        area_mask = np.zeros(frame.shape[:2], np.uint8)
        if mask is None:
            area_mask[self._totalAreaFrame[1]:self._totalAreaFrame[3], self._totalAreaFrame[0]:self._totalAreaFrame[2]] = 255
        else:
            area_mask[int(mask[1]):int(mask[3]), int(mask[0]):int(mask[2])] = 255
        return area_mask

    def setAreaMask(self):
        frame=self._frame
        cNum=self._multiColumns
        rNum=self._multiRows
        space = [0,0]
        space[0]=int(self._space[0])
        space[1]=int(self._space[1])
        self.checkAreaSize()
        #area_mask = np.zeros(frame.shape[:2], np.uint8)
        #area_mask[mask[1]:mask[3], mask[0]:mask[2]] = 255
        #return area_mask
        # Generate mask
        areaRowSpacing = ((self._totalAreaFrame[3] - self._totalAreaFrame[1] - space[1]*(rNum-1))/rNum)
        areaColSpacing = ((self._totalAreaFrame[2] - self._totalAreaFrame[0] - space[0]*(cNum-1))/cNum)
        
        self._area_mask_multi = []
        i = 0
        j = 0

        # creat an arrray of area mask frames
        for rMask in np.arange(float(self._totalAreaFrame[1]), float(self._totalAreaFrame[3]), areaRowSpacing+space[1]):
            for cMask in np.arange(float(self._totalAreaFrame[0]), float(self._totalAreaFrame[2]), areaColSpacing+space[0]):
                
                self._area_mask_multi.append(self.areaMask(self._frame, [cMask,rMask,cMask+areaColSpacing,rMask+areaRowSpacing]))
                j += 1
            i += 1


    def checkAreaSize(self):
        frame = self._frame
        frame_size = frame.shape[:2]
        while (self._totalAreaFrame[1] > frame_size[0]) or \
            (self._totalAreaFrame[3] > frame_size[0]) or \
            (self._totalAreaFrame[0] > frame_size[1]) or \
            (self._totalAreaFrame[2] > frame_size[1]):
            print("Area is to out of camera size.")
            print("Current size:", frame_size[0], "x", frame_size[1] )
            print("Put -a before input.")
            term = self.readInput()
            setAnalysisArea(term)

    def readInput(self):
        i_cmd = 1
        while True:
            terminalInput = input('Input [{0:d}] '.format(i_cmd))
            if terminalInput is not "":
                return terminalInput

    def draw_circle(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            #cv2.circle(frame,(x,y),100,(255,0,0),-1)
            
            print("First position:", x, y)
            if self.clickOnce:
                # Resume video on second click
                self.clickOnce = False
                self._totalAreaFrame[2] = x
                self._totalAreaFrame[3] = y
                print("Area Changed")
            else:
                # Stop video on first click
                self.clickOnce = True
                self._totalAreaFrame[0] = x
                self._totalAreaFrame[1] = y
    
    def setAnalysisArea(self, corner1, corner2):
        # set area to analyze data

        self._totalAreaFrame = np.zeros([4], np.uint32)

        self._totalAreaFrame[0] = corner1[0]
        self._totalAreaFrame[1] = corner1[1]
        self._totalAreaFrame[2] = corner2[0]
        self._totalAreaFrame[3] = corner2[1]

    def checkOutputFile(self):

        if self.outputFile == None:
                print("Error: No output file")
                return 1
        try:
            if str(self.outputFile).split('.')[1] != "avi":
                print("Error: Rename output file to .avi")
                print("Current output file:", outputFile)
                return 1
        except(IndexError):
            print("Error not file type defined for output.")
            print("Default .avi format.")
            outputFile = outputFile + ".avi"
            return 0
        return 0

    
    def analyzeFrames(self, frames, buf, dispFrame=True, dispMask=False, dispHist=False):
        i = 0
        self.playVideo = True
        imageColorDF = pd.DataFrame()
        tempDF = pd.DataFrame()
        imageColorArr = np.zeros([self._multiRows*self._multiColumns, frames, 3])

        while self.playVideo and frames > i:
            ret, self._frame = self.cap.read()


            if not ret:
                print("Video could not be grabbed")
                break

            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self._transf:
                rows,cols,f = self._frame.shape
                self._frame = cv2.warpAffine(self._frame,self._RotMatrix,(cols,rows))
            cv2.imshow('frame',self._frame)

            # Stop video on first click
            while self.clickOnce:
                cv2.waitKey(1)
                self.checkAreaSize()
                self.setAreaMask()
                imageColorArr = np.zeros([self._multiRows*self._multiColumns, frames, 3])
                
            
            # Copies form above code 07/11/2018 9:42AM
            for index, areaframe in enumerate(self._area_mask_multi):
                imageColorArr[index, i, :] = self.histogramDataBRG(self._frame, areaframe, True)
                area_img = cv2.bitwise_and(self._frame,self._frame,mask = areaframe)
                #cv2.imshow('area frame', area_img)
                
                #print(ind)
                if i >= frames-1:
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
            
            i += 1
            if cv2.waitKey(30) & 0xFF == ord('q'):
                return imageColorDF, False
        self.playVideo = False
        #self.cap.release()
        #cv2.destroyAllWindows()
        return imageColorDF, True

    def histogramDataBRG(self, img, mask = None, display = True):
        #for i,col in enumerate(color):
        hist_height = 64
        hist_width = 256
        nbins = 256
        bin_width = int(hist_width/nbins)
        color = ('b','g','r')

        hB = np.zeros((hist_height,hist_width))
        hG = np.zeros((hist_height,hist_width))
        hR = np.zeros((hist_height,hist_width))
        histMean = np.ones((256,1))
        colorAvg = np.zeros([3])

        data = (hB, hG, hR)

        for i,col in enumerate(color):
            # Calculates histogram and normalizes
            hist_raw = cv2.calcHist([img],[i],mask,[nbins],[0,256])
            cv2.normalize(hist_raw,hist_raw,64,cv2.NORM_MINMAX)
            hist=np.int32(np.around(hist_raw))

            avg_hist = np.int32(np.around(np.sum(np.multiply(hist, self.weightArray)) / hist.sum()))  #, weights=wieghtArray)

            if display:
                for x,y in enumerate(hist):
                    cv2.rectangle(data[i],(x*bin_width,y),(x*bin_width + bin_width-1,hist_height),(255),-1)

                cv2.rectangle(data[i], (avg_hist*bin_width, 0), (avg_hist*bin_width + bin_width-1, hist_height), (0), -1)
                # displays historam data
                #data[i] = np.flipud(data[i])

                cv2.imshow("Histogram " + str(col), data[i])

            colorAvg[i] = avg_hist
        return colorAvg

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
