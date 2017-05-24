#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import codecs
import json
import csv
import os

POINT = 1
POLYGON = 2
LINESTRING = 3

FILE_SUFFIX = "2017-05-19"

csvpointsfile = open('finna-points-' + FILE_SUFFIX + '.csv', 'w')
csvpolygonsfile = open('finna-polygons-' + FILE_SUFFIX + '.csv', 'w')
csvlinestringsfile = open('finna-linestrings-' + FILE_SUFFIX + '.csv', 'w')

#TODO: add BOM to file for Excel? (the next line makes everything scramble at least in macOS's Excel 2011)
#csvpointsfile.write(codecs.BOM_UTF16_LE)

csvpointswriter = csv.writer(csvpointsfile)
csvpolygonswriter = csv.writer(csvpolygonsfile)
csvlinestringswriter = csv.writer(csvlinestringsfile)

csvpointswriter.writerow(["title", "lat", "long", "subjects", "images", "nonPresentAuthors", "year", "imageRights", "buildings"])
csvpolygonswriter.writerow(["title", "polygon", "subjects", "images", "nonPresentAuthors", "year", "imageRights", "buildings"])
csvlinestringswriter.writerow(["title", "linestring", "subjects", "images", "nonPresentAuthors", "year", "imageRights", "buildings"])

for file in os.listdir("finna-data-"+FILE_SUFFIX):
    if file.endswith(".json"):
        filename = 'finna-data-'+FILE_SUFFIX+'/' + file
        if os.path.isfile(filename):
            jsonfile = open(filename)
            data = json.load(jsonfile)
            jsonfile.close()

            for item in data['records']:
                title = ""
                if item.has_key("title"):
                    title = item['title'].encode("utf-8").replace("\n", " ")

                geoLocation = ""
                point = ""
                lat = ""
                lng = ""
                polygon = ""
                linestring = ""
                geoLocationType = 0
                for geoLocation in item['geoLocations']:
                    if geoLocation.startswith("POINT"):
                        point = geoLocation.encode("utf-8")
                    elif geoLocation.startswith("POLYGON"):
                        polygon = geoLocation.encode("utf-8")
                    elif geoLocation.startswith("LINESTRING"):
                        linestring = geoLocation.encode("utf-8")
                if point != "":
                    point = point.replace("POINT", "").replace("(", "").replace(")", "").strip().split(" ")
                    lat = point[1]
                    lng = point[0]
                    geoLocationType = POINT
                elif polygon != "":
                    geoLocation = polygon
                    geoLocationType = POLYGON
                elif linestring != "":
                    geoLocation = linestring
                    geoLocationType = LINESTRING
                if geoLocation == "":
                    print "Error: no geoLocation: " + filename

                subjects = []
                if item.has_key("subjects"):
                    for subject in item['subjects']:
                        subjects.append(subject[0].encode("utf-8"))
                    subjects = ", ".join(subjects)

                images = []
                if item.has_key("images"):
                    for image in item['images']:
                        images.append("http://finna.fi"+image.encode("utf-8"))
                    images = ", ".join(images)

                authors = []
                if item.has_key("nonPresenterAuthors"):
                    for author in item['nonPresenterAuthors']:
                        authors.append(author['name'].encode("utf-8"))
                authors = ", ".join(authors)

                year = ""
                if item.has_key("year"):
                    year = item['year']

                rights = ""
                if item.has_key("imageRights"):
                    rights = item['imageRights']['copyright'].encode("utf-8")

                buildings = []
                for building in item['buildings']:
                    buildings.append(building['value'].encode("utf-8"))
                buildings = ", ".join(buildings)

                if geoLocationType == POINT:
                    csvpointswriter.writerow([title, lat, lng, subjects, images, authors, year, rights, buildings])
                elif geoLocationType == POLYGON:
                    csvpolygonswriter.writerow([title, geoLocation, subjects, images, authors, year, rights, buildings])
                elif geoLocationType == LINESTRING:
                    csvlinestringswriter.writerow([title, geoLocation, subjects, images, authors, year, rights, buildings])

csvpointsfile.close()
csvpolygonsfile.close()
csvlinestringsfile.close()
