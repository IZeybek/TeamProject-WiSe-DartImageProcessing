import Components.OneCameraLoop as oneCamera
import Components.TwoCameraLoop as dualCamera
import Components.TestingSkripts as test
import Components.Webserver.websocket as websocket
import threading
import time

if __name__ == "__main__":
    mode = "Static_Image_Test_One_Camera_Loop"

    # Single Camera Mode
    if mode == "Test_One_Camera_Loop":
        oneCamera.one_camera_loop(websocket)
    elif mode == "Static_Image_Test_One_Camera_Loop":
        oneCamera.test_one_camera_loop(websocket)
    elif mode == "One_Camera_Loop":
        main_loop = threading.Thread(target=oneCamera.one_camera_loop(websocket))
        main_loop.start()
        # start websocket
        websocket.start_server("localhost", 9000)

    # dual Camera Mode
    if mode == "Test_Dual_Camera_Loop":
        dualCamera.dual_camera_loop(websocket)
    elif mode == "Static_Image_Test_Dual_Camera_Loop":
        dualCamera.test_dual_camera_loop(websocket)
    elif mode == "Dual_Camera_Loop":
        main_loop = threading.Thread(target=dualCamera.dual_camera_loop(websocket))
        main_loop.start()
        # start websocket
        websocket.start_server("localhost", 9000)

    # Testing Skripts
    elif mode == "Test_Dart_Detection":
        test.test_dart_detection()
    elif mode == "Calibrate":
        test.test_calibration()
    elif mode == "take_snapshots":
        test.test_calibration()
        
