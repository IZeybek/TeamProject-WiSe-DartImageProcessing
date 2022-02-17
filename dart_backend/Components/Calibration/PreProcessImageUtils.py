import numpy as np
import cv2
from .Contrast import applyContrast,brighten
from .EllipseUtils import smoothEllipse

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
   
    cv2.imshow("result-mask-thresh", thresh2)
    
    
def getCanny(thresh):
    edged_thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE , cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    edged_thresh = cv2.morphologyEx(edged_thresh, cv2.MORPH_OPEN , cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    edged_thresh = cv2.GaussianBlur(edged_thresh, (5, 5), -1)
    cv2.imshow("blurrEdge", edged_thresh)
    edged = cv2.Canny(edged_thresh, 250, 255)  # imCal

    cv2.imshow("canny", edged)
    return edged

def getthresh(original):
    cv2.imshow("original", original)
    original_copy = original.copy()
    brightend = brighten(original_copy)
    cv2.imshow("1-brightened image", brightend)
    blurred = cv2.GaussianBlur(brightend, (3, 3), -1)
    cv2.imshow("1.1-blurred image", blurred)
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    cv2.imshow("2-hsv", hsv)
    
    h, s, v = cv2.split(hsv)
    
    ret, thresh = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow("3-threshold-hsv", thresh)
    return thresh
 
def preProcessImage(original):
    thresh = getthresh(original)

    pre_processed_lines = getCanny(thresh)
    pre_processed_ellipse = smoothEllipse(thresh)

    return pre_processed_lines, pre_processed_ellipse