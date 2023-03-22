#start multiple machine agents at once
import os, signal
import time
import json
import sys, json
import xml.etree.ElementTree as ET

start_time = time.time()

def process():
	
    url="controllerces.saas.appdynamics.com"
    
    port=443
    agentJar="/Users/satbisin/Desktop/Appd/Agents/machineagent-bundle-64bit-linux-22.12.0.3535/machineagent.jar"
    num=20
    for i in range(num):
        print(i)
        # add access key below
        print("java -Dappdynamics.controller.hostName=" + url +" -Dappdynamics.controller.port=" + str(port) + " -Dappdynamics.controller.ssl.enabled=true  -Dappdynamics.agent.applicationName=App1 -Dappdynamics.agent.tierName=App1_Tier"+ str(i) + " -Dappdynamics.agent.nodeName=App1_Tier1_Node"+ str(i) + " -Dappdynamics.agent.accountName=controllerces -Dappdynamics.agent.accountAccessKey= \
                -Dappdynamics.agent.uniqueHostId=SATBISIN-M-8481-" + str(i) + " -jar " +agentJar + " &")
        os.system("java -Dappdynamics.controller.hostName=" + url +" -Dappdynamics.controller.port=" + str(port) + " -Dappdynamics.controller.ssl.enabled=true  -Dappdynamics.agent.applicationName=App1 -Dappdynamics.agent.tierName=App1_Tier"+ str(i) + " -Dappdynamics.agent.nodeName=App1_Tier1_Node"+ str(i) + " -Dappdynamics.agent.accountName=controllerces -Dappdynamics.agent.accountAccessKey= \
                -Dappdynamics.agent.uniqueHostId=SATBISIN-M-8481-" + str(i) + " -jar " +agentJar + " &")

process()

print("--- %s seconds ---" % (time.time() - start_time))



