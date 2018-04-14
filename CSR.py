import numpy as np
import argparse
import imutils
import cv2

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		if len(approx) == 3:
			shape = "triangle"

		elif len(approx) == 4:
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)

			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		elif len(approx) == 5:
			shape = "pentagon"

		#else:
		#	shape = "circle"

		return shape

class CSR:

    def RunCSR(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
                        help="max buffer size")
        args = vars(ap.parse_args())

        #OLD RANGES
        '''lower = {'red': (166, 84, 141), 'green': (66, 122, 129), 'blue': (102, 104, 121), 'yellow': (23, 59, 119),
         'orange': (0, 50, 80)}  # assign new item lower['blue'] = (93, 10, 0)
        upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (119, 255, 255), 'yellow': (54, 255, 255),
         'orange': (20, 255, 255)}'''
        
        lower = {'red': (163, 84, 93), 'green': (66, 122, 129), 'blue': (100, 86, 8), 'yellow': (8, 133, 55),
         'orange': (0, 50, 80)}  # assign new item lower['blue'] = (93, 10, 0)
        upper = {'red': (187, 237, 255), 'green': (86, 255, 255), 'blue': (124, 237, 246), 'yellow': (33, 227, 266),
         'orange': (20, 255, 255)}

        colors = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 2, 2), 'yellow': (0, 255, 217),
         'orange': (0, 140, 255)}

        if not args.get("video", False):
            camera = cv2.VideoCapture(0)

        else:
            camera = cv2.VideoCapture(args["video"])
            
        while True:
            (grabbed, frame) = camera.read()
            if args.get("video") and not grabbed:
                break

            #frame = imutils.resize(frame, width=600)

            #convert it to grayscale, and then blur it using a Gaussian filter with a 11 x 11 kernel.
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            sd = ShapeDetector()
            
            for key, value in upper.items():
                kernel = np.ones((9, 9), np.uint8)
                mask = cv2.inRange(hsv, lower[key], upper[key])
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None


                if len(cnts) > 0:
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    shape = sd.detect(c)
                    if radius > 0.5:
                        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                        
                        if(key == "red" and shape == "triangle"): 
                                cv2.putText(frame, "A", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                                        colors["red"], 2)
                        if((key == "yellow" or key == "orange" or key == "green") and shape == "triangle"): 
                                cv2.putText(frame, "B", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                                        colors["yellow"], 2)
                        if(key == "blue" and shape == "triangle"): 
                                cv2.putText(frame, "C", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                                        colors["blue"], 2)
                        if(key == "red" and shape == "rectangle"): 
                                cv2.putText(frame, "D", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                                        colors["red"], 2)
                        if((key == "yellow" or key == "orange" or key == "green") and shape == "rectangle"): 
                                cv2.putText(frame, "E", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                                        colors["yellow"], 2)
                        if(key == "blue" and shape == "rectangle"): 
                                cv2.putText(frame, "F", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                                        colors["blue"], 2)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    NCSR = CSR()
    NCSR.RunCSR()
