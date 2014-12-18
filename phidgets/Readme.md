This project contains an end to end demo that captures data from a Phidget
Spatial sensor.  The sensor has an accelerometer, gyroscope, and compass.  Each
send x,y,z measurements at a desired data rate.

 

**Flow**
--------

1. Phidget Spatial (1044)

2. Phidget SBC

3. Spatial-demo.py on SBC

4. POST to http://phidgets.mikepwright.dyndns.ws:8080

5. Spring XD

    A) RabbitMQ on PCF

        i. Spring App using Websockets and Chart.js (PCF)

        ii. HDFS & HAWQ

6. TODO: Use MADlib to generate a model representing normal movements.  Use the
model to generate an alert based on non-compliant motion data.

 

 
