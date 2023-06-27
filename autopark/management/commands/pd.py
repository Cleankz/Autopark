from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

from autopark.models import Vehicle, Enterprise, Brand,Driver,Enterprise
import random

class Command(BaseCommand):
    help = 'Add driver'


    def add_arguments(self, parser):
        parser.add_argument('enterprise', nargs='+', type=str,help='Enterprise name')
        parser.add_argument('num_driver', type=int)

    def handle(self, *args, **kwargs):
        num_driver = kwargs['num_driver']
        enterprises = kwargs['enterprise']
        own = ''

        # for enterprise in enterprises:
        #     try:
        #         own = Enterprise.objects.filter(name=enterprise)
        #     except Vehicle.DoesNotExist:
        #         raise CommandError(f'Enterprise with name  does not exist')
        for j in range(len(enterprises)):
            for i in range(num_driver):
                driver = Driver()
                driver.name = get_random_string(10)
                # d = random.randint(1,30)
                # m = random.randint(1,12)
                # y = random.randint(1960,2000)
                # driver.date_of_birthday = datetime.date(y,m,d)
                driver.residential_address = get_random_string(10)
                driver.phone = random.randint(100000000, 10000000000)
                if i % 10 == 0:
                    driver.status = 'ACT'
                else:
                    driver.status = 'NACT'
                driver.job = Enterprise.objects.get(pk=enterprises[j])
                car = Vehicle.objects.get(pk=random.randint(6000,8000))
                while car.owner != driver.job:
                    car = Vehicle.objects.get(pk=random.randint(6000, 8000))

                driver.car = car

                driver.save()


