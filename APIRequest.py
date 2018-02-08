# coding: utf-8

import json
import time

import requests

# Class handling all communication with the API
class APIRequest():
    def __init__(self):
        # Read saved token
        try:
            with open("tempfiles/token.txt") as f:
                token = f.read()
                f.close()
            # Save token for future use
            placeholder = "Bearer " + token
            self.headers = {"Authorization": placeholder}
        except FileNotFoundError:
            self.renewToken()

    # Getting a trip plan
    def getPlan(self, fr, to, time_=time.strftime("%H:%M"), date=time.strftime("%Y-%m-%d"), arr=False, smallChangeTime=False):
        try:
            hour, minute = time_.split(":")
        except ValueError:
            try:
                hour, minute = time_.split(".")
            except ValueError:
                print("Could not interpret.")
                return

        # URL for the API
        url = f'https://api.vasttrafik.se/bin/rest.exe/v2/trip?originId={fr}&destId={to}&date={date}&time={hour}%3A{minute}&format=json&needGeo=1'
        if arr:
            url += "&searchForArrival=1"
        if smallChangeTime:
            url += "&disregardDefaultChangeMargin=1"

        # Http request trip
        r = requests.get(url, headers=self.headers)
        print("Status code:", r.status_code)

        # If token is invalid
        if r.status_code == 401:
            self.renewToken()

            # Do http request again with new token
            r = requests.get(url, headers=self.headers)
            print("Status code:", r.status_code)

        # Save departures to file
        file = open("tempfiles/trip.json", "w")
        json.dump(r.json(), file, indent=4, ensure_ascii=True)
        file.close()

        # Return
        trips = r.json().get("TripList").get("Trip")
        return trips

    # Renew token if invalid or nonexistent
    def renewToken(self):
        # Get the codes necessary for renewal
        with open("auth.txt", "r") as file:
            auth = file.read()
            file.close()

        # Send http request for new token
        header = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": auth}
        p = requests.post("https://api.vasttrafik.se/token?grant_type=client_credentials&scope=device_0", headers=header)
        text = p.json()

        token = text.get("access_token")

        # Save token for use next time
        with open("tempfiles/token.txt", "w") as file:
            file.write(token)
            file.close()
        placeholder = "Bearer " + token
        self.headers = {"Authorization": placeholder}

    # Get departures from stop
    def getDepartures(self, stop, date=time.strftime("%Y-%m-%d"), time_=time.strftime("%H:%M"), arr=False, direction=None):
        try:
            hour, minute = time_.split(":")
        except ValueError:
            try:
                hour, minute = time_.split(".")
            except ValueError:
                print("Could not interpret.")
                return

        # Base url
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
        with open("tempfiles/deps.json", "w") as f:
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

    # Find stop from input
    def findStop(self, inp):
        # HTTP Request
        url = f'https://api.vasttrafik.se/bin/rest.exe/v2/location.name?input={inp}&format=json'
        r = requests.get(url, headers=self.headers)
        print("Status code:", r.status_code)

        # If token is invalid
        if r.status_code == 401:
            self.renewToken()
            r = requests.get(url, headers=self.headers)

        # Save json file for easier viewing
        with open("tempfiles/stops.json", "w") as file:
            json.dump(r.json(), file, indent=4)
            file.close()

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

    # Get a line's departure (route, journey, whatever)
    def getRoute(self, url):
        # HTTP Request
        
        r = requests.get(url, headers=self.headers)
        print("Status code:", r.status_code)

        # If token is invalid
        if r.status_code == 401:
            self.renewToken()
            r = requests.get(url, headers=self.headers)

        # Save to file
        file = open("tempfiles/journey.json", "w")
        json.dump(r.json(), file, indent=4)
        file.close()

        # Return
        stops = r.json().get("JourneyDetail")
        return stops

    # Get polylines for maps
    def geometry(self, ref):
        # HTTP request
        r = requests.get(ref, headers=self.headers)

        if r.status_code == 401:
            # If token is invalid
            self.renewToken()
            r = requests.get(ref, headers=self.headers)
    
        print(f'Status code: {r.status_code}')

        if r.status_code != 200:
            raise ValueError("Http error: " + str(r.status_code))

        # Save json for easier viewing
        with open("tempfiles/geo.json", "w") as file:
            json.dump(r.json(), file, indent=4)

        # Return dict of results
        geo = r.json().get("Geometry").get("Points").get("Point")
        return geo

if __name__ == "__main__":        
	print("This file is only supposed to be used as a module.")