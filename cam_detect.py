import cv2
import sys
from picamera import PiCamera
import time
from datetime import datetime

camera = PiCamera()
camera.resolution = (640,480)

imagePath = "temp.jpg" 
cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

try:
  while True:
    start_time = datetime.now()

    print("snapping pic")
    camera.capture(imagePath)

    print("importing pic")
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("detecting faces")
    faces = faceCascade.detectMultiScale(
      gray,
      scaleFactor=1.1,
      minNeighbors=3,
      minSize=(30,30),
      flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Detected {0} faces!".format(len(faces)))


    for (x, y, w, h) in faces:
      cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces Detected", image)
 
    end_time = datetime.now()
    deltaT = end_time - start_time
    print(deltaT.total_seconds())

    cv2.waitKey(50)

    
    

except KeyboardInterrupt:
   pass
