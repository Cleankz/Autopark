from django.contrib.gis.geos import MultiPoint, Point
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from autopark.models import Vehicle, Enterprise, Brand,Driver,Enterprise, Routes
import openrouteservice
class Command(BaseCommand):
    help = 'add treck'

    def add_arguments(self,parser):
        parser.add_argument('car', type=int, help='Car id')
    def handle(self,car, *args, **kwargs):
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
     coords = ((8.34234, 48.23424), (8.34423, 48.26424))

    client = openrouteservice.Client(key='5b3ce3597851110001cf6248170095f78f3641c594c261ec409')
    routes = client.directions(coords)

    print(routes)




