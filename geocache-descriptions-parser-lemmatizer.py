#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parses geocache GPX files, lemmatizes descriptions and comments of caches, and prints them in text files (one file / cache)

import os
import xml.etree.ElementTree as ET
import re
import requests

lemmatizer_url = "http://demo.seco.tkk.fi/las/baseform"
# might be a good idea to use ARPA with "cgen" parameter instead, though adds complexity (n-grams, hard to ensure the word order of the original text)

src_dir = "geocaches/"
dst_dir = "geocache-descriptions/"

if os.path.isdir(dst_dir):
    print "Destination dir (" + dst_dir + ") already exists. Please delete it in order not to override previous data."
    exit()

os.mkdir(dst_dir)

for file in os.listdir(src_dir):
    if file.endswith(".gpx"):
        tree = ET.parse(src_dir + file)
        root = tree.getroot()

        for cache in root.findall("{http://www.topografix.com/GPX/1/0}wpt"):

            texts = []
            cache_inner = cache.find("{http://www.groundspeak.com/cache/1/0/1}cache")
            #TODO: it seems that not all caches have descriptions (next line throws exception)
            texts.append(cache_inner.find("{http://www.groundspeak.com/cache/1/0/1}short_description").text.encode("utf-8"))
            texts.append(cache_inner.find("{http://www.groundspeak.com/cache/1/0/1}long_description").text.encode("utf-8"))

            for log in cache_inner.find("{http://www.groundspeak.com/cache/1/0/1}logs").findall("{http://www.groundspeak.com/cache/1/0/1}log"):
                texts.append(log.find("{http://www.groundspeak.com/cache/1/0/1}text").text.encode("utf-8"))

            for text in texts:
                text = re.sub('<[^<]+?>', '', text)
                sentences = text.split(".")
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence != "":
                        response = requests.post(lemmatizer_url, data={'text': sentence})
                        if response.status_code == 200:
                            try:
                                resp_json = response.json()
                            except ValueError:
                                print "Warning: Non-JSON response."
                                continue
                            if resp_json.has_key("locale") and resp_json.has_key("baseform"):
                                filename = cache.get("lat") + "_" + cache.get("lon") + ".txt"
                                locale = resp_json['locale']
                                if not os.path.isdir(dst_dir + locale):
                                    os.mkdir(dst_dir + locale)
                                file = open(dst_dir + locale + '/' + filename, 'a')
                                file.write(resp_json['baseform'].encode("utf-8") + ". ")
