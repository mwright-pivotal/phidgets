import groovy.json.*

def slurper = new JsonSlurper()
def jsPayload = slurper.parseText(payload)

return jsPayload.rcvts + "|" + jsPayload.type + "|" + jsPayload.x + "|" + jsPayload.y + "|" + jsPayload.z