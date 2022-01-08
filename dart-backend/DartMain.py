
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
     # load the two input images
    imageA = cv2.imread("Links-dart.jpg")
    imageB = cv2.imread("Links-empty.jpg")
    cal_data, transformed_image = getCalibration(imageA,imageA)
    
    result = getResult(imageA, imageB)
    
     
    new_dart_coord = showLatestDartLocationOnBoard(transformed_image, result, cal_data)
    game_point_result = detect_segment(new_dart_coord, cal_data)
    cv2.putText(transformed_image, str(game_point_result), (int(new_dart_coord[0]),int(new_dart_coord[1])), cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.imshow("player Points detected", transformed_image)
    cv2.waitKey(0)