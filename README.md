# AECPCR Person counter

Notes on setting up person counter using DepthAI Oak 1 camera

## Setup DepthAI

This Python script requires the DepthAI repo installed on host machine. Install instructions are [in the DepthAI Docs](https://docs.luxonis.com/en/latest/), basic instructions are:

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


## Running the script

The script take one argument as input "-cam" to select the Oak1 as input stream.

```terminal
python3 main.py -cam
```

