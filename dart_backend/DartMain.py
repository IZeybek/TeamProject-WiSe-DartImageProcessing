import Components.OneCameraLoop as oneCamera
import Components.TwoCameraLoop as dualCamera
import Components.TwoCameraLoop_Soni as dualCamera1
import Components.TestingSkripts as test
import Components.Webserver.websocket as websocket
from Components.Calibration.VideoCapture import getVideoStream
import threading
import time

if __name__ == "__main__":
    mode = "Dual_Camera_Loop"

    # Single Camera Mode
    if mode == "Test_One_Camera_Loop":
        oneCamera.one_camera_loop(websocket)
    elif mode == "Static_Image_Test_One_Camera_Loop":
        oneCamera.test_one_camera_loop(websocket)
    elif mode == "One_Camera_Loop":
        main_loop = threading.Thread(target=oneCamera.one_camera_loop, args=(websocket,))
        main_loop.start()
        # start websocket
        websocket.start_server("localhost", 9000)

    # dual Camera Mode
    if mode == "Test_Dual_Camera_Loop":
        dualCamera.dual_camera_loop(websocket)
    elif mode == "Static_Image_Test_Dual_Camera_Loop":
        dualCamera.test_dual_camera_loop(websocket)
    elif mode == "Dual_Camera_Loop":
        main_loop = threading.Thread(target=dualCamera.dual_camera_loop, args=(websocket,))
        main_loop.start()
        # start websocket
        websocket.start_server("localhost", 9000)
    elif mode == "Dual_Camera_Loop_Soni":
        main_loop = threading.Thread(target=dualCamera1.test_dual_camera_loop, args=(websocket,))
        main_loop.start()
        # start websocket
        websocket.start_server("localhost", 9000)

    # Testing Skripts
    # Testing Skripts
    elif mode == "Calibrate-left":
        
        videoStream_L, snapshot_cam_L = getVideoStream(src=1)
        _,image = videoStream_L.read()
        test.test_calibration_Left(image.copy())
        
    elif mode == "Calibrate-right":
        
        videoStream_R, snapshot_cam_R = getVideoStream(src=0)
        _,image = videoStream_R.read()
        test.test_calibration_Right(image.copy())
        
    elif mode == "Test_Dart_Detection":
        test.test_dart_detection()
    elif mode == "Calibrate":
        test.test_calibration_both_videostreams()
    elif mode == "Calibrate2":
        test.test_calibration_both_imread("loop_specialcase_test/calibrationData_L.jpg", "loop_specialcase_test/calibrationData_R.jpg")
    elif mode == "take_snapshots":
        test.take_snapshots()
        
