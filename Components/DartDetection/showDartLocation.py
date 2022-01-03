import numpy as np
import cv2

def showLatestDartLocationOnBoard(transformed_image, locatedDart_coord, cal_data):
    dart_loc_temp = np.array([[locatedDart_coord[0], locatedDart_coord[1]]], dtype="float32")
    dart_loc_temp = np.array([dart_loc_temp])
    dart_loc = cv2.perspectiveTransform(dart_loc_temp, cal_data.transformation_matrix)
    new_dart_loc = tuple(dart_loc.reshape(1, -1)[0])
    cv2.circle(transformed_image, (int(new_dart_loc[0]), int(new_dart_loc[1])), radius=10, color=(255, 0, 255), thickness=-1)
    cv2.imshow("point detected", transformed_image)
    return new_dart_loc