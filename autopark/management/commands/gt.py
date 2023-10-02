from django.core.management.base import BaseCommand, CommandError
from autopark.models import Vehicle, Enterprise, Brand, Driver, Enterprise, Routes

from autopark.utils import next_point

import time


class Command(BaseCommand):
    help = "add treck"

    def add_arguments(self, parser):
        parser.add_argument("car", type=int, help="Car id")
        parser.add_argument("treck_len", type=int, help="treck lenght")
        parser.add_argument("max_speed", type=int, help="Car max speed")
        parser.add_argument("spread", type=int, help="spread num")

    def handle(self, car, max_speed, treck_len, spread, *args, **kwargs):
        routes = Routes.objects.filter(car_id=car)
        start = time.time()
        while time.time() - start < 60:
            time.sleep(10)
            for route in routes:
                route.max_speed = max_speed
                route.distance = treck_len
                route.step = spread
                next_point(route)
