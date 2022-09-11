import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
arucoDict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_50)
arucoParams = cv.aruco.DetectorParameters_create()

if not cap.isOpened():
    print("Cannot open camera")
    exit()

i = 0
while True:
	ret, frame = cap.read()

	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break
	# Display the resulting frame
	# gray_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	(corners, ids, rejected) = cv.aruco.detectMarkers(frame, arucoDict,parameters=arucoParams)
	
	if (i >= 100 and len(corners) > 0):
		print("type: {corners_type}".format(corners_type=type(corners[0])))
		print(" ============================== corners ==============================")
		print(corners[0])
		for rectangle in corners[0]:
			print(" ============================== rectangle ==============================")
			print(rectangle)
			#frame = cv.rectangle(frame, rectangle[0,:], rectangle[3,:], (255,0,0), 2)
		i = 0
	else:
		i += 1
	
	if len(corners) > 0:
		for rectangle in corners[0]:
			frame = cv.line(frame, rectangle[0,:].astype(int), rectangle[1,:].astype(int) , (255,0,0), 2)
			frame = cv.line(frame, rectangle[1,:].astype(int), rectangle[2,:].astype(int) , (255,0,0), 2)
			frame = cv.line(frame, rectangle[2,:].astype(int), rectangle[3,:].astype(int) , (255,0,0), 2)
			frame = cv.line(frame, rectangle[3,:].astype(int), rectangle[0,:].astype(int) , (255,0,0), 2)
	
	cv.imshow('original frame', frame)
	
	if cv.waitKey(1) == ord('q'):
		break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


#if __name__ == "__main__":
#    aruco_detection()