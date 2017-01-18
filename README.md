![Computer Music At the 2016 DAE](https://i1.wp.com/bitdeph.com/wp-content/uploads/2016/03/Computer-music-at-the-Expo.jpg)

Setup will be as follows

IAC MIDI BUS SHOUDLD BE CREATED ON MAC

CHANNELS 1-8 ARE THE FLOPPY DRIVES ON THE FIRST BUS
- pitched around C0-A3
- taken care of via an instance of MOPPY running on computer
- two arduino UNO's connected to mac VIA USB

CHANNELS 9-12 ARE THE CDROM DRIVES ON THE FIRST BUS
- midi notes split around 64 moving motor one way or another
- taken care of via python
- one arduino MEGA takes care of these 

CHANNELS 13-16 ARE THE CDROM DRIVE TREYS ON THE FIRST BUS
- any message sent will trigger the tray

CHANNELS 1-4 ARE THE STEPPERS ON THE SECOND BUS
- midi notes split around 64 moving the motor one way or another
- taken care of via python
- one arduino MEGA takes care of these 

PREREQUISITES:

sudo apt-get install python-dev libxml2-dev libxslt-dev
sudo apt-get install libasound2-dev
easy_install rtmidi-python
sudo apt-get install jack-tools ant openjdk-7-jdk fftw3 qjackctl
rtmidi python binding - pip install rtmidi-python
sudo pip install git-python
sudo pip install jira
