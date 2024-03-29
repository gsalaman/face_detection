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

Camera tweak:  direct import is about as long.  Going to "continous mode" stream cuts this WAAAY down:  << 1 ms.

Next issue: servo tracking.  Current loop does a PWM write, then waits, then turns it off.  The wait will delay the camera loop, so we want it to be exact.  Changing to always listen to the PWM introduces considerable jitter...I assume that's due to the Pi doing SW PWM.  Maybe try a servo hat?

# 10-17-21 OpenCV install notes
Didn't get these working, so I'm trying a new link that looks promising.  I think I'll actually have to build OpenCV.
https://www.youtube.com/watch?v=rdBTLOx0gi4

Confirm file system  is expanded  (raspi-config, advanced)
Claims not supported, as we're running NOOBS.  I'm gonna try my way through, but if I hit roadblocks, I'm gonna re-install the OS.

`sudo apt-get update && sudo apt-get upgrade`
Loads of errors....maybe my OS not supported?  Moving on just in case...

`sudo apt install snapd`
(also failed)

`sudo snapd install cmake --classic`
Can't find snapd.  Time to go back and redo the OS.  :(

(And then, I realized my pi wasn't on the network....)
Went back to first step...gave me warning that must be accepted explicitly becuase it's old stable.  
Update OS:
`sudo apt update` 
`sudo apt dist-upgrade`   <- took a WHILE!!!
`sudo apt clean`  
`sudo reboot`  

...and life looks good...back to the beginning...

Note:  still get "can't expand filesystem (NOOBS).
The initial update/upgrade didn't' do anything....duh.  Just updated.

Snapd now installs.

cmake step doesnt' work....trying a reboot...  
oh, look, it's:
`sudo snap install cmake --classic`  
(not snapd)

`sudo apt-get install python3-dev`  (already newest)

`wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip`  (note dual "opencv's" in the path...

`wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip`  

`unzip opencv.zip`

`unzip opencv_contrib.zip`

`pip install numpy`  yes, this does python 2.7...

Make a build dir...
```
cd ~/opencv-4.0.0
mkdir build
cd build
```

Compile command:
```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.0.0/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D WITH_TBB=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..
 ```
 ...and then:  
 `make -j4`
 
 If that fails, follow it up with a `make -j1`
 
 J4 worked for me.
 
 Last:
 ```
 sudo apt-get install libovencv-dev python-opencv
 ```
 
 
 



