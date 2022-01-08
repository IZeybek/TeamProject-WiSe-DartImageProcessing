import numpy as np
import math
class EllipseDef:
    def __init__(self):
        self.a = -1
        self.b = -1
        self.x = -1
        self.y = -1
        self.angle = -1

class CalibrationData:
    def __init__(self):
        self.ellipsecenter= (0,0)
        self.intersectPoints = []
        self.ring_radius = [14, 32, 194, 214, 320, 340]
        self.center_dartboard = (400, 400)
        self.sectorangle = 2 * math.pi / 20
        self.destinationPoints = []
        self.transformation_matrix = []

# line intersection
def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.

    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    https://newbedev.com/find-intersection-point-of-two-lines-drawn-using-houghlines-opencv
    """
    rho1, theta1 = line1
    rho2, theta2 = line2
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return (x0, y0)

# all intersections
def segmented_intersections(lines):
    """Finds the intersections between groups of lines."""

    intersections = []
    for i, line1 in enumerate(lines[:-1]):
        for line2 in lines[i+1:]:
            intersections.append(intersection(line1, line2)) 

    x0,y0 = (0,0);
    for x, y in intersections:
        x0 += x
        y0 += y
    return x0/ len(intersections), y0/ len(intersections)


def intersectLineCircle(center, radius, p1, p2):
    baX = p2[0] - p1[0]
    baY = p2[1] - p1[1]
    caX = center[0] - p1[0]
    caY = center[1] - p1[1]

    a = baX * baX + baY * baY
    bBy2 = baX * caX + baY * caY
    c = caX * caX + caY * caY - radius * radius

    pBy2 = bBy2 / a
    q = c / a

    disc = pBy2 * pBy2 - q
    if disc < 0:
        return False, None, False, None

    tmpSqrt = math.sqrt(disc)
    abScalingFactor1 = -pBy2 + tmpSqrt
    abScalingFactor2 = -pBy2 - tmpSqrt

    pint1 = p1[0] - baX * abScalingFactor1, p1[1] - baY * abScalingFactor1
    if disc == 0:
        return True, pint1, False, None

    pint2 = p1[0] - baX * abScalingFactor2, p1[1] - baY * abScalingFactor2
    return True, pint1, True, pint2