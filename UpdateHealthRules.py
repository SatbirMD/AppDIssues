import requests
import json
import sys, json
import xml.etree.ElementTree as ET
import subprocess

"""
1)get list of all the applications  and their HR's getting impacted - sql query
2)iterate over each app and its HR
3)Check if there are new nodes adedd
https://docs.appdynamics.com/appd/22.x/22.5/en/extend-appdynamics/appdynamics-apis/application-model-api#id-.ApplicationModelAPIv22.1-RetrieveNodeInformationforAllNodesinaBusinessApplication
4)If new node is added then check any new events for the HR's for this app
https://docs.appdynamics.com/appd/22.x/22.5/en/extend-appdynamics/appdynamics-apis/alert-and-respond-api/events-and-action-suppression-api#id-.EventsandActionSuppressionAPIv22.1-RetrieveEventData
5) If new events then fetch the HR and save it, new servers should start to evaluate
https://docs.appdynamics.com/appd/22.x/22.5/en/extend-appdynamics/appdynamics-apis/alert-and-respond-api/health-rule-api#id-.HealthRuleAPIv22.1-UpdateaHealthRule
6) If no new events then add it to the list of HR's that have new nodes but cannot be re-saved right now
"""

"""
javaquery = queryJava + "AND acn.id IN (" + ','.join([str(key) for key in dict_java.keys()]) + ")"
        javaresult = dbConnect(dbHostName, javaquery, 'controller', mysql_passwd)
        addRecordToCSV(outFileCSV, javaresult)
"""



#create dictionary of Application and array of its AppId, HRId and HR Name
App_HR_dic = {
    "AIX.PRD.RADIXX": [5137,24328,"Disk usage is too high"]
}

#username, password
authenticationDetails = ('satbir.singh%40appdynamics.com@controllerces', '')
host="controllerces"

#dictionary with Application and HR name which are not saved due to events currently active
App_HR_NotSaved = {}

#iterate over the each app and its HR's
for appName, value in App_HR_dic.items():
    print("Iterating for this set " , appName, ":", value[0], ":", value[1])

    #fetch the HR detils so that it can be used to update the HR
    hrDetailsResponse = requests.get("https://"+host+".saas.appdynamics.com/controller/alerting/rest/v1/applications/" + str(value[0]) + "/health-rules/" + str(value[1]), auth=authenticationDetails, headers={"Content-Type":"application/x-www-form-urlencoded"})
    # time period to check for a HR violation

    hrDR = json.loads(hrDetailsResponse.text)
    waitTimeAfterViolation=hrDR['waitTimeAfterViolation'] +2

    #check if there are events for an application
    eventPayload = {'time-range-type': 'BEFORE_NOW', 'duration-in-mins': waitTimeAfterViolation,'event-types': 'POLICY_OPEN_WARNING,POLICY_OPEN_CRITICAL,POLICY_UPGRADED,POLICY_DOWNGRADED,POLICY_CONTINUES_WARNING,POLICY_CONTINUES_CRITICAL,POLICY_CLOSE_WARNING,POLICY_CLOSE_CRITICAL,POLICY_CANCELED_WARNING', 'severities': 'INFO,WARN,ERROR','output': 'JSON'}

    #response = requests.get('https://controllerces.saas.appdynamics.com/controller/rest/applications/abhi-ca-auto-instrumentation-apptest/events\?time-range-type=BEFORE_NOW\&duration-in-mins=11520\&event-types=POLICY_OPEN_CRITICAL,POLICY_OPEN_WARNING,POLICY_CONTINUES_CRITICAL\&severities=INFO,WARN,ERROR\&output=JSON', headers={"Content-Type":"application/x-www-form-urlencoded"}, auth=authenticationDetails)

    eventResponse = requests.get("https://"+ host + ".saas.appdynamics.com/controller/rest/applications/" + appName + "/events", params=eventPayload, auth=authenticationDetails)

    er = json.loads(eventResponse.text)
    print("Fetching events for an application, eventResponse.code : eventResponse.reasonis >> " + str(eventResponse.status_code) + " : " + eventResponse.reason)

    params = ""
    eventCount = 0
    for event in er:
        params =   str(event['id']) + "," + params
        eventCount=eventCount+1

    #print("parama >> " + params)
    print("Number of events for the application " + appName + " and Its HR named : " + value[2] +  " is " + str(eventCount))

    if eventCount == 0:
        #fetch the HR detils so that it can be used to update the HR
        
        hrUpdateResponse = requests.put("https://" + host + ".saas.appdynamics.com/controller/alerting/rest/v1/applications/" + str(value[0]) + "/health-rules/" + str(value[1]), data=json.dumps(hrDR),  headers={"Content-Type":"application/json"}, auth=authenticationDetails)
        #SQL query to verify if HR is updated
        # select *, FROM_UNIXTIME(execution_time_ms/1000)  from controller_audit_v2 where object_name="Test" \G
        #print("hrUpdateResponse.status_code is >> " + str(hrUpdateResponse.status_code))

        #print( "eventResponse.reason  >> " + hrUpdateResponse.reason)

        print("Updating Applications : " + appName + " and Its HR named : " + value[2])
    else:
        #add the Application  and HR name that are not save due to active events 
        print("Not Updating Applications : " + appName + " and Its HR named : " + value[2])
        App_HR_NotSaved={appName, value[2]}; 


