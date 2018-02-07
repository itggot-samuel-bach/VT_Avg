# coding: utf-8

import time
import json
import tkinter as tk

from APIRequest import APIRequest
import mapmaker
import misc
		
NESW = tk.NE + tk.SW

class BackButton(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window.frame)
        self.button = tk.Button(self, text="Gå tillbaka", command=window.mainMenu)
        self.button.pack(fill=tk.BOTH, expand=True)


class Viewport(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.api = APIRequest()

        self.frame = tk.Frame(self)
        self.frame.pack()
        self.mainMenu()

    def clearFrame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def mainMenu(self):
        self.clearFrame()

        tk.Label(self.frame, text="Välkommen till planeraren!", font='bold', padx=10, pady=5).pack(fill=tk.BOTH, expand=True)
        tk.Button(self.frame, text="Reseplanerare", padx=5, pady=2, command=self.tripPlanMenu).pack(fill=tk.BOTH, expand=True)
        tk.Button(self.frame, text="Avgångar", padx=5, pady=2, command=self.departuresMenu).pack(fill=tk.BOTH, expand=True)
        tk.Button(self.frame, text="Ta mig hem", padx=5, pady=2, command=self.takeMeHomeMenu).pack(fill=tk.BOTH, expand=True)
        self.frame.mainloop()

    def tripPlanMenu(self):
        self.clearFrame()
        BackButton(self).grid(row=0, column=0, columnspan=4, sticky=NESW)

        tk.Label(self.frame, text="Reseplanerare", font="bold").grid(row=1, column=0, columnspan=4, sticky=NESW)

        tk.Label(self.frame, text="Fr\u00e5n").grid(row=2, column=0, columnspan=1, sticky=NESW)
        frombox = tk.Entry(self.frame)
        frombox.grid(row=2, column=1, columnspan=2, sticky=NESW)
        tk.Button(self.frame, text="Rensa", command=lambda: frombox.delete(0, tk.END)).grid(row=2, column=3, columnspan=1, sticky=NESW)

        tk.Label(self.frame, text="Till").grid(row=3, column=0, columnspan=1, sticky=NESW)
        tobox = tk.Entry(self.frame)
        tobox.grid(row=3, column=1, columnspan=2, sticky=NESW)
        tk.Button(self.frame, text="Rensa", command=lambda: tobox.delete(0, tk.END)).grid(row=3, column=3, columnspan=1, sticky=NESW)

        tk.Label(self.frame, text="Tid").grid(row=4, column=0, columnspan=1, sticky=NESW)
        timebox = tk.Entry(self.frame)
        timebox.grid(row=4, column=1, columnspan=2, sticky=NESW)
        timebox.insert(tk.END, time.strftime("%H:%M"))

        tk.Label(self.frame, text="Datum").grid(row=5, column=0, columnspan=1, sticky=NESW)
        datebox = tk.Entry(self.frame)
        datebox.grid(row=5, column=1, columnspan=2, sticky=NESW)
        datebox.insert(tk.END, time.strftime("%Y-%m-%d"))

        tk.Button(self.frame, text="Nu", command=lambda: self.setNow(timebox, datebox)).grid(row=4, column=3, rowspan=2, sticky=NESW)

        tk.Button(self.frame, text="Fler val", command=self.moreOptions).grid(row=6, column=0, columnspan=4, sticky=NESW)
        self.arr = tk.BooleanVar()
        self.smallChangeTime = tk.BooleanVar()
        self.notInUse = tk.BooleanVar()

        tk.Button(self.frame, text="Sök resa", command=lambda: misc.plan(self, frombox.get(), tobox.get(), timebox.get(), datebox.get(), 
                  self.arr.get(), self.smallChangeTime.get())).grid(column=0, columnspan=4, sticky=NESW)
        self.frame.bind("<Return>", lambda event: misc.plan(self, frombox.get(), tobox.get(), timebox.get(), datebox.get(),
                                                            self.arr.get(), self.smallChangeTime.get()))

        self.frame.mainloop()

    def moreOptions(self):
        root = tk.Toplevel()
        tk.Label(root, text="Fler val", font="bold").grid(row=0, column=0, columnspan=2, sticky=NESW)

        tk.Radiobutton(root, text="Ankomst", variable=self.arr, value=True).grid(row=1, column=0, columnspan=1, sticky=tk.N + tk.SW)
        tk.Radiobutton(root, text="Avg\u00e5ng", variable=self.arr, value=False).grid(row=1, column=1, columnspan=1, sticky=tk.N + tk.SW)

        tk.Checkbutton(root, text="Kort bytestid", variable=self.smallChangeTime).grid(row=2, column=0, columnspan=1, sticky=tk.N + tk.SW)

        tk.Checkbutton(root, text="Not in use", variable=self.notInUse).grid(row=2, column=1, columnspan=1, sticky=tk.N + tk.SW)

        tk.Button(root, text="Klar", command=root.destroy).grid(row=3, column=0, columnspan=2, sticky=NESW)

        root.mainloop()


    def printPlan(self, trips, to, fr, frame=None):
        if frame is None:
            frame = self.frame
            self.clearFrame()
            BackButton(self).grid(column=0, columnspan=2, sticky=NESW)
        trip = []

        if type(trips) == list:
            for i in trips:
                trip.append(i.get("Leg"))
        elif type(trips) == dict:
            trip[0] = trips.get("Leg")

        tk.Label(frame, font='bold', text=f'Fr\u00e5n {fr} till {to}').grid(column=0, columnspan=2, sticky=NESW)
        

        for i in trip:
            self.printLeg(frame, i)

    def printLeg(self, root, trip):
        frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        frame.grid(column=0, columnspan=2, sticky=NESW)

        if type(trip) == list:

            triptime, tH, tM = misc.tripTime(trip)

            tk.Label(frame, text= f'Resa {trip[0].get("Origin").get("time")}-{trip[-1].get("Destination").get("time")} - Restid {str(tH)} h {str(tM)} min', pady=5).grid(row=0, column=0, columnspan=2, sticky=NESW)
                                                                                          
            # print(trip[0].get("GeometryRef").get("ref"))
            tk.Button(frame, text="Karta", command= lambda: mapmaker.geometryBackEnd(trip)).grid(row=1, column=0, columnspan=2, sticky=NESW)

            for i, leg in enumerate(trip):
                if leg.get("type") == "WALK":
                    if not leg.get("Origin").get("name") == leg.get("Destination").get("name"):
                        tk.Label(frame, text=leg.get("Origin").get("time") + " - " + leg.get("Destination").get(
                            "time")).grid(row=i + 2, column=1, sticky=NESW)
                        tk.Label(frame,text=leg.get("name") + " till " + leg.get("Destination").get("name")).grid(row=i + 2, column=0, sticky=NESW)


                else:
                    tk.Label(frame, text=leg.get("Origin").get("time") + " - " + leg.get("Destination").get("time")).grid(row=i + 2, column=1, sticky=NESW)
                    tk.Button(frame, text=leg.get("name") + " till " + leg.get("Destination").get("name"),
                           bg=leg.get("fgColor"), fg=leg.get("bgColor"),
                           command=lambda leg=leg: self.displayRoute(leg.get("JourneyDetailRef").get("ref")),
                           relief=tk.FLAT).grid(row=i + 2, column=0, sticky=NESW)


        elif type(trip) == dict:
            triptime, tH, tM = misc.tripTime(trip)

            depTime = trip.get("Origin").get("time")
            arrTime = trip.get("Destination").get("time")
            depDelay = misc.getDelay(trip.get("Origin"))
            arrDelay = misc.getDelay(trip.get("Destination"))
            print(f'Dep delay: {depDelay}, Arr delay: {arrDelay}')

            tk.Label(frame, text=f'Resa {depTime}-{arrTime} - Restid {str(tH)} h {str(tM)} min', pady=5).pack(side=tk.TOP, fill=tk.X)
            tk.Button(frame, text="Karta", command= lambda: mapmaker.geometryBackEnd(trip.get("GeometryRef").get("ref"), trip.get("fgColor"))).pack(fill=tk.X)

            tk.Button(frame, text=trip.get("name") + " till " + trip.get("Destination").get("name"),
                   bg=trip.get("fgColor"), fg=trip.get("bgColor"),
                   command=lambda: self.displayRoute(trip.get("JourneyDetailRef").get("ref")),
                   relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X)
            tk.Label(frame, text=f'{depTime}{depDelay} - {arrTime}{arrDelay}').pack(side=tk.LEFT)


    def setNow(self, timebox, datebox):
        timebox.delete(0, tk.END)
        timebox.insert(tk.END, time.strftime("%H:%M"))
        datebox.delete(0, tk.END)
        datebox.insert(tk.END, time.strftime("%Y-%m-%d"))

    def displayRoute(self, url):
        route = self.api.getRoute(url)

        # New Tkinter window
        routeRoot = tk.Toplevel()

        # Get name of route ("Buss 50")
        try:
            name = route.get("JourneyName")[0].get("name")
        except KeyError:
            name = route.get("JourneyName").get("name")

        # Make names presentable
        name = name.replace("Bus", "Buss")
        name = name.replace("Sp\u00e5", "Sp\u00e5rvagn")
        name = name.replace("Reg T\u00c5G", "T\u00e5g")
        name = name.replace("Fär", "Färja")

        # Get destination ("Centralstationen")
        try:
            destination = route.get("Direction")[0].get("$")
        except KeyError:
            destination = route.get("Direction").get("$")

        # Store colour-dict in variable
        colour = route.get("Color")

        # Print out line and destination
        label = tk.Label(routeRoot, text= f'{name} mot {destination}', bg=colour.get("fgColor"), fg=colour.get("bgColor"))

        print(f'Number of route: {len(route.get("Stop"))}')
        if len(route.get("Stop")) > 60:
            label.grid(sticky=NESW, row=0, column=0, columnspan=6)
            columns = 6
        elif len(route.get("Stop")) > 30:
            label.grid(sticky=NESW, row=0, column=0, columnspan=4)
            columns = 4
        else:
            label.grid(sticky=NESW, row=0, column=0, columnspan=2)
            columns = 2

        # Print route and times
        for i, stops in enumerate(route.get("Stop")):
            column = 0
            row = i
            if len(route.get("Stop")) > 60:
                if i >= 2 * len(route.get("Stop")) // 3:
                    column = 4
                    row = i - (2 * len(route.get("Stop")) // 3)
                elif i >= len(route.get("Stop")) // 3:
                    column = 2
                    row = i - (len(route.get("Stop")) // 3)
                
            elif len(route.get("Stop")) > 30:
                if i >= len(route.get("Stop")) // 2:
                    column = 2
                    row = i - (len(route.get("Stop")) // 2)
            

            tk.Label(routeRoot, text=stops.get("name")).grid(sticky=NESW, row=row + 1, column=column)
            # Tries to get times. RT Dep -> TT Dep -> RT Arr -> TT Arr -> Error
            if not stops.get("rtDepTime"):
                if not stops.get("depTime"):
                    if not stops.get("rtArrTime"):
                        if not stops.get("arrTime"):
                            tk.Label(routeRoot, text="Error").grid(sticky=NESW, row=row + 1, column=column + 1)
                        else:
                            tk.Label(routeRoot, text="a(" + stops.get("arrTime") + ")").grid(sticky=NESW, row=row + 1, column=column + 1)
                    else:
                        delay = misc.getDelay(stops)
                        tk.Label(routeRoot, text="a" + stops.get("arrTime") + delay).grid(sticky=NESW, row=row + 1, column=column + 1)
                else:
                    tk.Label(routeRoot, text="(" + stops.get("depTime") + ")").grid(sticky=NESW, row=row + 1, column=column + 1)
            else:
                delay = misc.getDelay(stops)
                tk.Label(routeRoot, text=stops.get("depTime") + delay).grid(sticky=NESW, row=row + 1, column=column + 1)

        tk.Button(routeRoot, text="Karta", command= lambda: mapmaker.geometryBackEnd(route.get("GeometryRef").get("ref"), colour.get("fgColor"))).grid(column=0, columnspan=columns, sticky=NESW)

        tk.Button(routeRoot, text="Stäng", command=routeRoot.destroy).grid(column=0, columnspan=columns, sticky=NESW)

    def departuresMenu(self):
        self.clearFrame()
        BackButton(self).grid(row=0, column=0, columnspan=3, sticky=NESW)

        tk.Label(self.frame, text="Avgångar", font="bold").grid(row=1, column=0, columnspan=3, sticky=NESW)

        tk.Label(self.frame, text="Hållplats").grid(row=2, column=0, columnspan=1, sticky=NESW)
        stopbox = tk.Entry(self.frame)
        stopbox.grid(row=2, column=1, columnspan=1, sticky=NESW)
        tk.Button(self.frame, text="Rensa", command=lambda: stopbox.delete(0, tk.END)).grid(row=2, column=2, columnspan=1, sticky=NESW)

        tk.Label(self.frame, text="Tid").grid(row=3, column=0, columnspan=1, sticky=NESW)
        timebox = tk.Entry(self.frame)
        timebox.grid(row=3, column=1, columnspan=1, sticky=NESW)
        timebox.insert(tk.END, time.strftime("%H:%M"))

        tk.Label(self.frame, text="Datum").grid(row=4, column=0, columnspan=1, sticky=NESW)
        datebox = tk.Entry(self.frame)
        datebox.grid(row=4, column=1, columnspan=1, sticky=NESW)
        datebox.insert(tk.END, time.strftime("%Y-%m-%d"))

        tk.Button(self.frame, text="Nu", command=lambda: self.setNow(timebox, datebox)).grid(row=3, column=2, rowspan=2, sticky=NESW)

        tk.Button(self.frame, text="Sök", command=lambda: misc.dep(self, stopbox.get(), timebox.get(), datebox.get())).grid(
            row=5, column=0, columnspan=3, sticky=NESW)
        self.frame.bind("<Return>", lambda event: misc.dep(self, stopbox.get(), timebox.get(), datebox.get()))

        self.frame.mainloop()


    def printDepartures(self, departures, stopname, date, time_):
        self.clearFrame()
        BackButton(self).grid(row=0, column=0, columnspan=3, sticky=NESW)

        headline = tk.Label(self.frame, text=f'Avgångar från {stopname} {time_} {date}', pady=5, padx=10)
        headline.grid(row=1, column=0, columnspan=3, sticky=tk.E + tk.W)

        for i, departure in enumerate(departures):
            tk.Label(self.frame, text=departure.get("sname"), bg=departure.get("fgColor"),
                  fg=departure.get("bgColor")).grid(row=i + 2, column=0, sticky=NESW)
            tk.Button(self.frame, text=departure.get("direction"),
                   command=lambda departure=departure: self.displayRoute(departure.get("JourneyDetailRef").get("ref"))).grid(
                row=i + 2, column=1, sticky=tk.E + tk.W)
            if not departure.get("rtTime"):
                tk.Label(self.frame, text="ca " + departure.get("time")).grid(row=i + 2, column=2, sticky=NESW)
            else:

                delay = misc.getDelay(departure)

                tk.Label(self.frame, text=departure.get("time") + delay).grid(row=i + 2, column=2, sticky=NESW)

    def takeMeHomeMenu(self):
        pass

    

if __name__ == "__main__":        
	print("This file is only supposed to be used as a module.")
