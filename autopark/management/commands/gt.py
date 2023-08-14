from pprint import pprint

import geopy
import numpy as np
from geopy.distance import geodesic, distance
from django.contrib.gis.geos import MultiPoint, Point
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from autopark.models import Vehicle, Enterprise, Brand, Driver, Enterprise, Routes
import openrouteservice
import json
import math


class Command(BaseCommand):
    help = "add treck"

    def add_arguments(self, parser):
        parser.add_argument("car", type=int, help="Car id")
        parser.add_argument("treck_len", type=int, help="treck lenght")
        parser.add_argument("max_speed", type=int, help="Car max speed")
        parser.add_argument("spread", type=int, help="spread num")

    def handle(self, car, treck_len, max_speed, spread, *args, **kwargs):
        x_start, y_start = (8.34234, 48.23424)
        x_finish, y_finish = (8.34423, 48.26424)
        car = Vehicle.objects.filter(pk=car).first()

        if car is None:
            raise CommandError("Такой  машины не существует")

        faker = Faker()
        print(faker.longitude(), faker.latitude())
        print(type(faker.longitude()))
        route = Routes.objects.create(
            car=car,
            route=MultiPoint(
                Point(x=float(faker.longitude()), y=float(faker.latitude()))
            ),
            start=f"{x_start};{y_start}",
            finish=f"{x_finish};{y_finish}",
        )
        route.points.create(point=f"{x_start};{y_start}")
        next_point(route)
        # for i in range(10):
        #     point = Point(x=float(faker.longitude()), y=float(faker.latitude()))
        #     route.route.append(point)

        # route.save()
        # print(route)
        # coords = ((x_start, y_start), (x_finish, y_finish))
        # for p in route.route:
        #     coords.append({'longitude':p.y,'latitude':p.x})
        # json_points = json.dumps(coords)
        # # options = {'maximum_speed': max_speed}
        # print(json_points)
        # options = {
        # "maximum_speed": 100,
        # }
        # parameters = {
        # # 'spacing': 100,
        # 'coordinates': coords,
        # 'preference': 'fastest',
        # 'profile': 'driving-car',
        # 'units': 'km',
        # 'language': 'ru',
        # # "maximum_speed": max_speed,
        # # 'spacing': spread,
        # # 'spread': spread,
        # # 'distance_limit': treck_len,
        # }


def next_point(route: Routes):
    x_start, y_start = [float(x) for x in route.points.first().point.split(";")]
    x_finish, y_finish = [float(x) for x in route.finish.split(";")]

    data = {
        # "maximum_speed": route.max_speed,
        "preference": "fastest",
        "coordinates": ((x_start, y_start), (x_finish, y_finish)),
    }

    distance_1 = route.max_speed * 360 * 0.1

    client = openrouteservice.Client(
        key="5b3ce3597851110001cf6248017011c8bff04d5096aae5b5c8f03c15"
    )
    routes = client.directions(**data)
    bbox = routes["routes"][0]["bbox"]
    print(type(bbox[0]))
    # distance = geopy.distance.geodesic(bbox[0:2], bbox[2:4]).km
    point = geodesic(bbox[0:2], bbox[2:4]).destination(
        point=geopy.Point(bbox[0:2]), distance=distance, bearing=calc_bearing(*bbox)
    )
    # x = np.linspace(bbox[0],bbox[1],10)
    # y = np.linspace(bbox[2],bbox[4],10)
    # point = distance.interpolate(bbox[0:2], bbox[2:4])
    print(distance_1)

    print("POINT", point)

    # print(routes["routes"][0]["bbox"])
    # y =
    # point = f"{x};{y}"
    # routes.points.create(point=point)

    pprint(routes)


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
