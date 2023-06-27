from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

from autopark.models import Vehicle, Enterprise, Brand
import random

class Command(BaseCommand):
    help = 'Add vehicle'


    def add_arguments(self, parser):
        parser.add_argument('enterprise', nargs='+', type=str,help='Enterprise name')
        parser.add_argument('num_car', type=int)

    def handle(self, *args, **kwargs):
        num_car = kwargs['num_car']
        enterprises = kwargs['enterprise']
        own = ''

        # for enterprise in enterprises:
        #     try:
        #         own = Enterprise.objects.filter(name=enterprise)
        #     except Vehicle.DoesNotExist:
        #         raise CommandError(f'Enterprise with name  does not exist')
        for j in range(len(enterprises)):
            for i in range(num_car):
                car = Vehicle()
                car.owner = Enterprise.objects.get(pk=enterprises[j])
                car.price = random.randint(1,1000000)
                # car.condition= car.CONDITION[]
                car.mileage = random.randint(1,2500000)
                car.year_manufacture =random.randint(1980,2022)
                car.brand = Brand.objects.get(pk=random.randint(1,3))
                car.save()



