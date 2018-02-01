# coding: utf-8

def tripTime(trip1):
    if type(trip1) == list:
        hr1, mn1 = trip1[0].get("Origin").get("time").split(":")
        hr2, mn2 = trip1[-1].get("Destination").get("time").split(":")
        hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)
        if not trip1[0].get("Origin").get("date") == trip1[-1].get("Destination").get("date"):
            if hr1 < hr2:
                hr1 += 24
            else:
                hr2 += 24
    else:
        hr1, mn1 = trip1.get("Origin").get("time").split(":")
        hr2, mn2 = trip1.get("Destination").get("time").split(":")
        hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)
        if not trip1.get("Origin").get("date") == trip1.get("Destination").get("date"):
            if hr1 < hr2:
                hr1 += 24
            else:
                hr2 += 24
    mn1 += hr1 * 60
    mn2 += hr2 * 60
    tTime = mn2 - mn1
    tH = tTime // 60
    tM = tTime % 60
    return tTime, tH, tM

def plan(self, fr, to, timeP, date, arr, sChTime):
    toStop, toStopname = self.api.findStop(to)
    if not toStop:
        print("Destination stop not found.")
        return

    frStop, frStopname = self.api.findStop(fr)
    if not frStop:
        print("Origin stop not found.")
        return

    trip = self.api.getPlan(frStop, toStop, time_=timeP, date=date, arr=arr, sChTime=sChTime)
    self.printPlan(trip, toStopname, frStopname)

def dep(self, stop, timeP, date):
    # Find stop
    stop, stopname = self.api.findStop(stop)
    if not stop:
        print("Stop not found.")
        return

    # Get departures from stop
    departures = self.api.getDepartures(stop, date=date, time_=timeP)
    self.printDepartures(departures, stopname, date, timeP)

def getDelay(times):
    if not times.get("rtDepTime"):
        hr1, mn1 = times.get("rtArrTime").split(":")
        hr2, mn2 = times.get("arrTime").split(":")
        rtDate = times.get("rtArrDate")
        date = times.get("arrDate")
    else:
        hr1, mn1 = times.get("rtDepTime").split(":")
        hr2, mn2 = times.get("depTime").split(":")
        rtDate = times.get("rtDepDate")
        date = times.get("depDate")
    hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)

    if not rtDate == date:
        if hr1 < hr2:
            hr1 += 24
        else:
            hr2 += 24
    mn1 += hr1 * 60
    mn2 += hr2 * 60
    delay = mn1 - mn2
    if delay >= 0:
        delay = " +" + str(delay)
    else:
        delay = " " + str(delay)
    return delay

if __name__ == "__main__":        
	print("This file is only supposed to be used as a module.")