#!/bin/bash

# Fetch all photographs which have geolocation from Finna API (401 031 photos at the time of writing).
# Include the following information:
# - title
# - coordinates (point, polygon, etc.)
# - subjects
# - author
# - year
# - link to image file

for i in {1..4011};
do
  curl -o finna-$i.json -X GET --header 'Accept: application/json' 'https://api.finna.fi/api/v1/search?type=AllFields&field%5B%5D=title&field%5B%5D=geoLocations&field%5B%5D=subjects&field%5B%5D=images&field%5B%5D=nonPresenterAuthors&field%5B%5D=year&filter%5B%5D=%7B%21geofilt+sfield%3Dlocation_geo+pt%3D65.01650627048231%2C23.994140625000004+d%3D616.5783931055392%7D%3A%22%22&filter%5B%5D=format%3A%220%2FImage%2F%22&sort=relevance%2Cid%20asc&limit=100&lng=fi&page='$i
done