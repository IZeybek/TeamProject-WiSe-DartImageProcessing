# import the necessary packages
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import cv2
import numpy as np


def preprocess_image(img_a, img_b):
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # calc the difference between the two greyscale images to detect the thrown dart
    ssim_score, diff = calc_ssim(grayA, grayB)

    # threshold the difference image to get a clear dart
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # now get rid of black pixels in the dart
    kernel = np.ones((10, 10), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
    kernel = np.ones((10, 10), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel)

    return grayA, grayB, thresh, diff, ssim_score


def calc_ssim(img_a, img_b):
    # compute the Structural Similarity Index (SSIM) between the two images, can later be used to detect if a dart
    # has been thrown or not
    (score, diff) = compare_ssim(img_a, img_b, full=True)
    diff = (diff * 255).astype("uint8")
    return score, diff


def get_dart_contour(img):
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


def calc_object_lines(contour):
    # calc line through the object (line1)
    vx, vy, x, y = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)

    # calc line2. This line is orthogonal to line1 and divides the dart in half.
    nx, ny = 1, -vx / vy
    mag = np.sqrt((1 + ny ** 2))
    vx1, vy1 = nx / mag, ny / mag

    # calc two points on line1
    fit_line_l = int((-x * vy / vx) + y)
    fit_line_r = int(((grayA.shape[1] - x) * vy / vx) + y)
    ort_line_l = int((-x * vy1 / vx1) + y)
    ort_line_r = int(((grayA.shape[1] - x) * vy1 / vx1) + y)

    # calc 2 points on line2
    p_line_r = (grayA.shape[1] - 1, fit_line_r)
    p_line_l = (0, fit_line_l)
    p_ort_line_r = (grayA.shape[1] - 1, ort_line_r)
    p_ort_line_l = (0, ort_line_l)

    # calc slope of line through dart
    slope = (p_line_l[1] - p_line_r[1]) / (p_line_l[0] - p_line_r[0])

    return x, y, slope, p_line_r, p_line_l, p_ort_line_r, p_ort_line_l


def calc_bounding_box_intersection(a, b, p, slope):
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


def choose_dart_tip(contour, dart_tips, point_1, point_2):
    points_underneath_line = 0
    points_over_line = 0

    # check if pixel in contour is over or underneath the line defined by point_1 and point_2
    for p in contour:
        # check if point is underneath and add counter
        if np.cross(p - np.array(point_1), np.array(point_2) - np.array(point_1)) < 0:
            points_underneath_line = points_underneath_line + 1
        else:
            points_over_line = points_over_line + 1

    # check which one of our two points is the dart-tip.
    for p in dart_tips:
        if points_underneath_line > points_over_line and np.cross(p - np.array(point_1),
                                                                  np.array(point_2) - np.array(
                                                                          point_1)) > 0:
            return p
        elif points_underneath_line <= points_over_line and np.cross(p - np.array(point_1),
                                                                     np.array(point_2) - np.array(
                                                                             point_1)) <= 0:
            return p
        else:
            print("Error no Point found!")
            return None

def calc_dart_tip():
    return


# main class for testing
if __name__ == "__main__":
    mode = 0

    if mode == 0:
        print("Test in Mode1:")

        # load the two input images
        imageA = cv2.imread("Rechts-dart.jpg")
        imageB = cv2.imread("Rechts-empty.jpg")

        # preprocess image
        grayA, grayB, thresh, diff, score_ssim = preprocess_image(imageA, imageB)
        print("SSIM: {}".format(score_ssim))

        # get contour of dart from image
        dart_contour, dart_contour_points = get_dart_contour(thresh)

        # draw contour
        cv2.rectangle(imageA, dart_contour_points[0], dart_contour_points[1], (0, 0, 255), 2)
        cv2.rectangle(imageB, dart_contour_points[0], dart_contour_points[1], (0, 0, 255), 2)

        # calc 2 lines: 1. through the object (x, y, slope, p_line_r, p_line_l)
        # and a 2. line orthogonal through the object p_ort_line_r, p_ort_line_l
        x, y, slope, p_line_r, p_line_l, p_ort_line_r, p_ort_line_l = calc_object_lines(dart_contour)

        # draw these lines
        cv2.line(imageA, p_line_r, p_line_l, 255, 2)
        cv2.line(imageA, p_ort_line_r, p_ort_line_l, 255, 2)

        # calc intersection points between the bounding box and line through the object.
        points = calc_bounding_box_intersection(dart_contour_points[0], dart_contour_points[1], (x, y), slope)

        # Choose the point which is the tip of the dart
        result = choose_dart_tip(dart_contour, points, p_ort_line_l, p_ort_line_r)

        # draw intersection points green
        for point in points:
            print(point)
            cv2.circle(imageA, (point[0], point[1]), radius=5, color=(0, 255, 0), thickness=-1)

        # draw dart tip yellow
        cv2.circle(imageA, (result[0], result[1]), radius=5, color=(0, 255, 255), thickness=-1)

        # show the output images
        cv2.imshow("Original", cv2.resize(imageA, (1920, 1080)))
        cv2.imshow("Modified", cv2.resize(imageB, (1920, 1080)))
        cv2.imshow("Diff", cv2.resize(diff, (1920, 1080)))
        cv2.imshow("Thresh", cv2.resize(thresh, (1920, 1080)))
        cv2.waitKey(0)

    if mode == 1:
        print("Test in Mode 2:")

        # load the two input images
        imageA = cv2.imread("Rechts-dart.jpg")
        imageB = cv2.imread("Rechts-empty.jpg")