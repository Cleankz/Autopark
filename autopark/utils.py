import math
from math import atan2, cos, sin, radians

import openrouteservice

from autopark.models import Routes


def calc_bearing(lat1, long1, lat2, long2):
    # Convert latitude and longitude to radians
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)

    # Calculate the bearing
    bearing = math.atan2(
        math.sin(long2 - long1) * math.cos(lat2),
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1),
    )

    # Convert the bearing to degrees
    bearing = math.degrees(bearing)

    # Make sure the bearing is positive
    bearing = (bearing + 360) % 360

    return bearing


def calculate_coordinate_between_points(start_coord, end_coord, distance):
    lat1, lon1 = start_coord
    lat2, lon2 = end_coord

    azimuth = atan2(
        sin(radians(lon2 - lon1)) * cos(radians(lat2)),
        cos(radians(lat1)) * sin(radians(lat2))
        - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(lon2 - lon1)),
    )

    new_latitude = lat1 + (distance * cos(azimuth)) / 111000
    new_longitude = lon1 + (distance * sin(azimuth)) / (111000 * cos(radians(lat1)))

    return new_latitude, new_longitude


def next_point(rout: Routes):
    if not rout.points.exists():
        x_start, y_start = [float(x) for x in rout.start.split(";")]
        rout.points.create(point=f"{x_start};{y_start}")
        return
    x_start, y_start = [float(x) for x in rout.points.first().point.split(";")]
    x_finish, y_finish = [float(x) for x in rout.finish.split(";")]

    data = {
        # "maximum_speed": route.max_speed,
        "preference": "fastest",
        "coordinates": ((x_start, y_start), (x_finish, y_finish)),
    }

    distance_1 = rout.max_speed * 360 * 0.1

    client = openrouteservice.Client(
        key="5b3ce3597851110001cf6248017011c8bff04d5096aae5b5c8f03c15"
    )
    routes = client.directions(**data)
    bbox = routes["routes"][0]["bbox"]

    point = calculate_coordinate_between_points(bbox[0:2], bbox[2:4], distance_1)
    rout.points.create(point=f"{point[0]};{point[1]}")
