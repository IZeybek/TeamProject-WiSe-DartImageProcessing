# import the necessary packages
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import cv2
import numpy as np

# load the two input images
imageA = cv2.imread("Rechts-dart.jpg")
imageB = cv2.imread("Rechts-empty.jpg")
# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# get rid of dark spots in arrow
kernel = np.ones((10, 10), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
kernel = np.ones((10, 10), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
dart_contour = []
dart_contour_points = None
for c in cnts:
    # compute the bounding box of the contour and then draw the
    # bounding box on both input images to represent where the two
    # images differ
    (x, y, w, h) = cv2.boundingRect(c)
    if len(c) > len(dart_contour):
        dart_contour = c
        dart_contour_points = ((x, y), (x + w, y + h))
    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

vx, vy, x, y = cv2.fitLine(dart_contour, cv2.DIST_L2, 0, 0.01, 0.01)
# calc line which divides the objects
nx, ny = 1, -vx / vy
mag = np.sqrt((1 + ny ** 2))
vx1, vy1 = nx / mag, ny / mag

# Now find two extreme points on the line to draw line
lefty_1 = int((-x * vy / vx) + y)
righty_1 = int(((grayA.shape[1] - x) * vy / vx) + y)

lefty_2 = int((-x * vy1 / vx1) + y)
righty_2 = int(((grayA.shape[1] - x) * vy1 / vx1) + y)

# Now create the Points

extreme_point_1_r = (grayA.shape[1] - 1, righty_1)
extreme_point_1_l = (0, lefty_1)
extreme_point_2_r = (grayA.shape[1] - 1, righty_2)
extreme_point_2_l = (0, lefty_2)


# calc line segment intersection:
def calc_bounding_box_intersection(a, b, p, slope):
    new_points = []
    offset = p[1][0] - (slope * p[0][0])

    # left edge
    y1 = slope * a[0] + offset
    if y1 >= a[1] and y1 <= b[1]:
        new_points.append((int(a[0]), int(y1)))

    # right edge
    y2 = slope * b[0] + offset
    if y2 >= a[1] and y2 <= b[1]:
        new_points.append((int(b[0]), int(y2)))

    # top edge
    x1 = (a[1] - offset) / slope
    if x1 >= a[0] and x1 <= b[0]:
        new_points.append((int(x1), int(a[1])))

    # bottom edge
    x2 = (b[1] - offset) / slope
    if x2 >= a[0] and x2 <= b[0]:
        new_points.append((int(x2), int(b[1])))

    return new_points

def choose_dart_tip(contour, dart_tips, extreme_point_1, extreme_point_2):
    points_underneath_line = 0
    points_over_line = 0
    for p in contour:
        # check if point is underneath and add counter
        if np.cross(p - np.array(extreme_point_1), np.array(extreme_point_2) - np.array(extreme_point_1)) < 0:
            points_underneath_line = points_underneath_line + 1
        else:
            points_over_line = points_over_line + 1

    for p in dart_tips:
        if points_underneath_line > points_over_line and np.cross(p - np.array(extreme_point_1), np.array(extreme_point_2) - np.array(extreme_point_1)) < 0:
            return p
        elif points_underneath_line <= points_over_line and np.cross(p - np.array(extreme_point_1), np.array(extreme_point_2) - np.array(extreme_point_1)) >= 0:
            return p
        else:
            print("Error no Point found!")
            return None


cv2.line(imageA, extreme_point_1_r, extreme_point_1_l, 255, 2)
cv2.line(imageA, extreme_point_2_r, extreme_point_2_l, 255, 2)

slope = (extreme_point_1_l[1] - extreme_point_1_r[1]) / (extreme_point_1_l[0] - extreme_point_1_r[0])
print("slope: " + str(slope))
points = calc_bounding_box_intersection(dart_contour_points[0], dart_contour_points[1], (x, y), slope)
result = choose_dart_tip(dart_contour_points, points, extreme_point_2_l, extreme_point_2_r)

# choose point:
for point in points:
    print(point)
    cv2.circle(imageA, (point[0], point[1]), radius=10, color=(0, 255, 0), thickness=-1)
cv2.circle(imageA, (result[0], result[1]), radius=10, color=(0, 255, 255), thickness=-1)

# Finally draw the lines and intersection point


# show the output images
cv2.imshow("Original", cv2.resize(imageA, (1920, 1080)))
# cv2.imshow("Modified", cv2.resize(imageB, (1920, 1080)))
# cv2.imshow("Diff", cv2.resize(diff, (1920, 1080)))
cv2.imshow("Thresh", cv2.resize(thresh, (1920, 1080)))
cv2.waitKey(0)
