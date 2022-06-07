#!/usr/bin/env python3
import requests
import datetime



ASTRONOMYAPI_ID="274af23c-bdba-43f1-a070-ca3f0377a3e2"
ASTRONOMYAPI_SECRET="05b361de9f15e8511b9b1b3245f8221d5f379736200796fc26dce2abba197ad54f366c557faeca620806ea121a459f88bc15760831630a6e74e621c359f0a22c39ad06507fd39579dd8fccb230698948b3ef0122f2f613bfd093046375fbdde94e91e0ef5f0b5a398f7ac6659dc40de3"
date = datetime.date.today()
datethirty = date.today() + datetime.timedelta(days=30)
# print(datethirty)

# time = datetime.time()

current_time = date.strftime("%H:%M:%S")
# print(time)

def get_observer_location():
    response = requests.get("http://ip-api.com/json/73.61.1.59")
    events = response.json()    #events has the lat long from requests above
    global latitude
    latitude = events["lon"]
    global longitude
    longitude = events["lat"]
    global city
    city = events["city"]
    global state
    state = events["regionName"]
        
    # print(f"My latitude is " + str(latitude))
    # print(f"My longitude is " +str(longitude))
    
    return {latitude}, {longitude}
get_observer_location()


payload = {"latitude" : latitude, "longitude" : longitude, "elevation" : "100", 
        "from_date" : date, "to_date" : datethirty, "time" : current_time}

def get_sun_position():
    
    date = datetime.datetime.now()
    astroresponse = requests.get('https://api.astronomyapi.com/api/v2/bodies/positions', params=payload, auth=(ASTRONOMYAPI_ID, ASTRONOMYAPI_SECRET))
    # print(astroresponse)   #connection to astronomy bodies
    astrotime = astroresponse.json()
    
    global sunazimuth
    sunazimuth = astrotime["data"]["table"]["rows"][0]["cells"][1]["position"]["horizonal"]["azimuth"]["string"]
    global sunlocation
    sunlocation = astrotime["data"]["table"]["rows"][0]["cells"][1]["position"]["horizonal"]["altitude"]["string"]
    # print("The Sun's azimuth is " + sunazimuth)
    # print("The Sun's altitude is " + sunlocation)

    return {sunazimuth}, {sunlocation}

get_sun_position()


def print_position():
    print("You are currently connecting from " + city + ", " + state + ". Your Longigude is " + str(longitude) + " and you Latitude is " + str(latitude))
    print("The Sun is currently at: " + sunazimuth + " and " + sunlocation + " in the sky")

print_position()

