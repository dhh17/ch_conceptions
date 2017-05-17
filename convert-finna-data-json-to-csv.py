#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import os

csvfile = open('finna-2017-05-17.csv', 'w')
#csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
csvwriter = csv.writer(csvfile)

csvwriter.writerow(["title", "geoLocations", "subjects", "images", "nonPresentAuthors", "year", "imageRights"])

for i in range(1,4016):
    filename = 'finna-data-2017-05-17/finna-'+str(i)+'.json'
    if os.path.isfile(filename):
        jsonfile = open(filename)
        data = json.load(jsonfile)
        jsonfile.close()

        #print filename

        for item in data['records']:
            title = ""
            if item.has_key("title"):
                title = item['title'].encode("utf-8")

            geoLocations = []
            for geoLocation in item['geoLocations']:
                geoLocations.append(geoLocation.encode("utf-8"))
            geoLocations = ", ".join(geoLocations)

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

            csvwriter.writerow([title, geoLocations, subjects, images, authors, year, rights])

csvfile.close()
