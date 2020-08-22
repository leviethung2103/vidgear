# pip install vidgear
# python main.py 

import cv2
import imutils

from vidgear.gears import CamGear
url = 'https://www.youtube.com/watch?v=5fhajnXR2rc'
stream=CamGear(source=url, y_tube =True, time_delay=1, logging=True).start()

# validate
print("[INFO] Frame rate: ",stream.framerate)


while True:
	frame = stream.read()
	if frame is None:
		break
	frame = imutils.resize(frame,width=720)
	cv2.imshow("Output Frame",frame)

	key = cv2.waitKey(10) & 0xFF

	if key == ord("q"):
		break