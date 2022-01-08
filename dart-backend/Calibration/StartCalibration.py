
import os.path
import sys
import cv2
import pickle
from .Utils import *
from .ellipseToCircle import *
from .CalibrationMain import *

def getCalibration(imCalRGB_R, imCalRGB_L):
    imCalRGB_R = imCalRGB_R.copy();
    imCalRGB_L = imCalRGB_L.copy()
    if os.path.isfile("calibrationData_R.pkl"):
            try:
                return readCalibrationData(imCalRGB_R, imCalRGB_L)#, calData_L

            #corrupted file
            except EOFError as err:
                print(err)
    else: 
        # cam_R = VideoStream(src=1).start() 
        # cam_L = VideoStream(src=0).start()

        # cam_R = cv2.imread("Links-empty.jpg") #
        # cam_L = cv2.imread("Links-empty.jpg") # 
        return calibrate(imCalRGB_R, imCalRGB_L)

def readCalibrationData(imCalRGB_R, imCalRGB_L):
    calFile = open('calibrationData_R.pkl', 'rb')
    calData_R = CalibrationData()
    calData_R = pickle.load(calFile)
    calFile.close()

    # calFile = open('calibrationData_R.pkl', 'rb')
    # calData_L = CalibrationData()
    # calData_L = pickle.load(calFile)
    # calFile.close()

    #copy image for old calibration data
    transformed_img_R = imCalRGB_R.copy()
    # transformed_img_L = imCalRGB_L.copy()

    transformed_img_R = cv2.warpPerspective(imCalRGB_R, calData_R.transformation_matrix, (800, 800))
    # transformed_img_L = cv2.warpPerspective(imCalRGB_L, calData_L.transformation_matrix, (800, 800))
    draw_R = getNormilizedBoard(transformed_img_R, calData_R)
    # draw_L = getNormilizedBoard(imCalRGB_R,imCalRGB_R)

    # transformed_img_L = draw_L.drawBoard(transformed_img_L, calData_L)

    cv2.imshow("Left_Cam", draw_R)
    # cv2.imshow("Left Cam", transformed_img_L)
    return calData_R , draw_R#, calData_L