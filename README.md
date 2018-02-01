# VT_Avg - Västtrafik avgångsapp

### To use the app
To be able to use it you need your own authentication details placed in a file called 'auth.txt'. The contents of the file should be 'Basic [base64 encoded details from the dev portal]'.
https://developer.vasttrafik.se/portal/#/


### What the files do

#### viewport.py
Main file which coordinates everything. This is the file you run.

#### APIRequest.py
Handles all communication between the app and the Västtrafik API.

#### mapmaker.py
Holds one class for displaying routes in a google map.
