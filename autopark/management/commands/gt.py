from django.contrib.gis.geos import MultiPoint, Point
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from autopark.models import Vehicle, Enterprise, Brand,Driver,Enterprise, Routes
import openrouteservice
import json
class Command(BaseCommand):
    help = 'add treck'

    def add_arguments(self,parser):
        parser.add_argument('car', type=int, help='Car id')
        parser.add_argument('treck_len', type=int, help='treck lenght')
        parser.add_argument('max_speed', type=int, help='Car max speed')
        parser.add_argument('spread', type=int, help='spread num')
    def handle(self,car, *args,treck_len,max_speed,spread, **kwargs):
        try:
            car = Vehicle.objects.get(pk=car)

        except Vehicle.DoesNotExist:
            raise CommandError('Такой  машины не существует')
        faker = Faker()
        print(faker.longitude(),faker.latitude())
        print(type(faker.longitude()))
        route = Routes.objects.create(car=car,route = MultiPoint(Point(x=float(faker.longitude()), y=float(faker.latitude()))))
        for i in range(10):
            point = Point(x=float(faker.longitude()), y=float(faker.latitude()))
            route.route.append(point)

        route.save()
        print(route)
        coords = ((8.34234,48.23424),(8.34423,48.26424))
        # for p in route.route:
        #     coords.append({'longitude':p.y,'latitude':p.x})
        # json_points = json.dumps(coords)
        # # options = {'maximum_speed': max_speed}
        # print(json_points)
        options = {
        'profile': 'driving-car',
        "maximum_speed": 100,
        }
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
        client = openrouteservice.Client(key='5b3ce3597851110001cf6248017011c8bff04d5096aae5b5c8f03c15')
        routes = client.directions(coordinates = coords, options = options)
        print(routes)




