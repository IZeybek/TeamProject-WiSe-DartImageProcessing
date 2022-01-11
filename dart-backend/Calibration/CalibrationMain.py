import cv2 
import numpy as np
import math
import time
from .Utils import *
from sympy import *
from .ellipseToCircle import *
from .Contrast import applyContrast
import pickle
DEBUG = False

def findEllipse(edged, image_proc_img):

    Ellipse = EllipseDef()

    contours, _ =  cv2.findContours(edged, 1, 2)
    # countur = image_proc_img.copy()
    # cv2.drawContours(countur, contours, -1, (0, 255, 0), 3)
    # cv2.imshow("all-counturs", countur)
    minThresE = 100000
    maxThresE = 150000
    for cnt in contours:
        print(cv2.contourArea(cnt));
        try:  # threshold critical, change on demand?
            area = cv2.contourArea(cnt);
            if minThresE < area < maxThresE:
                
                ellipse = cv2.fitEllipse(cnt)
                
                x, y = ellipse[0]
                a, b = ellipse[1] 
                angle = ellipse[2]
                # y += 4
                # x += 1
                a -= 2
                b -= 2
                # cv2.drawContours(image_proc_img, cnt, -1, (0, 255, 0), 2)
                
                a = a / 2
                b = b / 2
                cv2.ellipse(image_proc_img, (int(x), int(y)), (int(a), int(b)), int(angle), 0.0, 360.0,
                            (255, 0, 0), 1)
                cv2.circle(image_proc_img,  (int(x), int(y)), 5, (255, 255, 0), -1)
  
                Ellipse.a = a
                Ellipse.b = b
                Ellipse.x = x
                Ellipse.y = y
                Ellipse.angle = angle
        # corrupted file
        except:
            continue
    return Ellipse, image_proc_img

def findSectorLines(edged, image_proc_img, calData):

    # fit line to find intersec point for dartboard center point
    #LEFT
    lines = cv2.HoughLines(edged, 1, np.pi / 135, 100)
    #Right
    # lines = cv2.HoughLines(edged, 1, np.pi / 135, 105)
    
    center= (400,300)
    horizontal_offset = 100
    vertical_offset = 100
    intersectLines = []
    intersectLines_XY_coord = []
    ## sector angles important -> make accessible
    for line in lines:
        # rho, theta = line[0]
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 2000 * (-b))
        y1 = int(y0 + 2000 * (a))
        x2 = int(x0 - 2000 * (-b))
        y2 = int(y0 - 2000 * (a))
        if theta > np.pi / 180 * calData.angleZone_horizontal[0] and theta < np.pi / 180 * calData.angleZone_horizontal[1]:
            cv2.line(image_proc_img, (x1,y1),(x2, y2), (0, 0, 255),2)              
            intersectLines.append(line[0])
            intersectLines_XY_coord.append([(x1,y1),(x2,y2)])
        elif theta > np.pi / 180 * calData.angleZone_vertical[0] and theta < np.pi / 180 * calData.angleZone_vertical[1]:
            cv2.line(image_proc_img, (x1,y1),(x2, y2), (0, 255, 0),2)     
            intersectLines.append(line[0])
            intersectLines_XY_coord.append([(x1,y1),(x2,y2)])
    
    # if len(intersectLines) == 2:
    #     x, y = intersection(intersectLines[0], intersectLines[1])
    # else:
    #     x, y = segmented_intersections(intersectLines)    

    # cv2.circle(image_proc_img,  (int(x), int(y)), 5, (255, 0, 255), -1)
    
    
    return intersectLines_XY_coord, image_proc_img

