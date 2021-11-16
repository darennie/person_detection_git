#!/usr/bin/env python3
import blobconverter
import cv2
import depthai as dai
import argparse
import itertools
import datetime
import csv
import os

from depthai_sdk import PipelineManager, NNetManager, PreviewManager
from depthai_sdk import cropToAspectRatio

#=====================================================================================
# To use a different NN, change `size` and `nnPath` here:
size = (544, 320)
nnPath = blobconverter.from_zoo("person-detection-retail-0013", shaves=6)
#=====================================================================================

# Labels
labelMap = ["background", "person"]

# define the current max people count (we want max count over the minute)
current_max_count = 0

# get the starting value of current minute - in the loop below we check to see if the value has changed
current_minute = datetime.datetime.now().strftime("%M")
        
# filename for each loggin session based on start time - csv file
filename = 'detection-' +str(datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")+'.csv')

# this function writes it a new csv
# each row appended has 2 values - an ISO 8601 timestamp plus an integer people count
def write_to_csv():
    # the a is for append, if w for write is used then it overwrites the file
    with open(filename, mode='a') as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([datetime.datetime.now().isoformat(), current_max_count])
        return(write_to_log)

# DepthAI Code - Get arguments - have stripped down to just camera input
parser = argparse.ArgumentParser()
parser.add_argument('-cam', '--camera', action="store_true", help="Use DepthAI RGB camera for inference (conflicts with -vid)")
args = parser.parse_args()

# rgb camera source
nnSource = "color"

# Start defining a pipeline
pm = PipelineManager()
pm.createColorCam(previewSize=size, xout=True)
pv = PreviewManager(display=["color"], nnSource=nnSource)
nm = NNetManager(inputSize=size, nnFamily="mobilenet", labels=labelMap, confidence=0.5)
nn = nm.createNN(pm.pipeline, pm.nodes, blobPath=nnPath, source=nnSource)
pm.setNnManager(nm)
pm.addNn(nn)


# Main loop starts by setting up pipeline and connecting device
with dai.Device(pm.pipeline) as device:
    nm.createQueues(device)
    pv.createQueues(device)

    # depending on framerate on device a count will be calculated per frame
    # we render this in preview window with bounding box and count
    # we compare the current count to max count and if the current minute
    # has changed we write the current max count value to file
    while True:
        
        #pv.prepareFrames(blocking=True)
        #frame = pv.get("color")
        nn_data = nm.decode(nm.outputQueue.get())
        #nm.draw(frame, nn_data)
        #cv2.putText(frame, f"People count: {len(nn_data)}", (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,255))
        #cv2.imshow("color", frame)

        # count the people
        pcount = len(nn_data)
        if pcount > current_max_count:
            current_max_count = pcount

        if datetime.datetime.now().strftime("%M") != current_minute:
            write_to_csv()
            print(str(datetime.datetime.now().isoformat()) + " --- " + str(current_max_count))
            current_max_count = 0
            current_minute = datetime.datetime.now().strftime("%M")

        if cv2.waitKey(1) == ord('q'): 
            break