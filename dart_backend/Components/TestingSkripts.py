from .DartDetection.DartDetection import *
from .Calibration.CalibrationMain import *


def test_dart_detection():
    imageA = cv2.imread("loop_test/cam_L_empty.jpg")
    imageB = cv2.imread("loop_test/cam_L_dart1.jpg")

    # wrapper function
    score_ssim, result, dart_contour_points = process_images(imageA, imageB)

    # draw result
    print("MSE: " + str(score_ssim))
    cv2.rectangle(imageA, dart_contour_points[0], dart_contour_points[1], (0, 0, 255), 2)
    cv2.circle(imageA, (result[0], result[1]), radius=5, color=(0, 255, 255), thickness=-1)
    cv2.imshow("Original", cv2.resize(imageA, (1920, 1080)))
    cv2.waitKey(0)


def take_snapshots():
    videoStream_L, snapshot_cam_L = getVideoStream(src=0)
    videoStream_R, snapshot_cam_R = getVideoStream(src=1)
    empty_L = snapshot_cam_L.copy()
    empty_R = snapshot_cam_R.copy()
    cal_data_L, transformed_image_L, cal_data_R, transformed_image_R = calibrateAll(empty_L, empty_R,
                                                                                    'loop_specialcase_test/calibrationData_L.pkl',
                                                                                    'loop_specialcase_test/calibrationData_R.pkl')
    cv2.imwrite("loop_test/cam_L_empty.jpg", snapshot_cam_L)
    cv2.imwrite("loop_test/cam_R_empty.jpg", snapshot_cam_R)
    _, snapshot_cam_L = videoStream_L.read()
    _, snapshot_cam_R = videoStream_R.read()

    cv2.imwrite("loop_test/cam_L_dart1.jpg", snapshot_cam_L)
    cv2.imwrite("loop_test/cam_R_dart1.jpg", snapshot_cam_R)
    _, snapshot_cam_L = videoStream_L.read()
    _, snapshot_cam_R = videoStream_R.read()

    cv2.imwrite("loop_test/cam_L_dart2.jpg", snapshot_cam_L)
    cv2.imwrite("loop_test/cam_R_dart2.jpg", snapshot_cam_R)
    _, snapshot_cam_L = videoStream_L.read()
    _, snapshot_cam_R = videoStream_R.read()

    cv2.imwrite("loop_test/cam_L_dart3.jpg", snapshot_cam_L)
    cv2.imwrite("loop_test/cam_R_dart3.jpg", snapshot_cam_R)


def test_calibration():
    videoStream_L, snapshot_cam_L = getVideoStream(src=0)
    videoStream_R, snapshot_cam_R = getVideoStream(src=1)

    cal_data_L, transformed_image_L, cal_data_R, transformed_image_R = calibrateAll(snapshot_cam_L, snapshot_cam_R)


def test_calibration_2(path_L, path_R):
    image_L = cv2.imread(path_L)
    image_R = cv2.imread(path_R)
    cal_data_L, transformed_image_L, cal_data_R, transformed_image_R = calibrateAll(image_L, image_R)
