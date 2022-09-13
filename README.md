# -aruco_detector
Package created to detect arUco markers on video frames using opencv python.

The package contains two files the file called 'aruco_detector.py' only detects the corners of the 
aruco markers and draws a blue border over each arUco code that is detected, the second file called
'aruco_detector position.py' aditionaly saves and processes the data of the arUcos detected, in such
way that the logic within this file is able to detect all the arUco markers existent on a scene, 
give the position in meters of the center point of each arUco marker (x,y,z) considering as reference
axis an axis that has its origin on the center of the camera that is being used, and to   
