"""
Script that counted time into our Kanban application. We had start and stop timestamps and were able to get total times input on each task from that.
"""


import json
from datetime import datetime
from datetime import timedelta


data=None
topData=None
with open('<Export URL>') as f:

	myObject=f.read()
	u = myObject.decode('utf-8-sig')
	myObject = u.encode('utf-8')

	
	topData=json.loads(myObject,'utf-8')
	data = topData["PROD"]["Finished"]


def calculateAll6PMTimeStampsSinceJanuary12020():
	fin=[]
	startTime=1609552896
	for i in range(180):
		fin.append((startTime+i*24*60*60)*1000)
	return fin


def calculateTime(starts,stops):
	tempStarts=starts
	tempStops=sorted(stops+calculateAll6PMTimeStampsSinceJanuary12020())
	totalTime=0
	while len(tempStarts) > 0:
		(firstStart, tempStarts)=(tempStarts[0],tempStarts[1:])
		while (sorted([firstStart]+tempStops)[0] < firstStart):
			tempStops=tempStops[1:]
		if (tempStops == []):
			return totalTime/(1000.0*60.0*60.0)
		(firstTempStop, tempStops)=(tempStops[0],tempStops[1:])
		totalTime=totalTime+(firstTempStop-firstStart)
	return totalTime/(1000.0*60.0*60.0)


def timeIntoActivity(unitNumber,activityName):
	activity=data[unitNumber+"-"+activityName]
	return calculateTime(activity["startTimes"], activity["pauseTimes"])



def returnKey(o,k, emptyVersion):
	if (k in o):
		if (type(o[k]) == str):
			return o[k].encode('utf-8', 'ignore')
		return o[k]
	return emptyVersion


def calculateHoursLoggedPerDayByPerson(person):
	totalHoursLogged=180*[0.0]
	for k in data:
		thisActivityHours=[]
		activity=data[k]
		if (activity["startTimesName"][0] == person or person=="ALL"):
			st=activity["startTimes"]
			pt=sorted(activity["pauseTimes"]+calculateAll6PMTimeStampsSinceJanuary12020())
			jan1time=1609552896
			for i in range(180):
				lastTime=(jan1time+i*24*60*60)*1000+10
				firstTime=(jan1time+i*24*60*60)*1000-12*60*60*1000-10
				thisDayStartTimes=[]
				thisDayPauseTimes=[]
				for entry in st:
					if (entry > firstTime and entry < lastTime):
						thisDayStartTimes.append(entry)
				for entry in pt:
					if (entry > firstTime and entry < lastTime):
						thisDayPauseTimes.append(entry)
				thisActivityHours.append(calculateTime(thisDayStartTimes, thisDayPauseTimes))
			for i in range(180):
				totalHoursLogged[i]=totalHoursLogged[i]+thisActivityHours[i]
	return totalHoursLogged

def findStartTimePeople(thisEntry):
	if (not "startTimesName" in thisEntry):
		return ""
	names=thisEntry["startTimesName"]
	nameSet=set()
	for name in names:
		nameSet.add(name)
	fin=""
	for n in nameSet:
		if (fin == ""):
			fin=n.encode('utf-8', 'ignore')
		else:
			fin=fin+" : "+n.encode('utf-8', 'ignore')
	return fin


def daysWorkedOn(thisEntry):
	if (not "startTimes" in thisEntry):
		return "no times"

	dates=set()
	lowM=34
	lowD=34
	highM=0
	highD=0
	for t in thisEntry["startTimes"]:
		date = datetime.fromtimestamp(t/1000)
		td=timedelta(hours=7)
		date=date-td
		if (date.month < lowM):
			lowM=date.month
			lowD=date.day
		if (date.month > highM):
			highM=date.month
			highD=date.day
		if (date.month == lowM and date.day < lowD):
			lowM=date.month
			lowD=date.day
		if (date.month == highM and date.day > highD):
			highM=date.month
			highD=date.day
		dates.add(str(date.month)+"/"+str(date.day))
	fin="DATES: "
	for d in dates:
		fin=fin+"-"+d
	return str(lowM)+"/"+str(lowD)+"-"+str(highM)+"/"+str(highD)
	return fin




import csv
with open('<TASK CSV>', 'w') as csvfile:

	sw = csv.writer(csvfile, delimiter=',')
	cur={ "Finished":topData["PROD"]["Finished"], "In Progress":topData["PROD"]["InProgress"]}

	for startKey in cur:
		CURRENT=cur[startKey]
		for k in CURRENT:
			thisEntry=CURRENT[k]
			(unitNumber,activity)=(k.split("-")[0],k.split("-")[1])

			unitNumber=unitNumber.encode('utf-8', 'ignore')
			activity=activity.encode('utf-8', 'ignore')
			station=returnKey(thisEntry,"Category", "No Category")
			cat=returnKey(thisEntry,"Category", "No Category")
			due=returnKey(thisEntry,"DueDate", "No Due Date")
			start=timesToday(returnKey(thisEntry,"startTimes", []))
			end=timesToday(returnKey(thisEntry,"pauseTimes", []))
			t=str(calculateTime(start,end)).encode('utf-8', 'ignore')
			startNames=returnKey(thisEntry,"startTimesName", "No Person Worked on this")
			endNames=returnKey(thisEntry,"pauseTimesName", "No Person Worked on this")
			timeStamps=extractTimeStamps(start, startNames, end, endNames)

			if (t > 0.01):
				sw.writerow([unitNumber,station,activity,startKey,due,cat,t])
