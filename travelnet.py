#!/usr/bin/python
from __future__ import print_function
from tabulate import tabulate
from collections import defaultdict
import os
import csv

from math import cos,radians,sin,pow,asin,sqrt

def distance(src_airport,lat1, long1, dest_airport,lat2, long2):
    radius = 3959 # radius of the earth in miles, roughly https://en.wikipedia.org/wiki/Earth_radius

    # Lat,long are in degrees but we need radians
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    long1 = radians(long1)
    long2 = radians(long2)

    dlat = lat2-lat1
    dlon = long2-long1

    a = pow(sin(dlat/2),2) + cos(lat1)*cos(lat2)*pow(sin(dlon/2),2)
    distance = 2 * radius * asin(sqrt(a))

    return int(round(distance))

lats = {}
longs = {}
data = defaultdict(list)
totals = defaultdict(list)

# Read the airports.dat file to populate the latts and longs Maps
f = open("airports.dat")
for row in csv.reader(f):
    airport_id = row[4]
    lats[airport_id] = float(row[6])
    longs[airport_id] = float(row[7])

# Read the Travelnet export.  Go to Travelnet, save travel history as a CSV

f = open("history.csv")

for row in csv.reader(f):

    # Skip any row that doesn't start with a number (each trip always starts with your PPR number)
    if row[0][0].isdigit():
        pass_rider = row[1]
        travel_date = row[4]
        travel_month, travel_date, travel_year = travel_date.split("/")

        travel_day = row[4]
        city_pair = row[5]
        source_airport, dest_airport = city_pair.split("/")

        # Travelnet exports the trip as origin and destination (ie: RDU/ATL)
        if source_airport in lats and dest_airport in lats:
            source_lat = lats[source_airport]
            source_long = longs[source_airport]
            dest_lat = lats[dest_airport]
            dest_long = longs[dest_airport]
            miles_traveled = distance(source_airport, source_lat,source_long,dest_airport, dest_lat,dest_long)

            if miles_traveled < 500:
                miles_earned = 500
            else:
                miles_earned = miles_traveled

            #trip = [travel_date, source_airport, dest_airport, miles_traveled, miles_earned]
            trip = {
                "travel_date": travel_day,
                "travel_year": travel_year,
                "source_airport": source_airport,
                "dest_airport": dest_airport,
                "miles_traveled": miles_traveled,
                "miles_earned": miles_earned
            }

            data[pass_rider].append(trip)

#print tabulate(trips, headers=table_headers, tablefmt='orgtbl')
#print("Date\tFrom\tTo\tActual Miles Flown\tMQMs")
#data = sorted(data, key=lambda data: data['pass_rider'], reverse=False)

for pass_rider in data.keys():
    print ("Pass Rider: ", pass_rider)
    table_headers = ["Skymiles Year", "Date", "From", "To", "Actual Miles Flown", "MQMs"]
    print (*table_headers, sep='\t\t')

    # Initialize the pass rider's mileage
    miles = {
        "total_miles_traveled": 0,
        "total_miles_earned": 0
    }
    totals[pass_rider]= miles

    for trip in data[pass_rider]:
        #print (trip[0],trip[1],trip[2],trip[3], sep='\t')
        print ("20"+trip['travel_year'], trip['travel_date'],trip['source_airport'],trip['dest_airport'],trip['miles_traveled'],trip['miles_earned'], sep='\t\t')

        miles = {
            "total_miles_traveled": totals[pass_rider]['total_miles_traveled'] + trip['miles_traveled'],
            "total_miles_earned": totals[pass_rider]['total_miles_earned'] + trip['miles_earned']
        }

        totals[pass_rider] = miles
    print ("")

print ("")

table_headers = ["Pass Rider", "Miles Traveled", "MQMs Earned"]
print (*table_headers, sep='\t\t')

for pass_rider in totals.keys():
    print(pass_rider, totals[pass_rider]['total_miles_traveled'], totals[pass_rider]['total_miles_earned'], sep='\t\t')

#print ("")
#print ("Total Distance Traveled (miles): ", "{:,}".format(total_miles_traveled))
#print ("Total MQMs: ", "{:,}".format(total_miles_earned))

#print ("")
#print ("--------------------------------------------------")
