import cv2 
import os.path
from .Utils import *
from .EllipseUtils import *
from .PreProcessImageUtils import *
import pickle

def getCalibration(calData, snapshot, original):
    # preprocess image in order to locate a well mapped Ellipse and to get two lines intersecting it in 4 diagonal points
    pre_processed_lines, pre_processed_ellipse = preProcessImage(snapshot)
    cv2.imshow("3-pre_processing_ellipse", pre_processed_ellipse)

    waitForKey()
    calData.intersectPoints = getIntersectionPointsFromEllipse(snapshot, pre_processed_lines, pre_processed_ellipse, calData)

    waitForKey()
    calData.transformation_matrix, transformed_image = getFinalTransformationMatrix(original, calData)
    return calData, transformed_image
    
def calibrateAll(snapshot_cam_R, snapshot_cam_L):

    cv2.imwrite("cam_R.jpg", snapshot_cam_R)
    cv2.imwrite("cam_L.jpg", snapshot_cam_L)

    original_R = snapshot_cam_R.copy()
    original_L = snapshot_cam_L.copy()
    
    calData_L, transformed_image_L = calibrateLeft(snapshot_cam_L, original_L)
    saveCalFile("calibrationData_L.pkl", calData_L)
    calData_R, transformed_image_R = calibrateRight(snapshot_cam_R, original_R)
    saveCalFile("calibrationData_R.pkl", calData_R)

    return calData_R, transformed_image_R, calData_L, transformed_image_L

def calibrateRight(snapshot_cam_R, original_R):
    calData_R = CalibrationData()
    calData_R.angleZone_horizontal = ( -40 , -35)
    calData_R.angleZone_vertical  = (-160, -150)
    calData_R.destinationPoints = [19, 9, 14, 4] # [0, 5, 10, 15]
    calData_R, transformed_image_R = getCalibration(calData_R, snapshot_cam_R, original_R)
    calData_R.calImage = original_R
    cv2.imshow('transformed_R', transformed_image_R)
    waitForKey()

    return calData_R, transformed_image_R

def calibrateLeft(snapshot_cam_L, original_L):
    calData_L = CalibrationData()

    calData_L.angleZone_horizontal = (10, 20)
    calData_L.angleZone_vertical = (-50 , -25)
    calData_L.destinationPoints = [9, 19, 15, 5] # [0, 5, 10, 15]
    calData_L, transformed_image_L = getCalibration(calData_L, snapshot_cam_L, original_L)
    calData_L.calImage = original_L
    cv2.imshow('transformed_L', transformed_image_L)
    waitForKey()

    return calData_L, transformed_image_L

def saveCalFile(filename, calData):
    calFile = open(filename, "wb")
    pickle.dump(calData, calFile, 0)
    calFile.close()

def readCalibrationData(filename_R, filename_L):

    calData_L = None
    calData_R = None
    if os.path.isfile(filename_R) and os.path.isfile(filename_L):
        try:
            calFile = open(filename_R, 'rb')
            calData_R = CalibrationData()
            calData_R = pickle.load(calFile)
            calFile.close()
            calFile = open(filename_L, 'rb')
            calData_L = CalibrationData()
            calData_L = pickle.load(calFile)
            calFile.close()
        #corrupted file
        except EOFError as err:
            print(err)
            return None
    imCalRGB_R = calData_R.calImage
    imCalRGB_L = calData_L.calImage
    #copy image for old calibration data
    transformed_img_R = calData_R.calImage.copy()
    transformed_img_L = calData_L.calImage.copy()

    transformed_img_R = cv2.warpPerspective(imCalRGB_R, calData_R.transformation_matrix, (800, 800))
    transformed_img_L = cv2.warpPerspective(imCalRGB_L, calData_L.transformation_matrix, (800, 800))
    draw_R = getNormilizedBoard(transformed_img_R, calData_R)
    draw_L = getNormilizedBoard(transformed_img_L, calData_L)

    # cv2.imshow("Left_Cam", draw_L)
    # cv2.imshow("Right_Cam", draw_R)
    return calData_L, draw_L, calData_R , draw_R

def waitForKey():
    keyInput = cv2.waitKey(0)
    if keyInput == 1:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    print("Welcome to darts!")
    
    # cam_R = VideoStream(src=1).start() 
    # cam_L = VideoStream(src=0).start()
    
    cam_R = cv2.imread("cam_R.jpg") #
    cam_L = cv2.imread("cam_R.jpg") # 
    calibrateAll(cam_R, cam_L)
