import cv2
import numpy

frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert video frame to grayscale

kernel = np.ones((1,1),np.uint8)
closing = cv2.morphologyEx(frame_grey, cv2.MORPH_CLOSE, kernel)
thresh = threshold_adaptive(closing, 251, offset = 35) #add thresholding
thresh = thresh.astype("uint8") * 255

if cv2.Laplacian(frame, cv2.CV_64F).var() > 350: #if frame is not blurry
    frame_copy = frame.copy() #copy not blurred frame
    text = Image.fromarray(frame_copy)
    text = pytesseract.image_to_string(text, config='-psm 6 -c tessedit_char_whitelist=12345678ABCDEFGHIJKLMNOPQRSTUVWXYZ load_system_dawg=false load_freq_dawg=false') #extract text
