#  First cut camera face-detect tracking.
#  Multi-detect algos

import cv2
import sys
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from datetime import datetime


# camera setup
camera = PiCamera()
camera_x=640
camera_y=480
camera.resolution = (camera_x, camera_y)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(.1)  # camera warmup time

# using Haar for face detection
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


# Servo setup...this will be susceptable to SW latency on the PWM 
# causing jitter.  Eventually go to a dedicated HW board.
servo_pin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
pwm=GPIO.PWM(servo_pin, 50)
pwm.start(0)


# Code to set Servo angle  
# Current algo moves, then waits, then turns it off
# could just keep the PWM stream on, but that is jittery
def setAngle(angle, servo_pin, wait):
  duty = angle/18 + 2
  GPIO.output(servo_pin, True)
  pwm.ChangeDutyCycle(duty)
  time.sleep(wait)
  GPIO.output(servo_pin, False)
  pwm.ChangeDutyCycle(0)

##############
# MAIN
##############

# start with camera at the middle of the servo position
current_x = 90
setAngle(current_x, servo_pin, 1)

try:
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start_time = datetime.now()

    print("snapping pic")
    image = frame.array
    
    # latency instrumentation...
    snap_time = datetime.now()
    deltaT = snap_time - start_time
    print(deltaT.total_seconds())
    

    print("importing pic")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
    # latency instrumentation...
    snap_time = datetime.now()
    import_time = datetime.now()
    deltaT = import_time - snap_time
    print(deltaT.total_seconds())

    # do the actual face detect.
    # Param notes:  
    #   increase minNeighbors for fewer false alarms but higher detect threshold
    #   minSize is the smallest (pixel) bounding box it'll detect.
    #   scaleFactor tells what "zoom levels" to look through...1.05 will give
    #      more detects but longer time...1.4 will be fewer detects but shorter
    #      time.
    print("detecting faces")
    faces = faceCascade.detectMultiScale(
      gray,
      scaleFactor=1.1,
      minNeighbors=10,
      minSize=(30,30),
      flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Detected {0} faces!".format(len(faces)))
   
    # more latency instrumentation....
    detect_time = datetime.now()
    deltaT = detect_time - import_time
    print(deltaT.total_seconds())


    # first iteration:  draw rectangles around all, but only track first face
    for (x, y, w, h) in faces:
      center = (x+w/2,y+h/2)
      print(center)

      cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

      # if we're more than move_threshold pixels away from the center, then 
      # move the servo by a small amount.
      move_threshold = 20
      if (center[0] + move_threshold < camera_x / 2):
        if (current_x > 10):
          current_x = current_x - 2 
          setAngle(current_x, servo_pin, .05)
          print("move ---")
      elif (center[0] - move_threshold > camera_x / 2):
        if (current_x < 170):
          current_x = current_x + 2
          setAngle(current_x, servo_pin, .05)
          print("move +++")

    # bring up a window showing all the detected faces
    cv2.imshow("Faces Detected", image)
 
    # latency instrumentation
    end_time = datetime.now()
    deltaT = end_time - start_time
    print(deltaT.total_seconds())

    # needed to keep the window open.  50 means wait 50ms for a keystroke, 
    # then go on.
    cv2.waitKey(50)

    # clear our buffer for the next pass through.
    rawCapture.truncate(0)
    

except KeyboardInterrupt:
   rawCapture.truncate(0)
