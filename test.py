import pafy
import re
from collections import deque
import cv2
import imutils
from threading import Thread
import time

def youtube_url_validator(url):
    """
    validate & retrieves Youtube video URLs ID
    """
    youtube_regex = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)
    return youtube_regex_match

class CustomVideoCapture:
    def __init__(self,source):
        self.frame = None
        # thread initialization
        self._thread = None
        # intialize termination flag
        self.terminate = False

        youtube_url = youtube_url_validator(source)
        if youtube_url:
            source_object = pafy.new(youtube_url)
            vo_source = source_object.getbestvideo("webm", ftypestrict=True)
            va_source = source_object.getbest("webm", ftypestrict=False)
            # select the best quality
            if vo_source is None or (
                    va_source.dimensions >= vo_source.dimensions
            ):
                source = va_source.url
            else:
                source = vo_source.url

            print("YouTube source ID: `{}`, Title: `{}`".format(youtube_url, source_object.title))
        else:
            raise RuntimeError(
                "`{}` Youtube URL cannot be processed!".format(source)
            )

        # youtube mode variable initialization
        self.youtube_mode = True

        # initialize threaded queue mode
        self._threaded_queue_mode = True

        self.queue = None

        # initialize deque for video files only
        if self._threaded_queue_mode and isinstance(source, str):
            self.queue = deque(maxlen=96)  # max len 96 to check overflow
            print("Enabling Threaded Queue Mode for the current video source!")

        else:
            # otherwise disable it
            _threaded_queue_mode = False
            print("Threaded Queue Mode is disabled for the current video source!")

        self.stream = cv2.VideoCapture(source)

        _fps = self.stream.get(cv2.CAP_PROP_FPS)

        # frame variable initialization
        (grabbed, frame) = self.stream.read()

        if grabbed:
            if self._threaded_queue_mode:
                # initialize and append to queue
                self.queue.append(frame)
        else:
            raise RuntimeError(
                "[CamGear:ERROR] :: Source is invalid, CamGear failed to intitialize stream on this source!"
            )

    def update(self):
        while True:
            if self.terminate:
                break
            if self._threaded_queue_mode:
                # check queue buffer for overflow
                if len(self.queue) >= 96:
                    print ("Queue is full")
                    # stop iterating if overflowing occurs
                    time.sleep(0.025)
                    continue
            # otherwise, read the next frame from the stream
            (grabbed, frame) = self.stream.read()

            # check for valid frames
            if not grabbed:
                # no frames received, then safely exit
                if self._threaded_queue_mode:
                    if len(self.queue) == 0:
                        break
                else:
                    break

            self.frame = frame

            # append to queue
            if self._threaded_queue_mode:
                self.queue.append(self.frame)

        self._threaded_queue_mode = False
        self.frame = None
        # release resources
        self.stream.release()

    def start(self):
        """ Launches the internal Threaded Frames Extractor
        **Returns:** A reference to the CamGear class object.
        """
        self._thread = Thread(target=self.update,name='CamGear',args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    def read(self):
        while self._threaded_queue_mode:
            if len(self.queue) > 0:
                return self.queue.popleft()
        return self.frame

    def stop(self):
        if self._threaded_queue_mode and not (self.queue is None):
            if len(self.queue) > 0:
                self.queue.clear()
            self._threaded_queue_mode = False
            self.frame = None

        # indicate that the thread should be terminate
        self.terminate = True

        # wait until stream resources are released (producer thread might be still grabbing frame)
        if self._thread is not None:
            self._thread.join()
            # properly handle _thread exit
            if self.youtube_mode:
                # kill _thread-lock in youtube mode
                self._thread = None


# source = 'https://www.youtube.com/watch?v=Csuk1Wm5W0E&list=RDCsuk1Wm5W0E&start_radio=1'
# source = 'https://www.youtube.com/watch?v=OzpvXl_JRXU'
# source = 'https://www.youtube.com/watch?v=5fhajnXR2rc'
source = 'https://www.youtube.com/watch?v=8C6XrNwQHjY'
stream = CustomVideoCapture(source).start()



while True:
    frame = stream.read()
    if frame is None:
        break
    frame = imutils.resize(frame, width=512)
    cv2.imshow("Output Frame", frame)

    key = cv2.waitKey(10) & 0xFF

    if key == ord("q"):
        break


# capture = cv2.VideoCapture('/home/hunglv/Videos/vlc-record-2020-08-05-02h18m21s-canhac3phut.mp4-.mp4')


# def __init__(
#         self,
#         source=0,
#         y_tube=False,
#         backend=0,
#         colorspace=None,
#         logging=False,
#         time_delay=0,
#         **options
# ):
#     from vidgear.gears import CamGear
#
#
#     stream = CamGear(source=url, y_tube=True, time_delay=1, logging=True).start()



