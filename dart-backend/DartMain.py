import sys
import cv2
from Calibration.CalibrationMain import *
from DartDetection.DartLocation import *
from DartDetection.DartDetection import *

from Calibration.VideoCapture import *
import Webserver.websocket as websocket
import threading
import time

def getVideoStream(src=0):
    try:

        videoStream = VideoStream(src).start()
        _, camRGB = videoStream.read()
        snapshot_cam = camRGB.copy()

    except:
        print("Could not init camaras")
        return None

    return videoStream, snapshot_cam

def dart_main_loop():
    videoStream_L, snapshot_cam_L = getVideoStream(src=0)
    videoStream_R, snapshot_cam_R = getVideoStream(src=1)

    cal_data_R, transformed_image_R, cal_data_L, transformed_image_L = calibrateAll(snapshot_cam_R, snapshot_cam_L)

    # load reference image
    reference_image = snapshot_cam_R.copy()

    # calibration data
    calData_L = None
    draw_L = None
    calData_R = None
    draw_R = None

    # main Loop
    turns = 200
    while turns != 0:
        # calibrate only if websocket thread Event is not set
        if not websocket.CALIBRATION_DONE.is_set():
            # TODO: add new Calibration instead of loading
            calData_L, draw_L, calData_R, draw_R = readCalibrationData()
            websocket.CALIBRATION_DONE.set()

        # reset reference image
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT == 0:
            reference_image = snapshot_cam_R.copy()
            test_image_idx = 0
        websocket.Global_LOCK.release()

        # get new image and calculate dart tip
        _, camRGB = videoStream_R.read()
        snapshot_cam = camRGB.copy()
        test_image = snapshot_cam
        score_ssim, result, dart_contour_points = process_images(reference_image, test_image)

        # get dart tip value if image difference is high enough
        if score_ssim < 0.99:
            # calc result value
            new_dart_coord = showLatestDartLocationOnBoard(draw_R, result, calData_R)
            game_point_result = detect_segment(new_dart_coord, calData_R)
            print("Detected dart. The score is " + str(game_point_result) + " Points!")

            # send result
            websocket.send_changes({"request": 1, "value": game_point_result})

            # increase count, replace reference image
            websocket.increase_image_count()
            reference_image = test_image

        cv2.waitKey(10)

        # check if round is done and wait if true and reset reference images afterwards
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT >= 3:
            websocket.Global_LOCK.release()
            websocket.ROUND_DONE.wait()
            reference_image = snapshot_cam_R.copy()
            websocket.ROUND_DONE.clear()
        else:
            websocket.Global_LOCK.release()

def test_dart_detection():
    imageA = cv2.imread("Links-dart.jpg")
    imageB = cv2.imread("Links-empty.jpg")
    if mode == 1:
        print("Test Wrapper function:")

        # wrapper function
        score_ssim, result, dart_contour_points = process_images(imageA, imageB)

        # draw result
        print("SSIM: " + str(score_ssim))
        cv2.rectangle(imageA, dart_contour_points[0], dart_contour_points[1], (0, 0, 255), 2)
        cv2.circle(imageA, (result[0], result[1]), radius=5, color=(0, 255, 255), thickness=-1)
        cv2.imshow("Original", cv2.resize(imageA, (1920, 1080)))
        cv2.waitKey(0)

def test_dart_main_loop():
    time.sleep(5)
    # load test images
    empty_dart_board = cv2.imread("Websocket_Server_Test_DATA/cam_R_empty.jpg")
    reference_image = empty_dart_board.copy()
    images = [cv2.imread("Websocket_Server_Test_DATA/cam_R_dart1.jpg"), cv2.imread(
        "Websocket_Server_Test_DATA/cam_R_dart2.jpg"),
              cv2.imread("Websocket_Server_Test_DATA/cam_R_dart3.jpg")]
    test_image_idx = 0

    # calibration data
    calData_L = None
    draw_L = None
    calData_R = None
    draw_R = None

    # main Loop
    turns = 200
    while turns != 0:
        # calibrate only if websocket thread Event is not set
        if not websocket.CALIBRATION_DONE.is_set():
            # TODO: add new Calibration instead of loading
            calData_L, draw_L, calData_R, draw_R = readCalibrationData()
            websocket.CALIBRATION_DONE.set()

        # reset reference image
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT == 0:
            reference_image = empty_dart_board.copy()
            test_image_idx = 0
        websocket.Global_LOCK.release()

        # calculate dart tip
        test_image = images[test_image_idx]
        score_ssim, result, dart_contour_points = process_images(reference_image, test_image)

        # get dart tip value if image difference is high enough
        if score_ssim < 0.99:
            # calc result value
            new_dart_coord = showLatestDartLocationOnBoard(draw_R, result, calData_R)
            game_point_result = detect_segment(new_dart_coord, calData_R)
            print("Detected dart. The score is " + str(game_point_result) + " Points!")

            # send result
            websocket.send_changes({"request": 1, "value": game_point_result})

            # increase count, replace reference image
            websocket.increase_image_count()
            reference_image = images[test_image_idx]
            test_image_idx += 1

        cv2.waitKey(10)

        # check if round is done and wait if true and reset reference images afterwards
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT >= 3:
            websocket.Global_LOCK.release()
            websocket.ROUND_DONE.wait()
            reference_image = empty_dart_board.copy()
            test_image_idx = 0
            websocket.ROUND_DONE.clear()
        else:
            websocket.Global_LOCK.release()

        # sleep 4 sec for next calc
        time.sleep(4)

if __name__ == "__main__":

    mode = "Test_Websocket_Server"
    if mode == "Ismael_test":
        test_ismael()
    elif mode == "Test_Dart_Detection":
        test_dart_detection()
    elif mode == "Test_Websocket_Server":
        # start main routine in new Thread
        websocket_server = threading.Thread(target=test_dart_main_loop)
        websocket_server.start()

        # start websocket
        websocket.start_server("localhost", 9000)
