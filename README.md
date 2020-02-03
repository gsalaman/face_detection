# face_detection
This repo is gonna contain my random notes for how to integrate face detection in a project.  My test case is some sort of device with two degrees of freedom (think a cartoon head), able to track a person.

My overall architecture is gonna be a device that has a camera, sends the pic to the "detection software", then that software gives an x/y of where in that pic the face is.  I can then feed that info back to the device, and move the servos to "center" the face in the next frame.

## Links
Here's some starting openCV links:

https://becominghuman.ai/face-detection-using-opencv-with-haar-cascade-classifiers-941dbb25177

https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/

https://www.datacamp.com/community/tutorials/face-detection-python-opencv

https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/

I'm gonna start by seeing if I can get a the algos working offline on a simple jpg.

## RPI installs
Following instructions here:
https://tutorials-raspberrypi.com/installing-opencv-on-the-raspberry-pi/

Not really happy.  Next try:

https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

Still busted.  First line of this seemed to work:
```
sudo apt-get install python3-opencv
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
```
Yup...now I'm happy.  Next steps:
* try this with a real Pi Camera rather than off the shel images.  Tweak image sizes, detection critera, and check speeds.  Does this need to go offline?
* Do a pan framework for a servo (3d print)
* Control said servo with the Pi
* Combine tracker and pan

## Camera:
picamera looks to already be installed.
need to enable via sudo raspi-config

# DNN:
also needed sudo pip3 install opencv-contrib-python...but that broke everything.
Did the uninstall...back to normal.

HOWEVER....the apt-get version does 3.2, but I need at least 3.3.  Doing a pip3 install got me to 4.x, but then I needed other libararies.  Did the jasper-dev, libqtgui4, libqt4-test...still issues.  Back to the 3.2 version and haar for now.

# Feb 3 notes
Pan-only tracker online in track.py.

Does very rough servo tracking, but has 2 issues:
* Camera field of view a little too narrow.  Maybe implement "search" mode?
* Latency is WAAAAY too great...sometimes order of 1s per update.  Checking individual steps:
  * Snapping the pic takes 1/2 second.  First low-hanging fruit...import directly?
  * Import takes 50 ms.  Fine.
  * Detection is 300 ms...a little long.  After we get the direct import, we can chase this...first try deep learning, then try offline?
