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

def midpoint_equation(p1, p2):
    return ( (p1[0]+p2[0])/2, (p1[1]+p2[1])/2 )

def get_aruco_midpoint(rectangle_corners):
    result = midpoint_equation(rectangle_corners[0,:], rectangle_corners[2,:])
    return (int(result[0]), int(result[1]))

def get_aruco_position(aruco_area, aruco_center):
    k1, k2 = 30000, 0
    k3, k4 = 1/250, -308
    k5, k6 = 1/250, -259
    z = k1*(1/aruco_area) + k2
    x = k3*(aruco_center[0] + k4)*z
    y = k5*(aruco_center[1] + k6)*z
    return (x, y, z)

def get_aruco_area(rectangle_corners):
    a = np.linalg.norm(rectangle_corners[0,:] - rectangle_corners[1,:])
    b = np.linalg.norm(rectangle_corners[1,:] - rectangle_corners[2,:])
    c = np.linalg.norm(rectangle_corners[2,:] - rectangle_corners[3,:])
    d = np.linalg.norm(rectangle_corners[3,:] - rectangle_corners[1,:])
    crossed_side = np.linalg.norm(rectangle_corners[0,:] - rectangle_corners[2,:])
    alpha = np.arccos( (crossed_side**2-a**2-b**2)/(-2*a*b) )
    gamma = np.arccos( (crossed_side**2-c**2-d**2)/(-2*c*d) )
    semiperimeter = (a + b + c + d) / 2
    return ( (semiperimeter-a)*(semiperimeter-b)*(semiperimeter-c)*(semiperimeter-d) - 
        (a*b*c*d)*(np.cos((alpha+gamma)/2)**2) )**(0.5)

def detect_all_arucos_in_scene(scene, scene_with_hidden_arucos, arucoDict, params, result_dict):
    (corners, ids, rejected) = cv.aruco.detectMarkers(scene_with_hidden_arucos, arucoDict,parameters=params)
    if len(corners) > 0:
        for rectangle in corners[0]:
            scene = draw_rectangle(scene, rectangle)
            (min_x, max_x, min_y, max_y) = get_rectangle_max_and_mins(rectangle)
            white_rect = np.ones((max_y-min_y, max_x-min_x), dtype=np.uint8)*255
            white_rect = cv.cvtColor(white_rect, cv.COLOR_GRAY2BGR) 
            scene_with_hidden_arucos[min_y:max_y, min_x:max_x] = white_rect
            aruco_center = get_aruco_midpoint(rectangle)
            scene = cv.circle(scene, aruco_center, radius=2, color=(0,0,255), thickness=2)
            aruco_area = get_aruco_area(rectangle)
            aruco_position = get_aruco_position(aruco_area, aruco_center)
            scene = cv.putText( 
                scene, 
                "x:{x:.2f} y:{y:.2f} z:{z:.2f}".format(x=aruco_position[0], y=aruco_position[1], z=aruco_position[2]), 
                aruco_center, 
                fontFace = cv.FONT_HERSHEY_SIMPLEX, 
                fontScale = 0.5, 
                color=(0,0,255), 
                thickness = 2 )
            result_dict["aruco_centers"].append( aruco_center )
            result_dict["aruco_corners"].append( rectangle.tolist() )
            result_dict["aruco_areas"].append( aruco_area )  
            result_dict["aruco_positions"].append( aruco_position ) 
        return detect_all_arucos_in_scene(scene, scene_with_hidden_arucos, arucoDict, params, result_dict)
    else:
        result_dict["scene"] = scene
        return result_dict

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
        
        aruco_detection_res = detect_all_arucos_in_scene(frame, frame.copy(), arucoDict, arucoParams, {"scene":None, "aruco_centers": [], "aruco_corners": [], "aruco_areas":[], "aruco_positions":[] })
        frame = aruco_detection_res["scene"]
        aruco_positions = aruco_detection_res["aruco_positions"]
        if len(aruco_positions) > 0:
            aruco_psoitions_sorted = sorted(aruco_positions, key=lambda x:x[2])
            closest_aruco_position = aruco_psoitions_sorted[0]
            closest_aruco_index = aruco_positions.index(closest_aruco_position)
            closest_aruco_second_corner = aruco_detection_res["aruco_corners"][closest_aruco_index][1]
            closest_aruco_second_corner_cords = (int(closest_aruco_second_corner[0]), int(closest_aruco_second_corner[1]))
            frame = cv.putText( 
                    frame, 
                    "closest",
                    closest_aruco_second_corner_cords, 
                    fontFace = cv.FONT_HERSHEY_SIMPLEX, 
                    fontScale = 0.5, 
                    color=(255,0,0), 
                    thickness = 2 )
            if closest_aruco_position[0] == 0:
                print("don't move")
            elif closest_aruco_position[0] > 0:
                print("izquierda")
            else:
                print("derecha")
        cv.imshow('resulting frame', frame)
        
        if cv.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    aruco_detection()