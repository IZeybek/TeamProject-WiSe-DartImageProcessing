from .Calibration.CalibrationMain import *
from .DartDetection.DartLocation import *
from .DartDetection.DartDetection import *
from .Calibration.VideoCapture import *
import time


def dual_camera_loop(websocket, calibrateOrRead="readCal"):
    videoStream_L, snapshot_cam_L = getVideoStream(src=1)
    videoStream_R, snapshot_cam_R = getVideoStream(src=0)

    reference_image_L = snapshot_cam_L.copy()
    reference_image_R = snapshot_cam_R.copy()

    if calibrateOrRead == "readCal":
        calData_L, draw_L, calData_R, draw_R = readCalibrationData('Calibration_standard_output/calibrationData_L.pkl', 'Calibration_standard_output/calibrationData_R.pkl')
    elif calibrateOrRead == 'newCal':
        calData_L, draw_L, calData_R, draw_R  = calibrateAll(snapshot_cam_L, snapshot_cam_R)
        
    websocket.CALIBRATION_DONE.set()
    
    # main Loop
    transformed_image_L = reference_image_L
    transformed_image_R = reference_image_R
    while True:
        # handle dart missed message
        websocket.send_missed_counter()

        # calibrate only if websocket thread Event is not set
        if not websocket.CALIBRATION_DONE.is_set():
            print("calibrating...")
            try:
                temp_reference_L, temp_reference_R = waitForStabilizedImage(videoStream_L, videoStream_R, websocket)
                orientation = websocket.get_Orientation()
                if orientation == 'left':
                    calData_L, draw_L = calibrateLeft(temp_reference_L, temp_reference_L.copy())
                elif orientation == 'right':
                    calData_R, draw_R = calibrateRight(temp_reference_R, temp_reference_R.copy())
                elif orientation == 'both':
                    calData_L, draw_L, calData_R, draw_R = calibrateAll(temp_reference_L, temp_reference_R)
            except:
                print("Error while calibrating!")
            
            print("calibrating DONE!")
            websocket.CALIBRATION_DONE.set()
            websocket.reset_image_count()
        
        # reset reference image
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT == 0:
            reference_image_L = snapshot_cam_L.copy()
            reference_image_R = snapshot_cam_R.copy()

        websocket.Global_LOCK.release()

        camRGB_L, camRGB_R = waitForStabilizedImage(videoStream_L, videoStream_R, websocket)
    
        snapshot_cam_L = camRGB_L.copy()
        snapshot_cam_R = camRGB_R.copy()

        rectangle_L = snapshot_cam_L.copy()
        rectangle_R = snapshot_cam_R.copy()

        mse_L, result_L, dart_contour_points_L = process_images(reference_image_L, snapshot_cam_L)
        mse_R, result_R, dart_contour_points_R = process_images(reference_image_R, snapshot_cam_R)
        print('mse_L', mse_L, 'mse_R', mse_R)
        
        # get dart tip value if image difference is high enough
        if 40 < mse_L < 150 or 40 < mse_R < 150:
            # draw images
            cv2.imshow("L - reference_image.jpg", reference_image_L)
            cv2.rectangle(rectangle_L, dart_contour_points_L[0], dart_contour_points_L[1], (0, 0, 255), 2)
            cv2.circle(rectangle_L, (result_L[0], result_L[1]), 3, (0, 255, 0), 2)
            cv2.imshow("L - second", rectangle_L)

            cv2.imshow("R - reference_image.jpg", reference_image_R)
            cv2.rectangle(rectangle_R, dart_contour_points_R[0], dart_contour_points_R[1], (0, 0, 255), 2)
            cv2.circle(rectangle_R, (result_R[0], result_R[1]), 3, (0, 255, 0), 2)
            cv2.imshow("R - second", rectangle_R)

            # calc result value
            new_dart_coord_L, transformed_image_L = showLatestDartLocationOnBoard(draw_L, result_L, calData_L)
            new_dart_coord_R, transformed_image_R = showLatestDartLocationOnBoard(draw_R, result_R, calData_R)
            
            game_point_result_L = detect_segment(new_dart_coord_L, calData_L)
            game_point_result_R = detect_segment(new_dart_coord_R, calData_R) 

            chosen_point = choose_better_dart(new_dart_coord_L, new_dart_coord_R, dart_contour_points_L,
                                            dart_contour_points_R)
            if chosen_point == None:
                print("Error pls try again")
                continue
            
            new_diff_score = detect_segment(chosen_point, calData_R) 
            cv2.circle(transformed_image_L, (int(chosen_point[0]), int(chosen_point[1])), radius=7, color=(255, 0, 255), thickness=-1)
            cv2.circle(transformed_image_R, (int(chosen_point[0]), int(chosen_point[1])), radius=7, color=(255, 0, 255), thickness=-1)
            
            print("Detected dart: ")
            print("     Left  -> " + str(game_point_result_L))
            print("     Right -> " + str(game_point_result_R))
            print("     The chosen score is: " + str(new_diff_score))


            # increase count, replace reference image
            websocket.increase_image_count()
            reference_image_L = snapshot_cam_L
            reference_image_R = snapshot_cam_R
            
            # send result
            websocket.send_changes({"request": 1, "value": new_diff_score})
            websocket.send_counter()
        
        
        cv2.imshow("point detected_L", transformed_image_L)
        cv2.imshow("point detected_R", transformed_image_R)
        
        cv2.waitKey(1)
            # check if round is done and wait if true and reset reference images afterwards
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT >= 3:
            
            websocket.Global_LOCK.release()
            websocket.send_stillLoading("roundDone")
            websocket.ROUND_DONE.wait()
            camRGB_L, camRGB_R = waitForStabilizedImage(videoStream_L, videoStream_R,websocket)
            websocket.send_stillLoading("loading")
            snapshot_cam_L = camRGB_L.copy()
            snapshot_cam_R = camRGB_R.copy()
            cv2.imshow("point detected_L", snapshot_cam_L)
            cv2.imshow("point detected_R", snapshot_cam_R)
            websocket.ROUND_DONE.clear()
        else:
            websocket.Global_LOCK.release()
            
        websocket.send_stillLoading("ready")



