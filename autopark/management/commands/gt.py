from pprint import pprint

import geopy

# import geopy
# import numpy as np
from geopy.distance import geodesic, distance
from django.contrib.gis.geos import MultiPoint, Point
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from autopark.models import Vehicle, Enterprise, Brand, Driver, Enterprise, Routes
import openrouteservice
import json
import math

from autopark.utils import next_point


class Command(BaseCommand):
    help = "add treck"

    def add_arguments(self, parser):
        parser.add_argument("car", type=int, help="Car id")
        parser.add_argument("treck_len", type=int, help="treck lenght")
        parser.add_argument("max_speed", type=int, help="Car max speed")
        parser.add_argument("spread", type=int, help="spread num")

    def handle(self, car, max_speed, spread, *args, **kwargs):
        routes = Routes.objects.filter(car_id=car)
        def next_p():
            for route in routes:
                route.max_speed = max_speed
                next_point(route)
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(next_point, 'interval', seconds=10)
scheduler.start()
scheduler.add_job(run_for_minute, 'interval', seconds=60)
        # x_start, y_start = (8.34234, 48.23424)
        # x_finish, y_finish = (8.34423, 48.26424)
        # car = Vehicle.objects.filter(pk=car).first()
        #
        # if car is None:
        #     raise CommandError("Такой  машины не существует")
        #
        # faker = Faker()
        # print(faker.longitude(), faker.latitude())
        # # print(type(faker.longitude()))
        # route = Routes.objects.create(
        #     car=car,
        #     route=MultiPoint(
        #         Point(x=float(faker.longitude()), y=float(faker.latitude()))
        #     ),
        #     start=f"{x_start};{y_start}",
        #     finish=f"{x_finish};{y_finish}",
        # )
        # route.points.create(point=f"{x_start};{y_start}")
