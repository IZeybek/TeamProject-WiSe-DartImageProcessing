# import the necessary packages
from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import mean_squared_error
import imutils
import cv2
import math
import numpy as np

def calc_image_difference(image_a, image_b):
    """Calculates the difference between 2 images and creates a new image which contains the difference.

    Parameters
    ----------
    image_a: array
        image of a dartboard with a dart stuck in it
    image_b: array
        image of an empty dart board

    Returns
    -------
    array
        grayA: The grayscale image of img_a.
    array
        grayB: The grayscale image of img_b.
    array
        thresh: The diff img processed with a threshold and smoothed afterwards.
    array
        diff: The full SSIM image multiplied by 255 to create the difference img.
    float
        mse: A score which tells you how identical the images are. (Mean Squared Error)
    """
    # convert the images to grayscale
    grayA = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # calc the difference between the two greyscale images to detect the thrown dart
    ssim_score, diff = calc_ssim(grayA, grayB)
    mse = mean_squared_error(grayA, grayB)

    # threshold the difference image to get a clear dart
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # now get rid of black pixels in the dart
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
    # thresh = cv2.GaussianBlur(thresh, (5, 5), -1)
    if ssim_score == 1:
        return grayA, grayB, thresh, diff, -1
    return grayA, grayB, thresh, diff, mse

def calc_ssim(img_a, img_b):
    """Calculate the difference between 2 images.

    Parameters
    ----------
    img_a: array
        image of a dartboard with a dart stuck in it
    img_b: array
        image of an empty dart board

    Returns
    -------
    array
        diff: The full SSIM image multiplied by 255 to create the difference img.
    float
        score: a score which tells you how identical the images are (1 = identical)
    """
    # compute the Structural Similarity Index (SSIM) between the two images, can later be used to detect if a dart
    # has been thrown or not
    (score, diff) = compare_ssim(img_a, img_b, full=True)
    diff = (diff * 255).astype("uint8")
    return score, diff

def get_dart_contour(img):
    """Calculate the contours of the biggest shape in the img.

    Parameters
    ----------
    img: array
        diff img processed with a threshold and smoothed afterwards.

    Returns
    -------
    array
        dart_contour: An array with all the points in the detected dart contour
    array
        dart_contour_points: An array with 2 points which define the bounding box of the detected dart.
    """
    # find contours in img
    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours and calculate the bounding box.
    # the biggest bounding box should be our dart
    dart_contour = []
    dart_contour_points = None
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if len(c) > len(dart_contour):
            dart_contour = c
            dart_contour_points = ((x, y), (x + w, y + h))
    return dart_contour, dart_contour_points

def calc_object_lines(contour, offset):
    """Calculates a line which goes through the center of the detected dart.

    Parameters
    ----------
    contour: array
        An array with all the points in the detected dart contour.
    offset:
        Max y value in the images

    Returns
    -------
    float
        x: x value of intersection point line1 and line2.
    float
        y: y value of intersection point line1 and line2.
    float
        slope: slope of line1
    tuple
        p_line_r: p1 which defines line1
    tuple
        p_line_l: p2 which defines line1
    """
    # calc line through the object (line1)
    vx, vy, x, y = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)

    # calc two points on line1
    fit_line_l = int((-x * vy / vx) + y)
    fit_line_r = int(((offset - x) * vy / vx) + y)

    # calc 2 points on line2
    p_line_r = (offset - 1, fit_line_r)
    p_line_l = (0, fit_line_l)

    # calc slope of line through dart
    slope = (p_line_l[1] - p_line_r[1]) / (p_line_l[0] - p_line_r[0])

    return x, y, slope, p_line_r, p_line_l

def calc_bounding_box_intersection(a, b, p, slope):
    """Calculate the intersection of a line (defined by p and slope) and the bounding box (defined by a and b)

    Parameters
    ----------
    a: tuple
        left lower corner of the bounding box.
    b: tuple
        right higher corner of the bounding box.
    p: tuple
        point one the line.
    slope: float
        slope of the line which goes through p.

    Returns
    -------
    array
        new_points: An array with the 2 points which intersect the bounding box.
    """
    new_points = []
    offset = p[1][0] - (slope * p[0][0])

    # calc left edge intersection
    y1 = slope * a[0] + offset
    if a[1] <= y1 <= b[1]:
        new_points.append((int(a[0]), int(y1)))

    # calc right edge intersection
    y2 = slope * b[0] + offset
    if a[1] <= y2 <= b[1]:
        new_points.append((int(b[0]), int(y2)))

    # calc top edge intersection
    x1 = (a[1] - offset) / slope
    if a[0] <= x1 <= b[0]:
        new_points.append((int(x1), int(a[1])))

    # calc bottom edge intersection
    x2 = (b[1] - offset) / slope
    if a[0] <= x2 <= b[0]:
        new_points.append((int(x2), int(b[1])))

    return new_points

