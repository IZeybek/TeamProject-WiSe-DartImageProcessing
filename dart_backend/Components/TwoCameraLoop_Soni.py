from .Calibration.VideoCapture import *
import time


def dual_camera_loop(websocket):

    while True:
        # calibrate only if websocket thread Event is not set
        if not websocket.CALIBRATION_DONE.is_set():
            print("calibrating...")
            print("calibrating DONE!")
            websocket.CALIBRATION_DONE.set()
            websocket.reset_image_count()

        # reset reference image
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT == 0:
            test_image_idx = 0
        websocket.Global_LOCK.release()

        if True:
            websocket.increase_image_count()


            # send result
            websocket.send_changes({"request": 1, "value": 6})
            websocket.send_counter()



        cv2.waitKey(1)
        # check if round is done and wait if true and reset reference images afterwards
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT >= 3:

            websocket.Global_LOCK.release()
            websocket.send_stillLoading("roundDone")
            websocket.ROUND_DONE.wait()

            websocket.send_stillLoading("loading")


            websocket.ROUND_DONE.clear()
        else:
            websocket.Global_LOCK.release()

        websocket.send_stillLoading("ready")

        time.sleep(10)

def test_dual_camera_loop(websocket):
    print("Strta")
    time.sleep(10)
    # load test images



    test_image_idx = 0

    # main Loop
    turns = 200
    while turns != 0:
        # calibrate only if websocket thread Event is not set
        if not websocket.CALIBRATION_DONE.is_set():
            # TODO: add new Calibration instead of loading
            websocket.CALIBRATION_DONE.set()

        # reset reference image
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT == 0:
            print("Something")
        websocket.Global_LOCK.release()

        if True:

            # send result

            websocket.send_changes({"request": 1, "value": 5})

            # increase count, replace reference image
            websocket.increase_image_count()
            websocket.send_counter()


            test_image_idx += 1

        cv2.waitKey(10)

        # check if round is done and wait if true and reset reference images afterwards
        websocket.Global_LOCK.acquire()
        if websocket.IMAGE_COUNT >= 3:
            websocket.Global_LOCK.release()
            websocket.ROUND_DONE.wait()


            test_image_idx = 0
            websocket.ROUND_DONE.clear()
        else:
            websocket.Global_LOCK.release()

        # sleep 4 sec for next calc
        time.sleep(10)