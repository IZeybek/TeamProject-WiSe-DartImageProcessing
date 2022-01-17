from dart_backend.Components.Calibration.CalibrationMain import *
from dart_backend.Components.DartDetection.DartLocation import *
from dart_backend.Components.DartDetection.DartDetection import *
from dart_backend.Components.Calibration.VideoCapture import *
import time


def dual_camera_loop(websocket):
    videoStream_L, snapshot_cam_L = getVideoStream(src=0)
    videoStream_R, snapshot_cam_R = getVideoStream(src=1)

    reference_image_L = snapshot_cam_L.copy()
    reference_image_R = snapshot_cam_R.copy()

    # cal_data_L, transformed_image_L, cal_data_R, transformed_image_R  = calibrateAll(snapshot_cam_L, snapshot_cam_R)
    # TODO: add new Calibration instead of loading
    calData_L, draw_L, calData_R, draw_R = readCalibrationData('calibrationData_L.pkl', 'calibrationData_R.pkl')
    websocket.CALIBRATION_DONE.set()
    # snapshot_cam_L = calData_L.calImage.copy()

    # main Loop
    while True:
        # calibrate only if websocket thread Event is not set
        if not websocket.CALIBRATION_DONE.is_set():
            # TODO: add new Calibration instead of loading
            calData_L, draw_L, calData_R, draw_R = readCalibrationData('calibrationData_L.pkl', 'calibrationData_R.pkl')
            websocket.CALIBRATION_DONE.set()

        # reset reference image
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT == 0:
            reference_image_L = snapshot_cam_L.copy()
            reference_image_R = snapshot_cam_R.copy()
            test_image_idx = 0
        websocket.Global_LOCK.release()

        # get new image and calculate dart tip
        _L, camRGB_L = videoStream_L.read()
        _R, camRGB_R = videoStream_L.read()

        snapshot_cam_L = camRGB_L.copy()
        snapshot_cam_R = camRGB_R.copy()

        rectangle_L = snapshot_cam_L.copy()
        rectangle_R = snapshot_cam_R.copy()

        mse_L, result_L, dart_contour_points_L = process_images(reference_image_L, snapshot_cam_L)
        mse_R, result_R, dart_contour_points_R = process_images(reference_image_R, snapshot_cam_R)


        # get dart tip value if image difference is high enough
        if mse_L > 40 or mse_R > 40:
            # draw images
            cv2.imshow("L - reference_image.jpg", reference_image_L)
            cv2.rectangle("L -rect", rectangle_L, dart_contour_points_L[0], dart_contour_points_L[1], (0, 0, 255), 2)
            cv2.circle(rectangle_L, (result_L[0], result_L[1]), 3, (0, 255, 0), 2)
            cv2.imshow("L - second", rectangle_L)

            cv2.imshow("R - reference_image.jpg", reference_image_R)
            cv2.rectangle("R -rect", rectangle_R, dart_contour_points_R[0], dart_contour_points_R[1], (0, 0, 255), 2)
            cv2.circle(rectangle_R, (result_R[0], result_R[1]), 3, (0, 255, 0), 2)
            cv2.imshow("R - second", rectangle_R)

            # calc result value
            new_dart_coord_L = showLatestDartLocationOnBoard(draw_L, result_L, calData_L)
            new_dart_coord_R = showLatestDartLocationOnBoard(draw_R, result_R, calData_R)

            game_point_result_L = detect_segment(new_dart_coord_L, calData_L)
            game_point_result_R = detect_segment(new_dart_coord_R, calData_R)

            print("Detected dart: ")
            print("     Left  -> " + str(game_point_result_L))
            print("     Right -> " + str(game_point_result_R))
            chosen_score = choose_better_dart(game_point_result_L, game_point_result_R, dart_contour_points_L,
                                              dart_contour_points_R)
            print("     The chosen score is: " + str(chosen_score))

            # send result
            websocket.send_changes({"request": 1, "value": chosen_score})

            # increase count, replace reference image
            websocket.increase_image_count()
            reference_image_L = snapshot_cam_L
            reference_image_R = snapshot_cam_R

        waitForKey()

        # check if round is done and wait if true and reset reference images afterwards
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT >= 3:
            websocket.Global_LOCK.release()
            websocket.ROUND_DONE.wait()
            _L, camRGB_L = videoStream_L.read()
            _R, camRGB_R = videoStream_L.read()
            snapshot_cam_L = camRGB_L.copy()
            snapshot_cam_R = camRGB_R.copy()
            websocket.ROUND_DONE.clear()
        else:
            websocket.Global_LOCK.release()


