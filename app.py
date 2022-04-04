from multiprocessing.sharedctypes import Value
import os
from queue import Empty
from flask import Flask, render_template, request, session
import json

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

@app.route("/", methods=['GET','POST'])
def init():
    session['temp_db'] = {}
    return "INIT"

@app.route("/ingest", methods=['GET','POST'])
def ingest():
    data = {**session['temp_db'],**request.get_json()}
    session['temp_db'] = data
    return "Data has been ingested"

@app.route("/getbacklog", methods=['GET'])
def getBacklog():
    data = session['temp_db']
    return data

@app.route("/searchbug", methods=['GET','POST'])
def getBlockedEpicsByBugName():
    data = session['temp_db']
    searchBugName = request.data.decode("utf-8")
    blockedEpics = []
    for key,value in data.items():
        if searchBugName in value['Bugs']:
            blockedEpics.append(key)

    return "BLOCKED EPICS ARE: "+ str(blockedEpics).strip('[]')

@app.route("/searchbugbyepic", methods=['GET','POST'])
def getBugsByEpicName():
    data = session['temp_db']
    searchEpicName = request.data.decode("utf-8")
    epicData = data[searchEpicName]
    print(epicData)
    listOfBugs = []
    #get current epic bugs
    listOfBugs.extend(epicData['Bugs'])
    #get linked epics bugs
    if epicData['Epics']:
        for epic in epicData['Epics']:
            if data[epic]["Bugs"]:
                listOfBugs.extend(data[epic]["Bugs"])

    return "BLOCKED EPICS ARE: "+ str(listOfBugs).strip('[]')

@app.route("/updateEpic", methods=['GET','POST'])
def addTaskOrBugInAEpic():
    data = session['temp_db']
    dataToBeUpdated = request.get_json()
    #Check Epic exsists
    if data[dataToBeUpdated["Epic"]]:
        data[dataToBeUpdated["Epic"]]["Tasks"].extend(dataToBeUpdated["Tasks"])
        data[dataToBeUpdated["Epic"]]["Bugs"].extend(dataToBeUpdated["Bugs"])
    session['temp_db'] = data
    return data

@app.route("/deleteTaskOrBug", methods=['GET','POST'])
def deleteTaskOrBug():
    data = session['temp_db']
    dataToBeDeleted = request.data.decode("utf-8")
    #Search by epic
    for key, value in data.items():
        #check and delete if its a bug
        if dataToBeDeleted in value["Bugs"]:
            value["Bugs"].remove(dataToBeDeleted)
        #check and delete if its a task
        if dataToBeDeleted in value["Tasks"]:
            value["Tasks"].remove(dataToBeDeleted)
    session['temp_db'] = data
    return data

@app.route("/exportBacklog", methods=['GET','POST'])
def exportBacklog():
    data = session['temp_db']
    with open('backlog.json', 'w') as f:
        json.dump(data, f)

    return "BACKLOG EXPORTED"
