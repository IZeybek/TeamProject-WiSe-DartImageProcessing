import numpy as np
import cv2
import math

game_points_array = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

map_board_game_points = {}
for index, point in enumerate(game_points_array):
    offset = (index - 5) % len(game_points_array)
    map_board_game_points[offset] = point

def showLatestDartLocationOnBoard(transformed_image, locatedDart_coord, cal_data):
    dart_loc_temp = np.array([[locatedDart_coord[0], locatedDart_coord[1]]], dtype="float32")
    dart_loc_temp = np.array([dart_loc_temp])
    dart_loc = cv2.perspectiveTransform(dart_loc_temp, cal_data.transformation_matrix)
    new_dart_loc = tuple(dart_loc.reshape(1, -1)[0])
    cv2.circle(transformed_image, (int(new_dart_loc[0]), int(new_dart_loc[1])), radius=7, color=(0, 255, 255), thickness=-1)
    cv2.imshow("point detected", transformed_image)
    return new_dart_loc

def detect_segment(new_dart_coord, calData):
    x = new_dart_coord[0]
    y = new_dart_coord[1]
    center = 400
    distance_x = center - x 
    distance_y = center - y 
    distance_of_point_to_center = math.sqrt(distance_x**2 + distance_y**2)
    result_ring = -1
    for index, ring in enumerate(calData.ring_radius):
        inner_ring = ring
        outer_ring = calData.ring_radius[(index+1) % 6]
        if index == 0 and distance_of_point_to_center < inner_ring:
            print("first Ring")
            result_ring = 0 
            continue
        elif distance_of_point_to_center > inner_ring and  distance_of_point_to_center < outer_ring:
            print("between middle and outer " + str(index + 1))
            result_ring = index + 1
            continue
        elif index == 5 and distance_of_point_to_center > inner_ring:
            print("not within boundingbox " + str(index + 1))
            result_ring = -1
            continue
            
    theta = math.degrees(math.atan2(y - center, x - center))
    if theta < 0:
        theta = theta + 360
    result_point_amount = -1
    
    for i in range(0, 20):
        sectorAngle1 = getSectorAngle(i,calData)
        nextIndex = (i + 1) % 20
        sectorAngle2 = getSectorAngle(nextIndex,calData)
        degree1 = math.degrees(sectorAngle1)
        degree2 = math.degrees(sectorAngle2)
        
        if  degree1 < theta < degree2:
            index = (i + 1) % 20
            print("its within sector " + str(i) + " and " + str(index))
            if result_ring == 0:
                result_point_amount = 50
            elif result_ring == 1:
                result_point_amount = 25
            elif result_ring == 3:
                result_point_amount = map_board_game_points[index] * 2
            elif result_ring == 5:
                result_point_amount = map_board_game_points[index] * 3
            elif result_ring == -1:
                result_point_amount = -1
            else:
                result_point_amount = map_board_game_points[index]
            
    print("your recent point equals = " + str(result_point_amount))
    return result_point_amount

def getSectorAngle(i, calData):
    return (0.5 + i) * calData.sectorangle