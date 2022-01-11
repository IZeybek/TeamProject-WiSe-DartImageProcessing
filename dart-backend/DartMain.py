
import sys
sys.path

import cv2
import numpy as np
from Calibration.CalibrationMain import *
from Calibration.StartCalibration import *
from DartDetection.DartLocation import *
from DartDetection.DartDetection import *

from Calibration.VideoCapture import *

if __name__ == "__main__":
    
    
    # cam_R = cv2.imread("cam_R.jpg")
    # cam_L = cv2.imread("cam_L.jpg")
    
    cam_L = VideoStream(src=0).start()
    cam_R = VideoStream(src=1).start()
    cal_data_R, transformed_image_R, cal_data_L, transformed_image_L = getCalibration(cam_R, cam_L, isCalibrate=true)
    
    
    
    imageA = cv2.imread("Links-dart.jpg")
    imageB = cv2.imread("Links-empty.jpg")
    
    result = getResult(imageA, imageB)
     
    new_dart_coord = showLatestDartLocationOnBoard(transformed_image_L, result, cal_data_L)
    game_point_result = detect_segment(new_dart_coord, cal_data_L)
    cv2.putText(transformed_image_L, str(game_point_result), (int(new_dart_coord[0]),int(new_dart_coord[1])), cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.imshow("player Points detected - LEFT", transformed_image_L)
    
    new_dart_coord = showLatestDartLocationOnBoard(transformed_image_R, result, cal_data_R)
    game_point_result = detect_segment(new_dart_coord, cal_data_R)
    cv2.putText(transformed_image_R, str(game_point_result), (int(new_dart_coord[0]),int(new_dart_coord[1])), cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.imshow("player Points detected -RIGHT", transformed_image_R)
    cv2.waitKey(0)