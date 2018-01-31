import json
import time

import requests

class APIRequest():
    def __init__(self):
        # Read saved token
        with open("C:/Edvin/Vasttrafik/token.txt") as f:
            token = f.read()
            f.close()
        placeholder = "Bearer " + token
        self.headers = {"Authorization": placeholder}

    def getPlan(self, fr, to, time_=time.strftime("%H:%M"), date=time.strftime("%Y-%m-%d"), arr=False, sChTime=False):
        try:
            hour, minute = time_.split(":")
        except ValueError:
            try:
                hour, minute = time_.split(".")
            except ValueError:
                print("Could not interpret.")
                return

        url = "https://api.vasttrafik.se/bin/rest.exe/v2/trip?originId=" + fr + "&destId=" + to + "&date=" + date + "&time=" + hour + "%3A" + minute + "&format=json&needGeo=1"
        if arr:
            url += "&searchForArrival=1"
        if sChTime:
            url += "&disregardDefaultChangeMargin=1"
        print(url)

        # Http request trip
        r = requests.get(url, headers=self.headers)
        print("Status code:", r.status_code)

        # if token is invalid
        if r.status_code == 401:
            self.renewToken()

            # Do http request again with new token
            r = requests.get(url, headers=self.headers)
            print("Status code:", r.status_code)

        # Save departures to file
        file = open("trip.json", "w")
        json.dump(r.json(), file, indent=4, ensure_ascii=True)
        file.close()

        # Return
        trips = r.json().get("TripList").get("Trip")
        return trips

    def renewToken(self):

        # Send http request for new token
        header = {"Content-Type": "application/x-www-form-urlencoded",
                  "Authorization": "Basic M0xwNmx1SkxNczBEa1RBQVJDZkxjc1dhbzlVYToxM1REOF9vUHZ5ZTlhMVoyVTBmZHF5Nm5oeU1h"}
        p = requests.post("https://api.vasttrafik.se/token?grant_type=client_credentials&scope=device_0",
                          headers=header)
        text = p.json()

        token = text.get("access_token")

        # save token for use next time
        with open("C:/Edvin/Vasttrafik/token.txt", "w") as f:
            f.write(token)
            f.close()
        placeholder = "Bearer " + token
        self.headers = {"Authorization": placeholder}

    def getDepartures(self, stop, date=time.strftime("%Y-%m-%d"), time_=time.strftime("%H:%M"), arr=False, direction=None):
        try:
            hour, minute = time_.split(":")
        except ValueError:
            try:
                hour, minute = time_.split(".")
            except ValueError:
                print("Could not interpret.")
                return

        url = "https://api.vasttrafik.se/bin/rest.exe/v2/departureBoard?id=" + stop + "&date=" + date + "&time=" + hour + "%3A" + minute + "&format=json"
        if arr:
            url.replace("departureBoard", "arrivalBoard")
            
        if direction != None:
            url += "&direction=" + direction

        # Http request departure board
        r = requests.get(url, headers=self.headers)
        print("Status code:", r.status_code)
        if r.status_code == 401:
            self.renewToken()
            # Do http request again with new token

            r = requests.get(url, headers=self.headers)
            print("Status code:", r.status_code)
            
            
        #Save to file
        with open("deps.json", "w") as f:
            json.dump(r.json(), f, indent=4)
            f.close()
        

        if not arr:
            # Return departures
            departures = r.json().get("DepartureBoard").get("Departure")
            return departures
        else:
            # Return arrivals
            arrivals = r.json().get("ArrivalBoard").get("Arrival")
            return arrivals

    def findStop(self, inp):
        # HTTP Request
        url = "https://api.vasttrafik.se/bin/rest.exe/v2/location.name?input=" + inp + "&format=json"
        r = requests.get(url, headers=self.headers)
        print("Status code:", r.status_code)

        # If token is invalid
        if r.status_code == 401:
            self.renewToken()
            r = requests.get(url, headers=self.headers)

        with open("stops.txt", "w") as f:
            json.dump(r.json(), f, indent=4)
            f.close()

        # Return dict of stops.
        if r.status_code == 403:
            print("HTTP ERROR 403 FORBIDDEN")
            raise TypeError("HTTP Error 403 Forbidden")

        stops = r.json().get("LocationList").get("StopLocation")

        # Get stop ID and name
        try:
            stop = stops[0].get("id")
            stopname = stops[0].get("name")
        except KeyError:
            # If only received 1 stop
            stop = stops.get("id")
            stopname = stops.get("name")
        except TypeError:
            print("No stop found.")
            return 0, 0

        return stop, stopname

    def getRoute(self, url, v2=False):
        # HTTP Request
        if v2:
            r = requests.get(url, headers=self.headers)
        else:
            r = requests.get(url)
        print("Status code:", r.status_code)

        # If token is invalid
        if r.status_code == 401:
            self.renewToken()
            r = requests.get(url, headers=self.headers)

        # Save to file
        f = open("journey.json", "w")
        json.dump(r.json(), f, indent=4)
        f.close()

        # Return
        stops = r.json().get("JourneyDetail")
        return stops

    def geometry(self, ref):
        if "/v1/" not in ref:
            r = requests.get(ref, headers=self.headers)

            if r.status_code == 401:
                # If token is invalid
                self.renewToken()
                r = requests.get(ref, headers=self.headers)
        else:
            r = requests.get(ref)

        if r.status_code != 200:
            raise ValueError("Http error: " + str(r.status_code))

        with open("geo.json", "w") as f:
            json.dump(r.json(), f, indent=4)

        geo = r.json().get("Geometry").get("Points").get("Point")
        return geo