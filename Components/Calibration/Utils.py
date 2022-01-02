import numpy as np

class EllipseDef:
    def __init__(self):
        self.a = -1
        self.b = -1
        self.x = -1
        self.y = -1
        self.angle = -1

class CalibrationData:
    def __init__(self):
        #for perspective transform
        self.top = []
        self.bottom = []
        self.left = []
        self.right = []
        self.intersectPoints = []

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