def waitForKey():
    keyInput = cv2.waitKey(0)
    if keyInput == 1:
        cv2.destroyAllWindows()


def drawRectangle(title ,test_image, result, dart_contour_points):
    rect = test_image.copy()
    cv2.rectangle(rect, dart_contour_points[0], dart_contour_points[1], (0, 0, 255), 2)
    cv2.circle(rect, (result[0], result[1]), radius=5, color=(0, 255, 255), thickness=-1)
    cv2.imshow(title, rect)


def test_dual_camera_loop(websocket):
    time.sleep(5)
    # load test images
    empty_dart_board_L = cv2.imread("loop_specialcase_test/cam_L_empty.jpg")
    empty_dart_board_R = cv2.imread("loop_specialcase_test/cam_R_empty.jpg")
    reference_image_L = empty_dart_board_L.copy()
    reference_image_R = empty_dart_board_R.copy()

    images_L = [cv2.imread("loop_specialcase_test/cam_L_dart1.jpg"),
              cv2.imread("loop_specialcase_test/cam_L_dart2.jpg"),
              cv2.imread("loop_specialcase_test/cam_L_dart3.jpg")]
    images_R = [cv2.imread("loop_specialcase_test/cam_R_dart1.jpg"),
              cv2.imread("loop_specialcase_test/cam_R_dart2.jpg"),
              cv2.imread("loop_specialcase_test/cam_R_dart3.jpg")]
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
            calData_L, draw_L, calData_R, draw_R = readCalibrationData('loop_specialcase_test/calibrationData_L.pkl',
                                                                       'loop_specialcase_test/calibrationData_R.pkl')
            websocket.CALIBRATION_DONE.set()

        # reset reference image
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT == 0:
            reference_image_L = empty_dart_board_L.copy()
            reference_image_R = empty_dart_board_R.copy()
        websocket.Global_LOCK.release()

        # calculate dart tip
        test_image_L = images_L[test_image_idx]
        test_image_R = images_R[test_image_idx]

        mse_L, result_L, dart_contour_points_L = process_images(reference_image_L, test_image_L)
        mse_R, result_R, dart_contour_points_R = process_images(reference_image_R, test_image_R)

        print("MSE_L: " + str(mse_L))
        print("MSE_R: " + str(mse_R))

        # get dart tip value if image difference is high enough
        if mse_L > 40 or mse_R > 40:
            # draw bounding box + point
            rect_L = test_image_L.copy()
            rect_R = test_image_R.copy()
            drawRectangle("L - rect", rect_L, result_L, dart_contour_points_L)
            drawRectangle("R - rect", rect_R, result_R, dart_contour_points_R)


            # calc result value
            new_dart_coord_L = showLatestDartLocationOnBoard(draw_L, result_L, calData_L)
            new_dart_coord_R = showLatestDartLocationOnBoard(draw_R, result_R, calData_R)

            game_point_result_L = detect_segment(new_dart_coord_L, calData_L)
            game_point_result_R = detect_segment(new_dart_coord_R, calData_R)


            print("Detected dart: ")
            print("     Left  -> " + str(game_point_result_L))
            print("     Right -> " + str(game_point_result_R))
            chosen_score = choose_better_dart(game_point_result_L, game_point_result_R, dart_contour_points_L, dart_contour_points_R)
            print("     The choosen score is: " + str(chosen_score))

            # send result
            websocket.send_changes({"request": 1, "value": chosen_score})

            # increase count, replace reference image
            websocket.increase_image_count()
            reference_image_L = images_L[test_image_idx]
            reference_image_R = images_R[test_image_idx]

            test_image_idx += 1

        cv2.waitKey(10)

        # check if round is done and wait if true and reset reference images afterwards
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT >= 3:
            websocket.Global_LOCK.release()
            websocket.ROUND_DONE.wait()
            reference_image_L = empty_dart_board_L.copy()
            reference_image_R = empty_dart_board_R.copy()

            test_image_idx = 0
            websocket.ROUND_DONE.clear()
        else:
            websocket.Global_LOCK.release()

        # sleep 4 sec for next calc
        time.sleep(4)