def locateRedSpots(img):

    result = img.copy()
    # lower mask (0-10)
    lower_red = np.array([0,0,50])
    upper_red = np.array([50,255,255])
    mask0 = cv2.inRange(img, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([0,0,50])
    upper_red = np.array([255,100,100])
    mask1 = cv2.inRange(img, lower_red, upper_red)

    # upper mask (170-180)
    lower_red_green = np.array([0,0,50])
    upper_red_green = np.array([255,50, 255])
    mask0_red_green = cv2.inRange(img, lower_red_green, upper_red_green)
    # upper mask (170-180)
    lower_red_green = np.array([0,0,50])
    upper_red_green = np.array([100,255, 100])
    mask1_red_green = cv2.inRange(img, lower_red_green, upper_red_green)

    lower_blue = np.array([0,0,0])
    upper_blue = np.array([255,255, 60])
    mask1_blue = cv2.inRange(img, lower_blue, upper_blue)

    # join my masks
    mask = mask1+mask1_red_green + mask0 + mask0_red_green + mask1_blue 
    result = cv2.bitwise_and(result, result, mask=mask)
    cv2.imshow("result", result)
    
    cv2.imshow("mask", mask)
    
    ret, thresh = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY_INV)
    
    cv2.imshow("first", thresh)
    kernel = np.ones((9,9), np.uint8) 
    thresh2 = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
   
    cv2.imshow("result-mask-tresh", thresh2)
    
    # kernel = np.ones((3, 3), np.uint8) 
    # thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_ERODE, kernel)
    # cv2.imshow("result-ERODE", thresh2)
    # kernel = np.ones((3, 3), np.uint8) 
    # thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel) 
    # cv2.imshow("result-OPEN", thresh2)
    test =2
    
