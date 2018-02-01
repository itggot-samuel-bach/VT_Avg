# coding: utf-8

import os
import time
import json
from tkinter import *
import webbrowser

from APIRequest import APIRequest
from mapmaker import GeometryDoc

# os.chdir("C:\Edvin\Vasttrafik")
		

class BackButton(Frame):
    def __init__(self, window):
        Frame.__init__(self, window.frame)
        self.button = Button(self, text="Gå tillbaka", command=window.mainMenu)
        self.button.pack(fill=BOTH, expand=True)


class Window(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.api = APIRequest()

        self.frame = Frame(self)
        self.frame.pack()
        self.mainMenu()

    def clearFrame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def mainMenu(self):
        self.clearFrame()

        Label(self.frame, text="Välkommen till planeraren!", font='bold', padx=10, pady=5).pack(fill=BOTH, expand=True)
        Button(self.frame, text="Reseplanerare", padx=5, pady=2, command=self.planBox).pack(fill=BOTH, expand=True)
        Button(self.frame, text="Avgångar", padx=5, pady=2, command=self.depBox).pack(fill=BOTH, expand=True)
        Button(self.frame, text="Ta mig hem", padx=5, pady=2, command=self.takeHomeBox).pack(fill=BOTH, expand=True)
        self.frame.mainloop()

    def planBox(self):
        self.clearFrame()
        BackButton(self).grid(row=0, column=0, columnspan=4, sticky=NE + SW)

        Label(self.frame, text="Reseplanerare", font="bold").grid(row=1, column=0, columnspan=4, sticky=NE + SW)

        Label(self.frame, text="Fr\u00e5n").grid(row=2, column=0, columnspan=1, sticky=NE + SW)
        frombox = Entry(self.frame)
        frombox.grid(row=2, column=1, columnspan=2, sticky=NE + SW)
        Button(self.frame, text="Rensa", command=lambda: frombox.delete(0, END)).grid(row=2, column=3, columnspan=1, sticky=NE + SW)

        Label(self.frame, text="Till").grid(row=3, column=0, columnspan=1, sticky=NE + SW)
        tobox = Entry(self.frame)
        tobox.grid(row=3, column=1, columnspan=2, sticky=NE + SW)
        Button(self.frame, text="Rensa", command=lambda: tobox.delete(0, END)).grid(row=3, column=3, columnspan=1, sticky=NE + SW)

        Label(self.frame, text="Tid").grid(row=4, column=0, columnspan=1, sticky=NE + SW)
        timebox = Entry(self.frame)
        timebox.grid(row=4, column=1, columnspan=2, sticky=NE + SW)
        timebox.insert(END, time.strftime("%H:%M"))

        Label(self.frame, text="Datum").grid(row=5, column=0, columnspan=1, sticky=NE + SW)
        datebox = Entry(self.frame)
        datebox.grid(row=5, column=1, columnspan=2, sticky=NE + SW)
        datebox.insert(END, time.strftime("%Y-%m-%d"))

        Button(self.frame, text="Nu", command=lambda: self.setNow(timebox, datebox)).grid(row=4, column=3, rowspan=2, sticky=NE + SW)

        Button(self.frame, text="Fler val", command=self.moreOptions).grid(row=6, column=0, columnspan=4, sticky=NE + SW)
        self.arr = BooleanVar()
        self.sChTime = BooleanVar()
        self.x = BooleanVar()

        Button(self.frame, text="Sök resa", command=lambda: self.plan(frombox.get(), tobox.get(), timebox.get(), datebox.get(), 
            self.arr.get(), self.sChTime.get())).grid(column=0, columnspan=4, sticky=NE + SW)
        self.frame.bind("<Return>", lambda event: self.plan(frombox.get(), tobox.get(), timebox.get(), datebox.get(),
                                                            self.arr.get(), self.sChTime.get()))

        self.frame.mainloop()

    def moreOptions(self):
        root = Toplevel()
        Label(root, text="Fler val", font="bold").grid(row=0, column=0, columnspan=2, sticky=NE + SW)

        Radiobutton(root, text="Ankomst", variable=self.arr, value=True).grid(row=1, column=0, columnspan=1, sticky=N + SW)
        Radiobutton(root, text="Avg\u00e5ng", variable=self.arr, value=False).grid(row=1, column=1, columnspan=1, sticky=N + SW)

        Checkbutton(root, text="Kort bytestid", variable=self.sChTime).grid(row=2, column=0, columnspan=1, sticky=N + SW)

        Checkbutton(root, text="Not in use", variable=self.x).grid(row=2, column=1, columnspan=1, sticky=N + SW)

        Button(root, text="Klar", command=root.destroy).grid(row=3, column=0, columnspan=2, sticky=NE + SW)

        root.mainloop()

    def plan(self, fr, to, timeP, date, arr, sChTime):
        print(arr)
        print(sChTime)

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

    def printPlan(self, trips, to, fr, frame=None):
        if frame is None:
            frame = self.frame
            self.clearFrame()
            BackButton(self).grid(column=0, columnspan=2, sticky=NE + SW)
        trip = []

        if type(trips) == list:
            for i in trips:
                trip.append(i.get("Leg"))
        elif type(trips) == dict:
            trip[0] = trips.get("Leg")

        Label(frame, font='bold', text="Fr\u00e5n " + fr + " till " + to).grid(column=0, columnspan=2, sticky=NE + SW)
        

        for i in trip:
            self.printLeg(frame, i)

    def printLeg(self, root, trip1):
        frame = Frame(root, bd=2, relief=GROOVE)
        frame.grid(column=0, columnspan=2, sticky=NE + SW)

        if type(trip1) == list:

            tTime, tH, tM = self.tripTime(trip1)

            Label(frame, text= f'Resa {trip1[0].get("Origin").get("time")}-{trip1[-1].get("Destination").get("time")} - Restid {str(tH)} h {str(tM)} min', pady=5).grid(row=0, column=0, columnspan=2, sticky=NE + SW)
                                                                                          
            print(trip1[0].get("GeometryRef").get("ref"))
            Button(frame, text="Karta", command= lambda: self.geometryBackEnd(trip1)).grid(row=1, column=0, columnspan=2, sticky=NE+SW)

            for i, j in enumerate(trip1):
                if j.get("type") == "WALK":
                    if not j.get("Origin").get("name") == j.get("Destination").get("name"):
                        Label(frame, text=j.get("Origin").get("time") + " - " + j.get("Destination").get(
                            "time")).grid(row=i + 2, column=1, sticky=NE + SW)
                        Label(frame,
                              text=j.get("name") + " till " + j.get("Destination").get("name")).grid(
                            row=i + 2, column=0, sticky=NE + SW)


                else:
                    Label(frame, text=j.get("Origin").get("time") + " - " + j.get("Destination").get(
                        "time")).grid(row=i + 2, column=1, sticky=NE + SW)
                    Button(frame, text=j.get("name") + " till " + j.get("Destination").get("name"),
                           bg=j.get("fgColor"), fg=j.get("bgColor"),
                           command=lambda j=j: self.displayRoute(j.get("JourneyDetailRef").get("ref"), v2=True),
                           relief=FLAT).grid(row=i + 2, column=0, sticky=NE + SW)


        elif type(trip1) == dict:
            tTime, tH, tM = self.tripTime(trip1)

            Label(frame, text="Resa " + trip1.get("Origin").get("time") + "-" + trip1.get("Destination").get(
                "time") + " - Restid " + str(tH) + " h " + str(tM) + " min", pady=5).pack(side=TOP, fill=X)
            Button(frame, text="Karta", command= lambda: self.geometryBackEnd(trip1.get("GeometryRef").get("ref"), trip1.get("fgColor"))).pack(fill=X)

            Button(frame, text=trip1.get("name") + " till " + trip1.get("Destination").get("name"),
                   bg=trip1.get("fgColor"), fg=trip1.get("bgColor"),
                   command=lambda: self.displayRoute(trip1.get("JourneyDetailRef").get("ref"), v2=True),
                   relief=FLAT).pack(side=LEFT, fill=X)
            Label(frame, text=trip1.get("Origin").get("time") + " - " + trip1.get("Destination").get("time")).pack(
                side=LEFT)

    def tripTime(self, trip1):

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

    def setNow(self, timebox, datebox):
        timebox.delete(0, END)
        timebox.insert(END, time.strftime("%H:%M"))
        datebox.delete(0, END)
        datebox.insert(END, time.strftime("%Y-%m-%d"))

    def displayRoute(self, url, v2=False):
        stops = self.api.getRoute(url, v2)

        # New Tkinter window
        routeRoot = Toplevel()

        # Get name of route ("Buss 50")
        try:
            name = stops.get("JourneyName")[0].get("name")
        except KeyError:
            name = stops.get("JourneyName").get("name")

        # Make names presentable
        name = name.replace("Bus", "Buss")
        name = name.replace("Sp\u00e5", "Sp\u00e5rvagn")
        name = name.replace("Reg T\u00c5G", "T\u00e5g")
        name = name.replace("Fär", "Färja")

        # Get destination ("Centralstationen")
        try:
            dest = stops.get("Direction")[0].get("$")
        except KeyError:
            dest = stops.get("Direction").get("$")

        # Store colour-dict in variable
        colour = stops.get("Color")

        # Print out line and destination
        lab = Label(routeRoot, text=name + " mot " + dest, bg=colour.get("fgColor"), fg=colour.get("bgColor"))

        if len(stops.get("Stop")) > 30:
            lab.grid(sticky=NE + SW, row=0, column=0, columnspan=4)
            k = 4
        else:
            lab.grid(sticky=NE + SW, row=0, column=0, columnspan=2)
            k = 2

        # Print stops and times
        for i, j in enumerate(stops.get("Stop")):
            clm = 0
            row = i
            if len(stops.get("Stop")) > 30:
                if i >= len(stops.get("Stop")) // 2:
                    clm = 2
                    row = i - (len(stops.get("Stop")) // 2)

            Label(routeRoot, text=j.get("name")).grid(sticky=NE + SW, row=row + 1, column=clm)
            # Tries to get times. RT Dep -> TT Dep -> RT Arr -> TT Arr -> Error
            if not j.get("rtDepTime"):
                if not j.get("depTime"):
                    if not j.get("rtArrTime"):
                        if not j.get("arrTime"):
                            Label(routeRoot, text="Error").grid(sticky=NE + SW, row=row + 1, column=clm + 1)
                        else:
                            Label(routeRoot, text="a(" + j.get("arrTime") + ")").grid(sticky=NE + SW, row=row + 1, column=clm + 1)
                    else:
                        hr1, mn1 = j.get("rtArrTime").split(":")
                        hr2, mn2 = j.get("arrTime").split(":")
                        hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)
                        if not j.get("rtArrDate") == j.get("arrDate"):
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
                        Label(routeRoot, text="a" + j.get("arrTime") + delay).grid(sticky=NE + SW, row=row + 1, column=clm + 1)
                else:
                    Label(routeRoot, text="(" + j.get("depTime") + ")").grid(sticky=NE + SW, row=row + 1, column=clm + 1)
            else:
                hr1, mn1 = j.get("rtDepTime").split(":")
                hr2, mn2 = j.get("depTime").split(":")
                hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)
                if not j.get("rtDepDate") == j.get("depDate"):
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
                Label(routeRoot, text=j.get("depTime") + delay).grid(sticky=NE + SW, row=row + 1, column=clm + 1)

        Button(routeRoot, text="Karta", command= lambda: self.geometryBackEnd(stops.get("GeometryRef").get("ref"), colour.get("fgColor"))).grid(column=0, columnspan=k, sticky=NE+SW)

        Button(routeRoot, text="Stäng", command=routeRoot.destroy).grid(column=0, columnspan=k, sticky=NE + SW)

    def depBox(self):
        self.clearFrame()
        BackButton(self).grid(row=0, column=0, columnspan=3, sticky=NE + SW)

        Label(self.frame, text="Avgångar", font="bold").grid(row=1, column=0, columnspan=3, sticky=NE + SW)

        Label(self.frame, text="Hållplats").grid(row=2, column=0, columnspan=1, sticky=NE + SW)
        stopbox = Entry(self.frame)
        stopbox.grid(row=2, column=1, columnspan=1, sticky=NE + SW)
        Button(self.frame, text="Rensa", command=lambda: stopbox.delete(0, END)).grid(row=2, column=2, columnspan=1, sticky=NE + SW)

        Label(self.frame, text="Tid").grid(row=3, column=0, columnspan=1, sticky=NE + SW)
        timebox = Entry(self.frame)
        timebox.grid(row=3, column=1, columnspan=1, sticky=NE + SW)
        timebox.insert(END, time.strftime("%H:%M"))

        Label(self.frame, text="Datum").grid(row=4, column=0, columnspan=1, sticky=NE + SW)
        datebox = Entry(self.frame)
        datebox.grid(row=4, column=1, columnspan=1, sticky=NE + SW)
        datebox.insert(END, time.strftime("%Y-%m-%d"))

        Button(self.frame, text="Nu", command=lambda: self.setNow(timebox, datebox)).grid(row=3, column=2, rowspan=2, sticky=NE + SW)

        Button(self.frame, text="Sök", command=lambda: self.dep(stopbox.get(), timebox.get(), datebox.get())).grid(
            row=5, column=0, columnspan=3, sticky=NE + SW)
        self.frame.bind("<Return>", lambda event: self.dep(stopbox.get(), timebox.get(), datebox.get()))

        self.frame.mainloop()

    def dep(self, stop, timeP, date):
        # Find stop
        stop, stopname = self.api.findStop(stop)
        if not stop:
            print("Stop not found.")
            return

        # Get departures from stop
        departures = self.api.getDepartures(stop, date=date, time_=timeP)
        self.printDepartures(departures, stopname, date, timeP)

    def printDepartures(self, departures, stopname, date, time_):
        self.clearFrame()
        BackButton(self).grid(row=0, column=0, columnspan=3, sticky=NE + SW)

        headline = Label(self.frame, text="Avgångar från " + stopname + " " + time_ + " " + date, pady=5, padx=10)
        headline.grid(row=1, column=0, columnspan=3, sticky=E + W)

        for i, j in enumerate(departures):
            Label(self.frame, text=j.get("sname"), bg=j.get("fgColor"),
                  fg=j.get("bgColor")).grid(row=i + 2, column=0, sticky=NE + SW)
            Button(self.frame, text=j.get("direction"),
                   command=lambda j=j: self.displayRoute(j.get("JourneyDetailRef").get("ref"))).grid(
                row=i + 2, column=1, sticky=E + W)
            if not j.get("rtTime"):
                Label(self.frame, text="ca " + j.get("time")).grid(row=i + 2, column=2, sticky=NE + SW)
            else:

                hr1, mn1 = j.get("rtTime").split(":")
                hr2, mn2 = j.get("time").split(":")
                hr1, hr2, mn1, mn2 = int(hr1), int(hr2), int(mn1), int(mn2)
                if not j.get("rtDate") == j.get("date"):
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

                Label(self.frame, text=j.get("time") + delay).grid(row=i + 2, column=2, sticky=NE + SW)

    def takeHomeBox(self):
        pass

    def geometryBackEnd(self, ref, colour=None):
        if type(ref) == list:
            doc = GeometryDoc()
            for i in ref:
                geoRef = i.get("GeometryRef").get("ref")
                points = self.api.geometry(geoRef)
                
                colour = i.get("fgColor")
                if colour is None: colour = "#00FF00"
                
                doc.addPoly(points, colour)
                doc.addMarker(points[0])
            doc.addMarker(points[-1])
        
        else:
            points = self.api.geometry(ref)
            doc = GeometryDoc()
            doc.addPoly(points, colour)
            doc.addMarker(points[0])
            doc.addMarker(points[-1])

        folder = os.path.dirname(__file__).replace("\\", "/")
        path = "file:///" + folder + "/tempfiles/doc.html"
        webbrowser.open(path)

if __name__ == "__main__":        
	gui = Window()
