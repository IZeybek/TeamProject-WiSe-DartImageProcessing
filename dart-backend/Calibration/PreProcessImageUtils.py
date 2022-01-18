import numpy as np
import cv2
from .Contrast import applyContrast
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
   
    cv2.imshow("result-mask-tresh", thresh2)
    
    # kernel = np.ones((3, 3), np.uint8) 
    # thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_ERODE, kernel)
    # cv2.imshow("result-ERODE", thresh2)
    # kernel = np.ones((3, 3), np.uint8) 
    # thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel) 
    # cv2.imshow("result-OPEN", thresh2)
    test = 2
    
def getCanny(tresh):
    edged_tresh = cv2.morphologyEx(tresh, cv2.MORPH_CLOSE , cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    edged_tresh = cv2.morphologyEx(edged_tresh, cv2.MORPH_OPEN , cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    edged_tresh = cv2.GaussianBlur(edged_tresh, (5, 5), -1)
    cv2.imshow("blurrEdge", edged_tresh)
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
 
def preProcessImage(image_proc_img):
    tresh = applyFilters(image_proc_img)

    pre_processed_lines = getCanny(tresh)
    pre_processed_ellipse = smoothEllipse(tresh)

    return pre_processed_lines, pre_processed_ellipse