def getEdges(tresh):
    edged_tresh = cv2.morphologyEx(tresh, cv2.MORPH_OPEN , cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    edged = cv2.Canny(edged_tresh, 250, 255)  # imCal

    cv2.imshow("canny", edged)
    return edged

def applyFilters(image_proc_img):
    cv2.imshow("original", image_proc_img)
    
    image_proc_img = applyContrast(image_proc_img, 300, 175)
    cv2.imshow("contrast", image_proc_img)
    blurred = cv2.GaussianBlur(image_proc_img, (3, 3), -1)
    # gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
    # cv2.imshow("1-gray", gray)
    
    # return the edged image
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    cv2.imshow("2-hsv", hsv)
    
    h, s, hsv = cv2.split(hsv)
    
    ret, tresh = cv2.threshold(hsv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow("3-treshold-hsv", tresh)
    return tresh

def smoothEllipse(tresh):
    # open -> erode then dilate
    # close -> dilate then erode
    # smooth out board to get an even ellipse
    pre_processing_ellipse = cv2.morphologyEx(tresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    pre_processing_ellipse = cv2.morphologyEx(pre_processing_ellipse, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
    return pre_processing_ellipse
    
def preProcessImage(image_proc_img):
    tresh = applyFilters(image_proc_img)

    pre_processing_lines = getEdges(tresh)
    pre_processing_ellipse = smoothEllipse(tresh)

    return pre_processing_lines, pre_processing_ellipse
    
def getIntersectionPointsFromEllipse(image_proc_img, calData):

    # preprocess image in order to locate a well mapped Ellipse and to get two lines intersecting it in 4 diagonal points
    pre_processed_lines, pre_processed_ellipse = preProcessImage(image_proc_img)
    cv2.imshow("3-pre_processing_ellipse", pre_processed_ellipse)

    key = cv2.waitKey(0)
    if key == 1:
        cv2.destroyAllWindows()
    
    # find enclosing ellipse TODO: use HoughEllipse or at least try using it :>    
    Ellipse, image_proc_img = findEllipse(pre_processed_ellipse, image_proc_img)
    cv2.imshow("4-findEllipse", image_proc_img)
    key = cv2.waitKey(0)
    if key == 1:
        cv2.destroyAllWindows()
        
    calData.angleZone_horizontal = (Ellipse.angle + calData.angleZone_horizontal[0] , Ellipse.angle + calData.angleZone_horizontal[1])
    calData.angleZone_vertical  = (Ellipse.angle + calData.angleZone_vertical[0], Ellipse.angle + calData.angleZone_vertical[1])
    lines_seg, image_proc_img = findSectorLines(pre_processed_lines, image_proc_img, calData)
    
    cv2.imshow("5-detectedLines", image_proc_img)
    key = cv2.waitKey(0)
    if key == 1:
        cv2.destroyAllWindows()
    # TODO: optimize angleZones
    intersectPoints, image_proc_img = getEllipseLineIntersection(Ellipse, lines_seg, image_proc_img)

    return intersectPoints

def initCalibration(calData, snapshot, original):
    
    calData.intersectPoints = getIntersectionPointsFromEllipse(snapshot, calData)
    
    test = cv2.waitKey(0)
    if test == 1:
        cv2.destroyAllWindows()
        
 
    calData.transformation_matrix, transformed_image = getFinalTransformationMatrix(original, calData)
        
    cv2.imshow('transformed_image_final', transformed_image)

    
    return calData, transformed_image
    
def calibrate(cam_R, cam_L, isStatic):
#------------------------------------------
 
    if isStatic == false:
        success, image_R = cam_R.read()
        _, image_L = cam_L.read()
        
        snapshot_cam_R = image_R.copy()
        snapshot_cam_L = image_L.copy()
    else:
        print("Could not init camaras - getting last saved image")
        
        cam_R = cv2.imread("cam_R.jpg")
        cam_L = cv2.imread("cam_L.jpg")

        snapshot_cam_R = cam_R.copy()
        snapshot_cam_L = cam_L.copy()
        # snapshot_cam_L = cam_R.copy()
        # snapshot_cam_L = cam_L.copy1()
    
        
#------------------------------------------
    cv2.imwrite("cam_R.jpg", snapshot_cam_R)
    cv2.imwrite("cam_L.jpg", snapshot_cam_L)

    original_R = snapshot_cam_R.copy()
    original_L = snapshot_cam_L.copy()
    

    calData_L, transformed_image_L = initLeft(snapshot_cam_L, original_L)
    calData_R, transformed_image_R = initRight(snapshot_cam_R, original_R)

   
    return calData_R, transformed_image_R, calData_L, transformed_image_L

def initRight(snapshot_cam_R, original_R):
    calData_R = CalibrationData()
    calData_R.angleZone_horizontal = ( -40 , -30)
    calData_R.angleZone_vertical  = (-160, -150)
    calData_R.destinationPoints = [0, 10, 5, 15] # [0, 5, 10, 15]
    calData_R, transformed_image_R = initCalibration(calData_R, snapshot_cam_R, original_R)
    test = cv2.waitKey(0)
    if test == 1:
        cv2.destroyAllWindows()
    # write the calibration data to a file
    calFile = open("calibrationData_R.pkl", "wb")
    pickle.dump(calData_R, calFile, 0)
    calFile.close()
    return calData_R, transformed_image_R

def initLeft(snapshot_cam_L, original_L):
    calData_L = CalibrationData()

    calData_L.angleZone_horizontal = (10, 20)
    calData_L.angleZone_vertical = (120 , 140)
    calData_L.destinationPoints = [9, 19, 14, 4] # [0, 5, 10, 15]
    calData_L, transformed_image_L = initCalibration(calData_L, snapshot_cam_L, original_L)
    test = cv2.waitKey(0)
    if test == 1:
        cv2.destroyAllWindows()
    #write the calibration data to a file
    calFile = open("calibrationData_L.pkl", "wb")
    pickle.dump(calData_L, calFile, 0)
    calFile.close()
    return calData_L, transformed_image_L

if __name__ == '__main__':
    print("Welcome to darts!")
    
    # cam_R = VideoStream(src=1).start() 
    # cam_L = VideoStream(src=0).start()
    
    cam_R = cv2.imread("cam_R.jpg") #
    cam_L = cv2.imread("cam_R.jpg") # 
    calibrate(cam_R, cam_L)
