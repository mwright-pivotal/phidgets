import groovy.json.*

def (t,s,ts,x,y,z) =  payload.split(',')
def data = [type: t,serialnum: s, rcvts: ts,x: x,y: y,z: z]
class PhidgetSpatial {     def spatial }
def myB = new PhidgetSpatial(spatial: data)
def js3 = new JsonBuilder(myB)
return js3.toString()