def choose_dart_tip(thresh, bounding_box, point_1, point_2):
    """Calculate which of the two possible dart_tip locations is correct.

    Parameters
    ----------
    contour: array
        An array with all the points in the detected dart contour.
    point_1: tuple
        1. possible point for the dart tip
    point_2: tuple
        2. possible point for the dart tip

    Returns
    -------
    array
        p: the point of the arrow tip.
    """
    mean_dist_p1 = 0
    mean_dist_p2 = 0
    count = 0
    dart_points = cv2.findNonZero(thresh)

    # calc mean dist from p in countour to point_1 and point_2
    for p in dart_points:
        if bounding_box[0][0] <= p[0][0] <= bounding_box[1][0] and bounding_box[0][1] <= p[0][1] <= bounding_box[1][1]:
            mean_dist_p1 += ((((p[0][0] - point_1[0]) ** 2) + ((p[0][1] - point_1[1]) ** 2)) ** 0.5)
            mean_dist_p2 += ((((p[0][0] - point_2[0]) ** 2) + ((p[0][1] - point_2[1]) ** 2)) ** 0.5)
            count += 1
    mean_dist_p1 = mean_dist_p1 / count
    mean_dist_p2 = mean_dist_p2 / count

    # print("mean_dist_p1: " + str(mean_dist_p1))
    # print("mean_dist_p2: " + str(mean_dist_p2))

    # pick point with the higher mean_dist as tip.
    if mean_dist_p1 > mean_dist_p2:
        return point_1
    else:
        return point_2

def process_images(image_a, image_b):
    """Calculates the difference of 2 images and calculates where the tip of a thrown dart is located.

    Parameters
    ----------
    image_a: array
        image of a dartboard
    image_a: array
        reference image of a dartboard. used to detect changes

    Returns
    -------
    float
        mse: a score which tells you how identical the images are, (Mean Squared Error)
    tuple
        result: a point which tells you where the tip of the dart is located.
    tuple
        dart_contour_points: a tuple which contains 2 points. These points define the bounding box around the dart.
    """
    gray_a, gray_b, thresh, diff, mse = calc_image_difference(image_a, image_b)
    if mse == -1:
        return  mse, None, None
    cv2.imshow("tresh", thresh)
    dart_contour, dart_contour_points = get_dart_contour(thresh)
    x, y, slope, p_line_r, p_line_l = calc_object_lines(dart_contour, gray_a.shape[1])
    points = calc_bounding_box_intersection(dart_contour_points[0], dart_contour_points[1], (x, y), slope)
    result = choose_dart_tip(thresh, dart_contour_points, points[0], points[1])
    area = (dart_contour_points[0][0] - dart_contour_points[1][0]) * (dart_contour_points[0][1] - dart_contour_points[1][1])
    print("area", area)
    # if 60000 < area:
    #     return 1, result, dart_contour_points
    return mse, result, dart_contour_points

def getTestResult(imageA, imageB):
    print("Test functions:")
    # preprocess image
    grayA, grayB, thresh, diff, score_ssim = calc_image_difference(imageA, imageB)
    print("SSIM: " + str(score_ssim))

    # get contour of dart from image
    dart_contour, dart_contour_points = get_dart_contour(thresh)

    # draw contour
    cv2.rectangle(imageA, dart_contour_points[0], dart_contour_points[1], (0, 0, 255), 2)
    cv2.rectangle(imageB, dart_contour_points[0], dart_contour_points[1], (0, 0, 255), 2)

    # calc 2 lines: 1. through the object (x, y, slope, p_line_r, p_line_l)
    # and a 2. line orthogonal through the object p_ort_line_r, p_ort_line_l
    x, y, slope, p_line_r, p_line_l = calc_object_lines(dart_contour, grayA.shape[1])

    # draw these lines
    cv2.line(imageA, p_line_r, p_line_l, 255, 2)

    # calc intersection points between the bounding box and line through the object.
    points = calc_bounding_box_intersection(dart_contour_points[0], dart_contour_points[1], (x, y), slope)

    # Choose the point which is the tip of the dart
    result = choose_dart_tip(dart_contour, points[0], points[1])

    # draw intersection points green
    for point in points:
        print(point)
        cv2.circle(imageA, (point[0], point[1]), radius=5, color=(0, 255, 0), thickness=-1)

    # draw dart tip yellow
    cv2.circle(imageA, (result[0], result[1]), radius=5, color=(0, 255, 255), thickness=-1)

    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified",imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    return result

def choose_better_dart(dart1, dart2, contour1, contour2):
    firstArea = (contour1[0][0] - contour1[1][0]) * (contour1[0][1] - contour1[1][1])
    secondArea = (contour2[0][0] - contour2[1][0]) * (contour2[0][1] - contour2[1][1])
    diffArea = abs(firstArea - secondArea)
    print('firstArea', firstArea, 'secondArea', secondArea)
    print('diffArea', diffArea)
    if diffArea < 15000:
        newDart = ((dart1[0] + dart2[0])/ 2, (dart1[1] + dart2[1])/ 2)
        distance = ((dart1[0] - dart2[0])/ 2, (dart1[1] - dart2[1])/ 2)
        
        newDart_distance = math.sqrt((distance[0]**2 +  distance[1]**2))*2
        print('newDart_distance', newDart_distance)
        if newDart_distance < 25: 
            return (newDart[0], newDart[1]) #(x,y)
        else:
            if firstArea > secondArea:
                
                return dart1
            else:
                return dart2
    elif firstArea < 25000 or secondArea < 25000:
        if firstArea < secondArea:
            return dart1
        else:
            return dart2
    else:
        return None
