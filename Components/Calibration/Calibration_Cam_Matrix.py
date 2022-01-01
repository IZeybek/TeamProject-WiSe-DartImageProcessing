import cv2 
import numpy as np
from Classes import *
from VideoCapture import VideoStream


DEBUG = False

def findEllipse(edged, image_proc_img):

    Ellipse = EllipseDef()

    contours, _ =  cv2.findContours(edged, 1, 2)


    ## contourArea threshold important -> make accessible
    
    cv2.drawContours(image_proc_img, contours, -1, (0, 255, 0), 3)
    cv2.imshow("counturs-all", image_proc_img)
    
    minThresE = 80000
    maxThresE = 150000
    for cnt in contours:
        print(cv2.contourArea(cnt));
        try:  # threshold critical, change on demand?
            area = cv2.contourArea(cnt);
            if minThresE < area < maxThresE:
                
                ellipse = cv2.fitEllipse(cnt)
                test = image_proc_img.copy()
                cv2.ellipse(test, ellipse, (255, 0, 0), 2)
                
                x, y = ellipse[0]
                a, b = ellipse[1]
                angle = ellipse[2]
                
                #cv2.drawContours(image_proc_img, cnt, -1, (255, 0, 0), 10)
                #cv2.imshow("counturs-adasdasd", image_proc_img)
                
                center_ellipse = (x, y)

                a = a / 2
                b = b / 2

                cv2.ellipse(image_proc_img, (int(x), int(y)), (int(a), int(b)), int(angle), 0.0, 360.0,
                            (255, 0, 0), 3)
                cv2.imshow("ellipse", image_proc_img)
                test=1+1
                Ellipse.a = a
                Ellipse.b = b
                Ellipse.x = x
                Ellipse.y = y
                Ellipse.angle = angle
        # corrupted file
        except:
            continue
            return Ellipse, image_proc_img

    
    return Ellipse, image_proc_img

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
    
def initTransformationMatrix(image_proc_img, mount):

    blurred = cv2.GaussianBlur(image_proc_img, (3, 3), -1)
    gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
    
    cv2.imshow("1-gray", gray)
    
    # return the edged image
    edged = cv2.Canny(gray, 245, 255)  # imCal
    cv2.imshow("autocanny", edged)
    ret, inv_edge = cv2.threshold(edged, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow("2-inv_edge", inv_edge)
    
    kernel = np.ones((17, 17), np.uint8) 
    inv_edge = cv2.morphologyEx(inv_edge, cv2.MORPH_ERODE, kernel)
    cv2.imshow("4-erode_edge", inv_edge)
    
    kernel = np.ones((15, 15), np.uint8) 
    inv_edge = cv2.morphologyEx(inv_edge, cv2.MORPH_DILATE, kernel)
    cv2.imshow("5-Dilate_edge", inv_edge)
    
    # find enclosing ellipse
    Ellipse, image_proc_img = findEllipse(inv_edge, image_proc_img)

def calibrate(cam_R, cam_L):
#------------------------------------------
    
    # try:
    #    success, snapshot_cam_R = cam_R.read()
    #    _, snapshot_cam_L = cam_L.read()

    # except:
    #    print("Could not init cams")
    #    return

    # imCal_R = snapshot_cam_R.copy()
    # # imCal_L = snapshot_cam_L.copy()

    # imCalRGBorig = snapshot_cam_R.copy()

#------------------------------------------
    
    snapshot_cam_R = cam_R.copy()
    snapshot_cam_L = cam_L.copy()
    imCal_R = cam_R.copy() #snapshot_cam_R.copy()
    imCal_L = cam_L.copy() #snapshot_cam_L.copy()

    imCalRGBorig = cam_R.copy()

#------------------------------------------
    cv2.imwrite("cam_R.jpg", snapshot_cam_R)     # save calibration frame
    #cv2.imwrite("cam_R_L.jpg", imCalRGB_L)  # save calibration frame

    calData_R = CalibrationData()
    #calData_L = CalibrationData()

    imCal_R = snapshot_cam_R.copy()
    #imCal_L = imCalRGB_L.copy()

    calData_R.points = initTransformationMatrix(imCal_R, "right")
   
    

    print("The dartboard image has now been normalized.")
    print("")

    cv2.imshow('winName4', imCal_R)
    test = cv2.waitKey(0)
    if test == 13:
        cv2.destroyWindow('winName4')
        cv2.destroyAllWindows()
   
    return calData_R #, calData_L


if __name__ == '__main__':
    print("Welcome to darts!")
    
    # cam_R = VideoStream(src=1).start() 
    # cam_L = VideoStream(src=0).start()
    
    cam_R = cv2.imread("cam_R.jpg") #
    cam_L = cv2.imread("cam_R.jpg") # 
    calibrate(cam_R, cam_L)
