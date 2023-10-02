import config
import requests
import gpxpy.gpx
from datetime import datetime

base_url = config.traccar_api_url
traccar_user = config.traccar_user
traccar_pass = config.traccar_pass
traccar_device_id = config.traccar_device_id

time_from = "2023-09-23T00:00:00Z"
time_to = "2023-09-24T23:59:59Z"
filename = "tracklog.gpx"

get_parameters = {"deviceId": traccar_device_id, "from": time_from, "to": time_to}
print (get_parameters)

resp = requests.get(base_url, params=get_parameters, auth=(traccar_user, traccar_pass))
# TODO: handle 401 exception
print (resp)

gps_points = resp.json()

gpx = gpxpy.gpx.GPX()
# Create first track in our GPX:
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)

# Create first segment in our GPX track:
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

for point in gps_points:
    dt = datetime.strptime(point["fixTime"], "%Y-%m-%dT%H:%M:%S.000+00:00")
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point["latitude"], point["longitude"], time=dt))

xml = gpx.to_xml()

with open(filename, "wt") as text_file:
    n = text_file.write(xml)
