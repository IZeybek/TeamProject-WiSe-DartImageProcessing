# import the necessary packages
from threading import Thread
import cv2
import time

class VideoStream:
    """create new VideoStream Thread with helper functions.
 
        Paramter
        -------
        src: int
            cam index. 
            
        Attributes
        ----------
        grabbed : bool
            cam is grabbed successfull?.
        frame : np.array
            Description of `attr1`.
        stream : cv2.VideoCapture
            stream of videoCapture.
        stopped : bool
            true if thread should be terminated.

        """
    def __init__(self, src=0):
        
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.fps = self.stream.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(self.fps))
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        """start the thread to read frames from the video stream.
 
        Returns
        -------
        VideoStream
            self returns its own object.
        """
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """keep looping infinitely until the thread is stopped.
 
        Returns
        -------
        VideoStream
            self returns its own object.
        """
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            #self.debug_fps()

            (self.grabbed, self.frame) = self.stream.read()

    def debug_fps(self):
        # otherwise, read the next frame from the stream
        num_frames = 30;
        # Grab a few frames
        
        print("Capturing {0} frames".format(num_frames))

        # Start time

        start = time.time()

        # Grab a few frames

        for i in range(0, num_frames) :

            ret, frame = self.stream.read()

        # End time

        end = time.time()

        # Time elapsed

        seconds = end - start

        print ("Time taken : {0} seconds".format(seconds))

        # Calculate frames per second

        fps  = num_frames / seconds

        print("Estimated frames per second : {0}".format(fps))
    
    
    def initRead(self):
        
        time.sleep(4)
        return self.grabbed, self.frame

    def read(self):
        """return the frame most recently read.
 
        Returns
        -------
        boolean
            grabbed returns true if cam is grabbed.
        array    
            frame returns videoFrame as an array.
        """
        time.sleep(3/self.fps)
        # return the frame most recently read
        return self.grabbed, self.frame

    def stop(self):
        """indicate that the thread should be stopped.
        """
        # indicate that the thread should be stopped
        self.stopped = True
        
def getVideoStream(src=0):
    try:

        videoStream = VideoStream(src).start()
        _, camRGB = videoStream.initRead()
        snapshot_cam = camRGB.copy()

    except:
        print("Could not init camaras")
        return None

    return videoStream, snapshot_cam