#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import requests

API_KEY = ""

flickr_api_base_url = "https://api.flickr.com/services/rest/"
flickr_url = flickr_api_base_url + "?method=flickr.photos.search&format=json&nojsoncallback=1&api_key=" + API_KEY + "&radius=0.05"

src_file = open('suomenlinna-objects.csv')
dst_file = open('suomenlinna-objects-flickr-counts.csv', 'w')

csvreader = csv.reader(src_file)
csvwriter = csv.writer(dst_file)

line = 0
for row in csvreader:
    line = line + 1
    if line == 1:
        row.append("Flickr_count")
        csvwriter.writerow(row)
    else:
        response = requests.get(flickr_url + "&lat=" + row[3].replace(",", ".") + "&lon=" + row[2].replace(",", "."))
        if response.status_code == 200:
            resp_json = response.json()
            flickr_count = resp_json['photos']['total']
            csvwriter.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],flickr_count])

src_file.close()
dst_file.close()
