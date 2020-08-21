# pip install vidgear

import cv2
import imutils

from vidgear.gears import CamGear
url = 'https://www.youtube.com/watch?v=Csuk1Wm5W0E&list=RDCsuk1Wm5W0E&start_radio=1'
stream=CamGear(source=url, y_tube =True, time_delay=1, logging=True).start()

# validate
print(stream.framerate)


while True:
	frame = stream.read()
	if frame is None:
		break
	frame = imutils.resize(frame,width=512)
	cv2.imshow("Output Frame",frame)

	key = cv2.waitKey(10) & 0xFF

	if key == ord("q"):
		break