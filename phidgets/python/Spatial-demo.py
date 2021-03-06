#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__revised__= 'Mike Wright'
__version__ = '2.2.0'
__date__ = 'Jan 5, 2015'

#Basic imports
from ctypes import *
import sys
import datetime
import time
import simplejson
#Phidget specific imports
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan
from Phidgets.Devices.GPS import GPS
import urllib, httplib2

springxd_url = 'http://phidgets.mikepwright.dyndns.ws:8080'

h = httplib2.Http(".cache") # WAT?
h.add_credentials("user", "******", "http://192.168.0.108:9020")

#Create an accelerometer object
try:
    spatial = Spatial()
    gps = GPS()
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
    	    #data = "{serialnum : \"" + str(source.getSerialNum()) + "\", rcvts : \"" + str(datetime.datetime.now()) + "\", acceleration:{ x : \"" + str(spatialData.Acceleration[0]) + "\" , y : \"" + str(spatialData.Acceleration[1]) +"\" , z : \"" + str(spatialData.Acceleration[2]) + "\"} }"
    	    data = "accel," + str(serialnum) + "," + str(datetime.datetime.now()) + "," + str(spatialData.Acceleration[0]) + "," + str(spatialData.Acceleration[1]) +"," + str(spatialData.Acceleration[2])
    	    resp, content = h.request(springxd_url, 'POST', data)
        if len(spatialData.AngularRate) > 0:
    	    #data = "{serialnum : " + str(source.getSerialNum()) + ", rcvts : " + str(datetime.datetime.now()) + ", angularRate:{ x : " + str(spatialData.AngularRate[0]) + " , y :  " + str(spatialData.AngularRate[1]) +" , z : " + str(spatialData.AngularRate[2]) + "} }"
    	    data = "angular," + str(serialnum) + "," + str(datetime.datetime.now()) + "," + str(spatialData.AngularRate[0]) + "," + str(spatialData.AngularRate[1]) +"," + str(spatialData.AngularRate[2])
    	    resp, content = h.request(springxd_url, 'POST', data)
        if len(spatialData.MagneticField) > 0:
            data = "magnetic," + str(serialnum) + "," + str(datetime.datetime.now()) + "," + str(spatialData.MagneticField[0]) + "," + str(spatialData.MagneticField[1]) +"," + str(spatialData.MagneticField[2])
            resp, content = h.request(springxd_url, 'POST', data)

def GPSAttached(e):
    attached = e.device
    print("GPS %i Attached!" % (attached.getSerialNum()))

def GPSDetached(e):
    detached = e.device
    print("GPS %i Detached!" % (detached.getSerialNum()))

def GPSError(e):
    try:
        source = e.device
        print("GPS %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def GPSPositionChanged(e):
	global prev_lat
	global prev_long
	global prev_alt
	source = e.device
	serialnum = source.getSerialNum()
	if (abs(e.latitude - prev_lat) > .001 or abs(e.longitude - prev_long) > .001 or abs(e.altitude - prev_alt) > .001):
		data = "gps," + str(serialnum) + "," + str(datetime.datetime.now()) + "," + str(e.latitude) + "," + str(e.longitude) +"," + str(e.altitude)
		resp, content = h.request(springxd_url, 'POST', data)
		prev_lat = e.latitude
		prev_long = e.longitude
		prev_alt = e.altitude
    #print("GPS %i: Latitude: %F, Longitude: %F, Altitude: %F, Date: %s, Time: %s" % (source.getSerialNum(), e.latitude, e.longitude, e.altitude, source.getDate().toString(), source.getTime().toString()))

def GPSPositionFixStatusChanged(e):
    source = e.device
    if e.positionFixStatus:
        status = "FIXED"
    else:
        status = "NOT FIXED"
    print("GPS %i: Position Fix Status: %s" % (source.getSerialNum(), status))
#Main Program Code
try:
    spatial.setOnAttachHandler(SpatialAttached)
    spatial.setOnDetachHandler(SpatialDetached)
    spatial.setOnErrorhandler(SpatialError)
    spatial.setOnSpatialDataHandler(SpatialData)
    
    gps.setOnAttachHandler(GPSAttached)
    gps.setOnDetachHandler(GPSDetached)
    gps.setOnErrorhandler(GPSError)
    gps.setOnPositionChangeHandler(GPSPositionChanged)
    gps.setOnPositionFixStatusChangeHandler(GPSPositionFixStatusChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    spatial.openPhidget()
    gps.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    print("Waiting for accelerometer attach....")
    spatial.waitForAttach(10000)
    print("accelerometer attached....")
    print("Waiting for GPS attach....")
    gps.waitForAttach(10000)
    print("GPS attached....")
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        spatial.closePhidget()
        gps.closePhidget()
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
    gps.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