def waitForStabilizedImage(videoStream_L,videoStream_R,websocket):
    # get new image and calculate dart tip
    _L, temp_reference_L = videoStream_L.read()
    _R, temp_reference_R = videoStream_R.read()
    
    snapshot_cam_L = temp_reference_L.copy()
    snapshot_cam_R = temp_reference_R.copy()
    mse_R = 45
    mse_L = 45
    counter = 0
    while mse_L > 40 or mse_R > 40:

        if counter > 1:
            print("shaking")
        
        if counter == 1:
            websocket.send_stillLoading("loading")
        _L, new_L = videoStream_L.read()
        _R, new_R = videoStream_R.read()
        snapshot_cam_L = new_L.copy()
        snapshot_cam_R = new_R.copy()
        mse_L, _, _ = process_images(temp_reference_L.copy(), snapshot_cam_L)
        mse_R, _, _ = process_images(temp_reference_R.copy(), snapshot_cam_R)
        temp_reference_L = new_L.copy()
        temp_reference_R = new_R.copy()
        counter += 1
        
    
    return snapshot_cam_L, snapshot_cam_R

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
        if mse_L > 45 or mse_R > 45:
            # draw bounding box + point
            rect_L = test_image_L.copy()
            rect_R = test_image_R.copy()
            drawRectangle("L - rect", rect_L, result_L, dart_contour_points_L)
            drawRectangle("R - rect", rect_R, result_R, dart_contour_points_R)


            # calc result value
            new_dart_coord_L, transformed_image_L = showLatestDartLocationOnBoard(draw_L, result_L, calData_L)
            cv2.imshow("point detected_L", transformed_image_L)
            new_dart_coord_R, transformed_image_R = showLatestDartLocationOnBoard(draw_R, result_R, calData_R)
            cv2.imshow("point detected_R", transformed_image_R)

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
            websocket.send_counter()
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
