import cv2 
import numpy as np
import math
import sys
from .Utils import *

def getEllipseLineIntersection(Ellipse, lines_seg, image_proc_img):
    x = Ellipse.x
    y = Ellipse.y
    
    a = Ellipse.a
    b = Ellipse.b
    angle = (Ellipse.angle) * math.pi / 180
    
    # build transformation matrix http://math.stackexchange.com/questions/619037/circle-affine-transformation
    R1 = np.array([[math.cos(angle), math.sin(angle), 0], [-math.sin(angle), math.cos(angle), 0], [0, 0, 1]])
    T1 = np.array([[1, 0, -x], [0, 1, -y], [0, 0, 1]])
    D = np.array([[1, 0, 0], [0, a / b, 0], [0, 0, 1]])
    M = D.dot(R1.dot(T1))
    
    M_inv = np.linalg.inv(M)
    transformed_intersectpoints = []
    for line in lines_seg:
        x0, y0 = line[0]
        x1, y1 = line[1]
        p1 = M.dot(np.transpose([x0,y0,1]))
        p2 = M.dot(np.transpose([x1,y1,1]))
        x0, y0 = p1[0], p1[1]
        x1, y1 = p2[0], p2[1]
         # # build transformation matrix http://math.stackexchange.com/questions/619037/circle-affine-transformation
        
        slope = (y1 - y0) / (x1 - x0)
        intercept = y0 - (slope * x0)
        
        t_0 = 1 + slope**2
        t_1 = 2 * slope * intercept
        t_2 = intercept**2 - a**2
    
        d = (t_1**2) - (4 * t_0 * t_2)
   
        sol_x0 = (-t_1 - math.sqrt(d))/(2 * t_0)
        sol_x1 = (-t_1 + math.sqrt(d))/(2 * t_0)

        sol_y0 = slope * sol_x0 + intercept
        sol_y1 = slope * sol_x1 + intercept

        inter_p1 = [sol_x0, sol_y0,1]
        inter_p2 = [sol_x1, sol_y1,1]
        inter_p1 = M_inv.dot(np.transpose(inter_p1))
        inter_p2 = M_inv.dot(np.transpose(inter_p2))
        transformed_intersectpoints.append(inter_p1)
        transformed_intersectpoints.append(inter_p2)
    
    # for points in transformed_intersectpoints:
    #      cv2.circle(image_proc_img,  (int(points[0]), int(points[1])), 10, (0, 255, 255), -1)
    point1 = (int(transformed_intersectpoints[0][0]), int(transformed_intersectpoints[0][1]))
    piont2 = (int(transformed_intersectpoints[1][0]), int(transformed_intersectpoints[1][1]))
    piont3 = (int(transformed_intersectpoints[2][0]), int(transformed_intersectpoints[2][1]))
    piont4 = (int(transformed_intersectpoints[3][0]), int(transformed_intersectpoints[3][1]))
    cv2.circle(image_proc_img,  point1, 5, (255, 0, 0), 3)    
    cv2.putText(image_proc_img, str(1), point1, cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.circle(image_proc_img,  piont2, 5, (0, 255, 0), 3)
    cv2.putText(image_proc_img, str(2), piont2, cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.circle(image_proc_img,  piont3, 5, (255, 0, 0), 3)
    cv2.putText(image_proc_img, str(3), piont3, cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.circle(image_proc_img,  piont4, 5, (0, 255, 0), 3) 
    cv2.putText(image_proc_img, str(4), piont4, cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 0, 255), 4, cv2.LINE_AA)
    cv2.imshow("intersection points", image_proc_img)
    return transformed_intersectpoints, image_proc_img

def calculateDstPoint(i, calData):
    dstpoint = [(calData.center_dartboard[0] + calData.ring_radius[5] * math.cos((0.5 + i) * calData.sectorangle)),
                (calData.center_dartboard[1] + calData.ring_radius[5] * math.sin((0.5 + i) * calData.sectorangle))]

    return dstpoint

def nothing(x):
    pass

def createTrackbars():
    cv2.namedWindow('transformation', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('p1_x', 'transformation', 0, 20, nothing)
    cv2.createTrackbar('p1_y', 'transformation', 0, 20, nothing)
    cv2.createTrackbar('p2_x', 'transformation', 0, 20, nothing)
    cv2.createTrackbar('p2_y', 'transformation', 0, 20, nothing)
    cv2.createTrackbar('p3_x', 'transformation', 0, 20, nothing)
    cv2.createTrackbar('p3_y', 'transformation', 0, 20, nothing)
    cv2.createTrackbar('p4_x', 'transformation', 0, 20, nothing)
    cv2.createTrackbar('p4_y', 'transformation', 0, 20, nothing)
    cv2.setTrackbarPos('p1_x', 'transformation', 10)
    cv2.setTrackbarPos('p1_y', 'transformation', 10)
    cv2.setTrackbarPos('p2_x', 'transformation', 10)
    cv2.setTrackbarPos('p2_y', 'transformation', 10)
    cv2.setTrackbarPos('p3_x', 'transformation', 10)
    cv2.setTrackbarPos('p3_y', 'transformation', 10)
    cv2.setTrackbarPos('p4_x', 'transformation', 10)
    cv2.setTrackbarPos('p4_y', 'transformation', 10)
    
    cv2.createTrackbar('1 -> Done', 'transformation', 0, 1, nothing)

def getFinalTransformationMatrix(image, calData):
    image = image.copy()
    intersectPoints = calData.intersectPoints
    createTrackbars()
    
    while (1):
        # get current positions of four trackbars
        
        s = cv2.getTrackbarPos('1 -> Done', 'transformation')
        if s == 1:
            cv2.destroyAllWindows()
            break

        p1_x = cv2.getTrackbarPos('p1_x', 'transformation') - 10
        p1_y = cv2.getTrackbarPos('p1_y', 'transformation') - 10
        p2_x = cv2.getTrackbarPos('p2_x', 'transformation') - 10
        p2_y = cv2.getTrackbarPos('p2_y', 'transformation') - 10
        p3_x = cv2.getTrackbarPos('p3_x', 'transformation') - 10
        p3_y = cv2.getTrackbarPos('p3_y', 'transformation') - 10
        p4_x = cv2.getTrackbarPos('p4_x', 'transformation') - 10
        p4_y = cv2.getTrackbarPos('p4_y', 'transformation') - 10
        trackings = [(p1_x,p1_y),(p2_x,p2_y),(p3_x,p3_y),(p4_x,p4_y)]
        
        dst_points = []
        for dstPoint in calData.destinationPoints:
            dst_points.append(calculateDstPoint(dstPoint, calData))
        
        # finalize transformation matrix
        src_points = []
        for index, point in enumerate(intersectPoints):
            src_points.append((point[0] + trackings[index][0], point[1]+ trackings[index][1]))
        
        transformation_matrix = cv2.getPerspectiveTransform(np.array(src_points, np.float32), np.array(dst_points, np.float32))

        normilzed_board_image = cv2.warpPerspective(image, transformation_matrix, (800, 800))

        normilzed_board_image = getNormilizedBoard(normilzed_board_image, calData)

        for dstPoint in dst_points:
            cv2.circle(normilzed_board_image, (int(dstPoint[0]), int(dstPoint[1])), 2, (255, 255, 0), 2, 4)
        
        for index, point in enumerate(dst_points):
                cv2.putText(normilzed_board_image, str(index+1), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 4, cv2.LINE_AA)
        cv2.imshow('adjusted_image', normilzed_board_image)
        cv2.waitKey(1)
       
    return transformation_matrix, normilzed_board_image

def getSectorAngle(i, calData):
    return (0.5 + i) * calData.sectorangle

def getNormilizedBoard(img, calData):
        center = 400
        for rings in calData.ring_radius:
            cv2.circle(img, (center, center), rings, (255, 255, 255), 1)  # outside double    

        for i in range(0,20):
            sectorAngle = getSectorAngle(i,calData)
            p1 = center + int(calData.ring_radius[1] * math.cos(sectorAngle))
            p2 = center + int(calData.ring_radius[1] * math.sin(sectorAngle))
            cv2.line(img, (p1, p2), (
                int(center + calData.ring_radius[5] * math.cos(sectorAngle)),
                int(center + calData.ring_radius[5] * math.sin(sectorAngle))), (255, 255, 255), 1)

        return img

    
def getIntersectionPointsFromEllipse(image_proc_img, pre_processed_lines, pre_processed_ellipse):

    # find enclosing ellipse TODO: use HoughEllipse or at least try using it :>    
    Ellipse, image_proc_img = findEllipse(pre_processed_ellipse, image_proc_img)
    cv2.imshow("4-findEllipse", image_proc_img)
    
    waitForKey()

    lines_seg, image_proc_img = findSectorLines(pre_processed_lines, image_proc_img, Ellipse)
    
    cv2.imshow("5-detectedLines", image_proc_img)
    waitForKey()
    
    intersectPoints, image_proc_img = getEllipseLineIntersection(Ellipse, lines_seg, image_proc_img)

    return intersectPoints

def smoothEllipse(tresh):
    # open -> erode then dilate
    # close -> dilate then erode
    # smooth out board to get an even ellipse
    pre_processing_ellipse = cv2.morphologyEx(tresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    pre_processing_ellipse = cv2.morphologyEx(pre_processing_ellipse, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    return pre_processing_ellipse

def findSectorLines(edged, image_proc_img, Ellipse):
    
    x_line = cv2.HoughLines(edged, 1, np.pi / 160, 90,100)
    
    horizontal_lines = []
    vertical_lines = []
    intersectLines_XY_coord = []
    
    fixed_horizontal_slope= 0
    fixed_vertical_slope= sys.maxsize
    
    filtered_Lines = []
    horizontal_temp = 75
    vertical_temp = 75

    for line in x_line:
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
        slope = (y1 - y0) / (x1 - x0)
        c= y0-slope
        
        distance = (slope * Ellipse.x - Ellipse.y +c) / (math.sqrt(slope**2 + 1))
        if distance < 300:
            angle_for_vertical_line =  abs(math.degrees(math.atan((slope-fixed_horizontal_slope)/(1+ (slope * fixed_horizontal_slope)))))
            angle_for_horizontal_line = abs(math.degrees(math.atan((slope-fixed_vertical_slope)/(1+ (slope * fixed_vertical_slope)))))
            
            
            cv2.line(image_proc_img, (x1,y1),(x2, y2), (255, 0, 255),1) 
            if angle_for_vertical_line > angle_for_horizontal_line and angle_for_vertical_line > horizontal_temp:

                horizontal_temp = angle_for_vertical_line
                vertical_lines.append([(x1,y1),(x2,y2)])
                filtered_Lines.append([(x1,y1),(x2,y2)])
            elif angle_for_vertical_line < angle_for_horizontal_line and angle_for_horizontal_line > vertical_temp:
                vertical_temp = angle_for_horizontal_line
                horizontal_lines.append([(x1,y1),(x2,y2)])
                filtered_Lines.append([(x1,y1),(x2,y2)])
            
    degree_btw_both_lines = 60
    h = 0
    v = 0
    for x_line in horizontal_lines:
        (x0,y0), (x1,y1) = x_line
        slope_x = (y1 - y0) / (x1 - x0)
        for y_line in vertical_lines:
            (x2,y2), (x3,y3) = y_line
            
            slope_y = (y3 - y2) / (x3 - x2)
            try:
                angle_between =  abs(math.degrees(math.atan((slope_x-slope_y)/(1+ (slope_x * slope_y)))))
                if  angle_between > degree_btw_both_lines:
                    degree_btw_both_lines = angle_between
                    h = [(x0,y0),(x1,y1)]
                    v = [(x2,y2),(x3,y3)]
            except:
                continue
        
    cv2.line(image_proc_img, h[0],h[1], (0, 0, 255),2)  
    cv2.line(image_proc_img, v[0],v[1], (0, 255, 0),2)  
    
    # if len(intersectLines) == 2:
    #     x, y = intersection(intersectLines[0], intersectLines[1])
    # else:
    #     x, y = segmented_intersections(intersectLines)    

    # cv2.circle(image_proc_img,  (int(x), int(y)), 5, (255, 0, 255), -1)
    intersectLines_XY_coord.append(h)
    intersectLines_XY_coord.append(v)
    
    return intersectLines_XY_coord, image_proc_img

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

def waitForKey():
    keyInput = cv2.waitKey(0)
    if keyInput == 1:
        cv2.destroyAllWindows()