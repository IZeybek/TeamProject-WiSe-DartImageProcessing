import cv2 
import os.path
from .Utils import *
from .EllipseUtils import *
from .PreProcessImageUtils import *
from .VideoCapture import *
import pickle

def createTrackbarsMapping(calData):
    cv2.namedWindow('point mapping', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('p1', 'point mapping', 0, 19, nothing)
    cv2.createTrackbar('p2', 'point mapping', 0, 19, nothing)
    cv2.createTrackbar('p3', 'point mapping', 0, 19, nothing)
    cv2.createTrackbar('p4', 'point mapping', 0, 19, nothing)
    cv2.setTrackbarPos('p1', 'point mapping', calData.destinationPoints[0])
    cv2.setTrackbarPos('p2', 'point mapping', calData.destinationPoints[1])
    cv2.setTrackbarPos('p3', 'point mapping', calData.destinationPoints[2])
    cv2.setTrackbarPos('p4', 'point mapping', calData.destinationPoints[3])
    cv2.createTrackbar('1 -> Done', 'point mapping', 0, 1, nothing)

def getCalibration(calData, snapshot, original):
    # preprocess image in order to locate a well mapped Ellipse and to get two lines intersecting it in 4 diagonal points
    pre_processed_lines, pre_processed_ellipse = preProcessImage(snapshot)
    cv2.imshow("3-pre_processing_ellipse", pre_processed_ellipse)

    waitForKey()
    calData.intersectPoints, intersected_image = getIntersectionPointsFromEllipse(snapshot, pre_processed_lines, pre_processed_ellipse)
    createTrackbarsMapping(calData)
    while True:
        p1 = cv2.getTrackbarPos('p1', 'point mapping')
        p2 = cv2.getTrackbarPos('p2', 'point mapping')
        p3 = cv2.getTrackbarPos('p3', 'point mapping')
        p4 = cv2.getTrackbarPos('p4', 'point mapping')
        cv2.waitKey(1)
        cv2.imshow('intersections', intersected_image)
        s = cv2.getTrackbarPos('1 -> Done', 'point mapping')
        if s == 1:
            cv2.destroyAllWindows()
            break
    
    calData.destinationPoints = [p1,p2,p3,p4]
    calData.transformation_matrix, transformed_image = getFinalTransformationMatrix(original, calData)
    return calData, transformed_image
    
def calibrateAll(cam_L, cam_R, filename_L='Calibration_standard_output/calibrationData_L.pkl', filename_R='Calibration_standard_output/calibrationData_R.pkl'):
    snapshot_cam_L = cam_L.copy()
    snapshot_cam_R = cam_R.copy()
    image_L = filename_L.replace(".pkl", ".jpg")
    image_R = filename_R.replace(".pkl", ".jpg")

    cv2.imwrite(image_L, snapshot_cam_L)
    cv2.imwrite(image_R, snapshot_cam_R)

    original_R = snapshot_cam_R.copy()
    original_L = snapshot_cam_L.copy()
    
    calData_L, transformed_image_L = calibrateLeft(snapshot_cam_L, original_L, filename_L)
    calData_R, transformed_image_R = calibrateRight(snapshot_cam_R, original_R, filename_R)

    return calData_L, transformed_image_L, calData_R, transformed_image_R

def calibrateRight(snapshot_cam_R, original_R, filename_R='Calibration_standard_output/calibrationData_R.pkl'):
    calData_R = CalibrationData()
    calData_R.destinationPoints = [18, 8, 14, 4]
    calData_R, transformed_image_R = getCalibration(calData_R, snapshot_cam_R, original_R)
    calData_R.calImage = original_R
    cv2.imshow('transformed_R', transformed_image_R)
    cv2.waitKey(1)
    saveCalFile(filename_R, calData_R)
    cv2.destroyAllWindows()
    return calData_R, transformed_image_R

def calibrateLeft(snapshot_cam_L, original_L, filename_L='Calibration_standard_output/calibrationData_L.pkl'):
    calData_L = CalibrationData()
    calData_L.destinationPoints = [11, 1, 15, 5]
    calData_L, transformed_image_L = getCalibration(calData_L, snapshot_cam_L, original_L)
    calData_L.calImage = original_L
    cv2.imshow('transformed_L', transformed_image_L)
    cv2.waitKey(1)
    saveCalFile(filename_L, calData_L)
    cv2.destroyAllWindows()
    return calData_L, transformed_image_L

def saveCalFile(filename, calData):
    calFile = open(filename, "wb")
    pickle.dump(calData, calFile, 0)
    calFile.close()
    print("file saved to: ", filename)

def readCalibrationData(filename_L, filename_R):

    calData_L = None
    calData_R = None
    if os.path.isfile(filename_L) and os.path.isfile(filename_R):
        try:
            calFile = open(filename_L, 'rb')
            calData_L = CalibrationData()
            calData_L = pickle.load(calFile)
            calFile.close()

            calFile = open(filename_R, 'rb')
            calData_R = CalibrationData()
            calData_R = pickle.load(calFile)
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
    else:
        raise Exception('no calibration found')

def waitForKey():
    keyInput = cv2.waitKey(0)
    if keyInput == 1:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    
    videoStream_L, snapshot_cam_L = getVideoStream(src=0)
    videoStream_R, snapshot_cam_R = getVideoStream(src=1)

    cal_data_L, transformed_image_L, cal_data_R, transformed_image_R = calibrateAll(snapshot_cam_L, snapshot_cam_R)