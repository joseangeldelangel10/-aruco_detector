import numpy as np
import cv2 as cv

def draw_rectangle(image,rectangle_corners):
	image = cv.line(image, rectangle_corners[0,:].astype(int), rectangle_corners[1,:].astype(int) , (255,0,0), 2)
	image = cv.line(image, rectangle_corners[1,:].astype(int), rectangle_corners[2,:].astype(int) , (255,0,0), 2)
	image = cv.line(image, rectangle_corners[2,:].astype(int), rectangle_corners[3,:].astype(int) , (255,0,0), 2)
	image = cv.line(image, rectangle_corners[3,:].astype(int), rectangle_corners[0,:].astype(int) , (255,0,0), 2)
	return image

def get_rectangle_max_and_mins(rectangle_corners):
	x_vals = rectangle_corners[:,0]
	y_vals = rectangle_corners[:,1]
	return map(int, (min(x_vals), max(x_vals), min(y_vals), max(y_vals)) )

def detect_all_arucos_in_scene(scene, scene_with_hidden_arucos, arucoDict, params):
	(corners, ids, rejected) = cv.aruco.detectMarkers(scene_with_hidden_arucos, arucoDict,parameters=params)
	if len(corners) > 0:
		for rectangle in corners[0]:
			scene = draw_rectangle(scene, rectangle)
			(min_x, max_x, min_y, max_y) = get_rectangle_max_and_mins(rectangle)
			white_rect = np.ones((max_y-min_y, max_x-min_x), dtype=np.uint8)*255
			white_rect = cv.cvtColor(white_rect, cv.COLOR_GRAY2BGR) 
			scene_with_hidden_arucos[min_y:max_y, min_x:max_x] = white_rect
		return detect_all_arucos_in_scene(scene, scene_with_hidden_arucos, arucoDict, params)
	else:
		return scene

def aruco_detection():
	cap = cv.VideoCapture(0)
	arucoDict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_50)
	arucoParams = cv.aruco.DetectorParameters_create()

	if not cap.isOpened():
		print("Cannot open camera")
		exit()

	while True:
		ret, frame = cap.read()

		if not ret:
			print("Can't receive frame (stream end?). Exiting ...")
			break
		
		frame = detect_all_arucos_in_scene(frame, frame.copy(), arucoDict, arucoParams)
		cv.imshow('resulting frame', frame)
		
		if cv.waitKey(1) == ord('q'):
			break
			
	cap.release()
	cv.destroyAllWindows()


if __name__ == "__main__":
    aruco_detection()