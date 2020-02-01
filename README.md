# face_detection
This repo is gonna contain my random notes for how to integrate face detection in a project.  My test case is some sort of device with two degrees of freedom (think a cartoon head), able to track a person.

My overall architecture is gonna be a device that has a camera, sends the pic to the "detection software", then that software gives an x/y of where in that pic the face is.  I can then feed that info back to the device, and move the servos to "center" the face in the next frame.

## Links
Here's some starting openCV links:

https://becominghuman.ai/face-detection-using-opencv-with-haar-cascade-classifiers-941dbb25177

https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/

https://www.datacamp.com/community/tutorials/face-detection-python-opencv

I'm gonna start by seeing if I can get a the algos working offline on a simple jpg.

## RPI installs
Following instructions here:
https://tutorials-raspberrypi.com/installing-opencv-on-the-raspberry-pi/

Not really happy.  Next try:

https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

Still busted.  First line of this seemed to work:
sudo apt-get install python3-opencv
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
