import cv2
import sys
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
from datetime import datetime

camera = PiCamera()
camera_x=640
camera_y=480
camera.resolution = (camera_x, camera_y)

imagePath = "temp.jpg" 
cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

servo_pin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
pwm=GPIO.PWM(servo_pin, 50)
pwm.start(0)

def setAngle(angle, servo_pin):
  duty = angle/18 + 2
  GPIO.output(servo_pin, True)
  pwm.ChangeDutyCycle(duty)
  time.sleep(.05)
  GPIO.output(servo_pin, False)
  pwm.ChangeDutyCycle(0)

current_x = 90
setAngle(current_x, servo_pin)

try:
  while True:
    start_time = datetime.now()

    print("snapping pic")
    camera.capture(imagePath)
    
    snap_time = datetime.now()
    deltaT = snap_time - start_time
    print(deltaT.total_seconds())
    

    print("importing pic")
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
    import_time = datetime.now()
    deltaT = import_time - snap_time
    print(deltaT.total_seconds())

    print("detecting faces")
    faces = faceCascade.detectMultiScale(
      gray,
      scaleFactor=1.1,
      minNeighbors=10,
      minSize=(30,30),
      flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Detected {0} faces!".format(len(faces)))
    detect_time = datetime.now()
    deltaT = detect_time - import_time
    print(deltaT.total_seconds())


    # first iteration:  only track first face

    for (x, y, w, h) in faces:
      center = (x+w/2,y+h/2)
      print(center)

      cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

      move_threshold = 20
      if (center[0] + move_threshold < camera_x / 2):
        if (current_x > 10):
          current_x = current_x - 5
          setAngle(current_x, servo_pin)
          print("move ---")
      elif (center[0] - move_threshold > camera_x / 2):
        if (current_x < 170):
          current_x = current_x + 5
          setAngle(current_x, servo_pin)
          print("move +++")

    cv2.imshow("Faces Detected", image)
 
    end_time = datetime.now()
    deltaT = end_time - start_time
    print(deltaT.total_seconds())

    cv2.waitKey(50)

    
    

except KeyboardInterrupt:
   pass
