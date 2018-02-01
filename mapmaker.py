# coding: utf-8

import os

import webbrowser

import APIRequest

class GeometryDoc():
    def __init__(self):
        self.polys = 0
        self.markers = 0
        self.document = """<!DOCTYPE html>
                       <html>
                        <head>
                        <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                        <meta charset="utf-8">
                        <title>Karta</title>
                        <style>
                        /* Always set the map height explicitly to define the size of the div
                        * element that contains the map. */
                        #map {
                        height: 100%;
                        }
                        /* Optional: Makes the sample page fill the window. */
                        html, body {
                        height: 100%;
                        margin: 0;
                        padding: 0;
                        }
                        </style>
                        </head>
                        <body>
                        <div id="map"></div>
                        <script>

                          function initMap() {
                            var map = new google.maps.Map(document.getElementById('map'), {
                              zoom: 10,
                              center: {lat: 57.7, lng: 12},
                              mapTypeId: 'roadmap'
                            });
                            
                            var image = 'https://hydra-media.cursecdn.com/simcity.gamepedia.com/c/cd/Bus_stop.png?version=25cdaa09d7415c963ccc7c1af1cf819a'
                            var image0 = {url: 'https://hydra-media.cursecdn.com/simcity.gamepedia.com/c/cd/Bus_stop.png?version=25cdaa09d7415c963ccc7c1af1cf819a', 
                                         size: new google.maps.Size(20, 32)}
                            var name = 'Hållplats'

                            //NEW
                            
                          }
                        </script>
                        <script async defer
                        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCoLm181B8i5rccrfuuw7YtynsvFzbO6Vk&callback=initMap">
                        </script>
                      </body>
                    </html>"""
                    
                    
    def addPoly(self, points, colour):
        #print(points)
        document = "var route" + str(self.polys) + """ = [];
                            var flightPath""" + str(self.polys) + """ = new google.maps.Polyline({
                              path: route""" + str(self.polys) + """,
                              geodesic: true,
                              strokeColor: '#FF0000',
                              strokeOpacity: 1.0,
                              strokeWeight: 4
                            });

                            flightPath""" + str(self.polys) + """.setMap(map);
                            
                            //NEW"""
                            
        document = document.replace(" = []", " = " + str(points).replace("},", "},\n").replace("'", "").replace('"', ""))
        document = document.replace("lon:", "lng:")
        
        document = document.replace("strokeColor: '#FF0000'", "strokeColor: '" + colour + "'")
        
        self.document = self.document.replace("//NEW", document)
        self.polys += 1
        
        #print(self.document)
        self.save()
        
    def addMarker(self, points):
        if type(points) != dict:
            raise TypeError(f'Expected dict, {str(type(points))} received.')
            
        # print("Adding marker")
        document = "var point" + str(self.markers) + "= " + str(points) + """
                var marker""" + str(self.markers) + """ = new google.maps.Marker({
                    position: point""" + str(self.markers) + """,
                    icon: image,
                    title: name,
                    map: map
                });
                
                //NEW"""
                
        document = document.replace("'lon'", "lng").replace("'", "").replace('"', "")
        
        self.document = self.document.replace("//NEW", document)
        self.markers += 1
        self.save()
        
    def save(self):
        with open("tempfiles/document.html", "w") as file:
            file.write(self.document)
            file.close()
        # print("saved")

def geometryBackEnd(ref, colour=None):
    document = GeometryDoc()
    if type(ref) == list:
        for item in ref:
            geoRef = item.get("GeometryRef").get("ref")
            points = APIRequest.APIRequest().geometry(geoRef)
            
            colour = item.get("fgColor")
            if colour is None: colour = "#00FF00"
            
            document.addPoly(points, colour)
            document.addMarker(points[0])
        document.addMarker(points[-1])
    
    else:
        points = APIRequest.APIRequest().geometry(ref)
        document.addPoly(points, colour)
        document.addMarker(points[0])
        document.addMarker(points[-1])

    folder = os.path.dirname(__file__).replace("\\", "/")
    path = f'file:///{folder}/tempfiles/document.html'
    webbrowser.open(path)

if __name__ == "__main__":        
	print("This file is only supposed to be used as a module.")
