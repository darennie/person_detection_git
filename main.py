#!/usr/bin/env python3
from pathlib import Path

import blobconverter
import cv2
import depthai as dai
import numpy as np
import argparse
from time import monotonic
import itertools
import time, sched
import datetime
import logging
import csv
import io
import os

from depthai_sdk import PipelineManager, NNetManager, PreviewManager
from depthai_sdk import cropToAspectRatio

parentDir = Path(__file__).parent

#=====================================================================================
# To use a different NN, change `size` and `nnPath` here:
size = (544, 320)
nnPath = blobconverter.from_zoo("person-detection-retail-0013", shaves=6)
#=====================================================================================

# Labels
labelMap = ["background", "person"]

# Time Section

#prints actual time
starttime_actual = datetime.datetime.now()
#print(starttime_actual)

#prints time in unix
starttime_unix = time.time()
#print(starttime_unix)

# starting the count
maxcount = 0

# Check current working directory.
#retval = os.getcwd()
#print("Current working directory %s" % retval)


#change as needed to get the right directory (I know there is a more elegant way to do this but I can't remember!)
filename = 'detection-' +str(datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")+'.csv')
#os.chdir('/Users/danielrennie/Dropbox/My Mac (Daniel’s MacBook Air)/Documents/CASA/UCL/AECPCR/person_detection')


# function to count the people
def person_count():
    pcount = len(nn_data)
    pcount = str(len(nn_data))
    return(pcount)


# function to get today's date
def date_now():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today = str(today)
    return(today)


#funtion to get the time in hours and minutes (I decided that seconds weren't worth it to get the maximum value per minute)
def time_now():
    now = datetime.datetime.now().strftime("%H:%M")
    now = str(now)
    return(now)


# this fucntion writes it a new csv
def write_to_csv():
    # the a is for append, if w for write is used then it overwrites the file
    with open(filename, mode='a') as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([date_now(), time_now(), person_count()])
        return(write_to_log)


#the next part is all code from DepthAi

# Get argument first
parser = argparse.ArgumentParser()
parser.add_argument('-nn', '--nn', type=str, help=".blob path")
parser.add_argument('-i', '--image', type=str,
                    help="Path to an image file to be used for inference (conflicts with -cam)")
parser.add_argument('-cam', '--camera', action="store_true",
                    help="Use DepthAI RGB camera for inference (conflicts with -vid)")
args = parser.parse_args()

# Whether we want to use images from host or rgb camera
IMAGE = not args.camera
nnSource = "host" if IMAGE else "color"

# Start defining a pipeline
pm = PipelineManager()
if not IMAGE:
    pm.createColorCam(previewSize=size, xout=True)
    pv = PreviewManager(display=["color"], nnSource=nnSource)

nm = NNetManager(inputSize=size, nnFamily="mobilenet", labels=labelMap, confidence=0.5)
nn = nm.createNN(pm.pipeline, pm.nodes, blobPath=nnPath, source=nnSource)
pm.setNnManager(nm)
pm.addNn(nn)


#this gets the new file to write to

with open(filename, "a") as log:

    # Back to DepthAI code
    # Pipeline defined, now the device is connected to
    with dai.Device(pm.pipeline) as device:
        nm.createQueues(device)
        if IMAGE:
            imgPaths = [args.image] if args.image else list(parentDir.glob('images/*.jpeg'))
            og_frames = itertools.cycle([cropToAspectRatio(cv2.imread(str(imgPath)), size) for imgPath in imgPaths])
        else:
            pv.createQueues(device)

        while True:
            if IMAGE:
                frame = next(og_frames).copy()
                nm.sendInputFrame(frame)
            else:
                pv.prepareFrames(blocking=True)
                frame = pv.get("color")

            nn_data = nm.decode(nm.outputQueue.get())
            nm.draw(frame, nn_data)
            cv2.putText(frame, f"People count: {len(nn_data)}", (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,255))
            cv2.imshow("color", frame)

            #this calls the function that we created earlier
            write_to_csv()

            if cv2.waitKey(3000 if IMAGE else 1) == ord('q'): 
                break