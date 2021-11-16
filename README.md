# AECPCR Person counter

Notes on setting up person counter using DepthAI Oak 1 camera

![Oak 1 Camera](https://cdn.shopify.com/s/files/1/0106/8325/2802/products/OAK-1_1600x.jpg?v=1627660345)

[Oak 1 product website](https://shop.luxonis.com/products/megaai-kit)

## Setup DepthAI

This Python script requires the DepthAI repo installed on host machine. Install instructions are [in the DepthAI Docs](https://docs.luxonis.com/en/latest/pages/tutorials/first_steps/#first-steps-with-depthai) and OS specific instrutions are [here](https://docs.luxonis.com/projects/api/en/latest/install/), basic instructions are:

```terminal 
git clone https://github.com/luxonis/depthai.git
cd depthai
python3 install_requirements.py
```

To check setup is working before running AECPCR code run the default demo:

```terminal 
python3 depthai_demo.py
```

## Dependencies used in project:

The [Hello World](https://docs.luxonis.com/projects/api/en/latest/tutorials/hello_world/) example on the DepthAI docs is always a good place to start if you are using this device for first time and wanting to check you have the dependcies you need


## Running scripts in this folder

The script take one argument as input "-cam" to select the Oak1 as input stream. Main.py records count every frame to csv file.

```terminal
python3 main.py -cam
```

Oak1 version writes to csv once every minute and records the max number of people counted in a scene over that minute

```terminal
python3 oak1_counter.py -cam
```

## Notes for restart.py

This restarts the script whenever it drops off as there is intermittent drop off as the program is running occassionally. This ensures that the script run continuously throughout the desired timeframe.

## Notes for running on RPi

To run on RPi follow same process to install DepthAI but also make sure OpenCV is installed:

```terminal 
sudo apt-get update && sudo apt-get upgrade
sudo apt install git python3-pip python3-opencv libcurl4 libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test
```

To run on boot of a RPi you must enter the following first into terminal:

```terminal 
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
Once there add the following line of code to the bottom of the existing text to run the restart.py script:

```terminal 
@python3 /home/pi/person_detection/restart.py
```
Follow the instructions within the terminal to save and exit as appropriate. Once this is complete the restart.py will run on the reboot of the RPi. Please note that the path to the file must be adjusted to suit the user's directory.
