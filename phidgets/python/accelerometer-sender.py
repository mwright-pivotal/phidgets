#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""
from logging import INFO

__author__ = 'Adam Stelmack'
__revised__= 'Mike Wright'
__version__ = '2.2.0'
__date__ = 'Jan 5, 2015'

#Basic imports
from ctypes import *
import sys
import datetime
import time, logging
import simplejson as json
from flask import jsonify
#Phidget specific imports
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan
from Phidgets.Devices.GPS import GPS
import urllib, httplib2

accleration_url = 'http://accelerometer-synapse.south.fe.pivotal.io/api/acceleration'
angular_url = 'http://accelerometer-synapse.south.fe.pivotal.io/api/angular'
magnetic_url = 'http://accelerometer-synapse.south.fe.pivotal.io/api/magnetic'

h = httplib2.Http(".cache") # WAT?
h.add_credentials("user", "******", "http://accelerometer-synapse.south.fe.pivotal.io")
FORMAT = '%(asctime)-15s %(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('spatial-sender')
logger.setLevel(INFO)

#Create an accelerometer object
try:
    spatial = Spatial()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def DisplayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (spatial.isAttached(), spatial.getDeviceName(), spatial.getSerialNum(), spatial.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Acceleration Axes: %i" % (spatial.getAccelerationAxisCount()))
    print("Number of Gyro Axes: %i" % (spatial.getGyroAxisCount()))
    print("Number of Compass Axes: %i" % (spatial.getCompassAxisCount()))

#Event Handler Callback Functions
def SpatialAttached(e):
    attached = e.device
    attached.setDataRate(100)
    print("Spatial %i Attached!" % (attached.getSerialNum()))

def SpatialDetached(e):
    detached = e.device
    print("Spatial %i Detached!" % (detached.getSerialNum()))

def SpatialError(e):
    try:
        source = e.device
        print("Spatial %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def SpatialData(e):
    source = e.device
    serialnum = source.getSerialNum()
    print("Spatial %i: Amount of data %i" % (source.getSerialNum(), len(e.spatialData)))
    for index, spatialData in enumerate(e.spatialData):
        print("=== Data Set: %i ===" % (index))
        if len(spatialData.Acceleration) > 0:
            data = {'type' : 'accel', 'device' : str(serialnum), 'rcvts' : str(datetime.datetime.now()), 'x' : str(spatialData.Acceleration[0]), 'y' : str(spatialData.Acceleration[1]), 'z' : str(spatialData.Acceleration[2])}
            obj = json.dumps(data)
            resp, content = h.request(uri=accleration_url + "/" + str(serialnum), method='POST', headers={'Content-Type': 'application/json; charset=UTF-8'}, body=obj)
        if len(spatialData.AngularRate) > 0:
            data = {'type' : 'angular', 'device' : str(serialnum), 'rcvts' : str(datetime.datetime.now()), 'x' : str(spatialData.AngularRate[0]) , 'y' : str(spatialData.AngularRate[1]), 'z' : str(spatialData.AngularRate[2])}
            obj = json.dumps(data)
            resp, content = h.request(uri=angular_url + "/" + str(serialnum), method='POST', headers={'Content-Type': 'application/json; charset=UTF-8'}, body=obj)
        if len(spatialData.MagneticField) > 0:
            data = {'type' : 'magnetic', 'device' : str(serialnum), 'rcvts' : str(datetime.datetime.now()), 'x' : str(spatialData.MagneticField[0]) , 'y' : str(spatialData.MagneticField[1]), 'z' : str(spatialData.MagneticField[2])}
            obj = json.dumps(data)
            resp, content = h.request(uri=magnetic_url + "/" + str(serialnum), method='POST', headers={'Content-Type': 'application/json; charset=UTF-8'}, body=obj)

#Main Program Code
try:
    spatial.setOnAttachHandler(SpatialAttached)
    spatial.setOnDetachHandler(SpatialDetached)
    spatial.setOnErrorhandler(SpatialError)
    spatial.setOnSpatialDataHandler(SpatialData)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)
    
print("Opening phidget object....")

try:
    spatial.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    print("Waiting for accelerometer attach....")
    spatial.waitForAttach(10000)
    print("accelerometer attached....")
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        spatial.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        #raise SystemExit(1)
        exit(1)
else:
    spatial.setDataRate(1000)
    DisplayDeviceInfo()

while True:
    time.sleep(10)

print("Closing...")

try:
    spatial.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
