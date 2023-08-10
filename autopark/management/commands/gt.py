from pprint import pprint

from django.contrib.gis.geos import MultiPoint, Point
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from autopark.models import Vehicle, Enterprise, Brand, Driver, Enterprise, Routes
import openrouteservice
import json


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

    distance = route.max_speed * 10

    client = openrouteservice.Client(
        key="5b3ce3597851110001cf6248017011c8bff04d5096aae5b5c8f03c15"
    )
    routes = client.directions(**data)
    routes.points.create(point=point)

    pprint(routes)
