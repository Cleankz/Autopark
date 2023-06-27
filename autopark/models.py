import datetime

import pytz
from django.contrib.auth.models import AbstractUser, User
from django.contrib.gis.geos import LineString, Point
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models
from djgeojson.fields import GeoJSONField
from pytz import common_timezones



class Brand (models.Model):
    brand_name = models.CharField(max_length=70, help_text='Введите название бренда', verbose_name='Бренд')
    type = models.CharField(max_length=70, help_text='Введите тип техники', verbose_name='Тип')
    tank_volume = models.IntegerField(validators=[MinValueValidator(0)], verbose_name= 'Объем бака')
    seats_number = models.IntegerField(validators=[MinValueValidator(0)], verbose_name= 'Количество мест')
    load_capacity = models.IntegerField(validators=[MinValueValidator(0)], verbose_name= 'Грузоподъемность')

    class Meta:
        ordering = ['brand_name','type'] # sort by id
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.brand_name

class Manager(User):


    class Meta:
        proxy = True
        ordering = ['id'] # sort by id
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'




    def __str__(self):
        return str(self.id)



class Enterprise(models.Model):
    name = models.CharField(max_length=70, help_text='Введите название предприятия', verbose_name='Имя предприятия')
    address = models.CharField(max_length=70, help_text='Введите адрес предприятия', verbose_name='Адрес предприятия')
    num_of_employee = models.IntegerField(validators=[MinValueValidator(0)], verbose_name= 'Число сотрудников')
    # manager = models.ForeignKey(Manager, verbose_name='Менеджер',on_delete=models.SET_NULL,null=True, blank=True)
    manager = models.ManyToManyField(Manager, verbose_name='Сотрудники',blank=True)
    zoner = models.CharField(max_length=255, choices=[(tz, tz) for tz in common_timezones], default='Europe/Moscow',verbose_name='Часовой пояс')

    class Meta:
        ordering = ['name']
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'

    def __str__(self):
        return str(self.pk)


class Vehicle(models.Model):
    year_manufacture = models.IntegerField(validators=[MinValueValidator(1900),MaxValueValidator(datetime.date.today().year)], verbose_name= 'Год выпуска')
    mileage = models.IntegerField(validators=[MinValueValidator(0)], verbose_name= 'Пробег')
    price = models.IntegerField(validators=[MinValueValidator(0)],help_text='Введите стоимость в рублях', verbose_name= 'Стоимость')
    brand = models.ForeignKey(Brand,verbose_name='Бренд', on_delete=models.SET_NULL,null=True)
    owner = models.ForeignKey(Enterprise,verbose_name='Владелец', on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(default=datetime.datetime.utcnow(),blank=True, null=True)


    CONDITION = [
        ('NEW','Новое'),
        ('GOOD','Хорошее'),
        ('WORN','С пробегом'),
        ('BAD','Плохое'),
        ('UNK','Неизвестно')
    ]

    condition = models.CharField(choices=CONDITION, max_length=7, default="UNKNOWN", verbose_name='Состояние')
    # discount_code = models.CharField(max_length = 10, verbose_name = '')
    # discount = models.IntegerField(
    #     validators=[MinValueValidator(1),MaxValueValidator(100)],
    #     verbose_name='Скидка',
    #     help_text='В процентах'
    # )

    class Meta:
        ordering = ['brand','year_manufacture','price','mileage'] # sort by id
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'

    def price_currency(self):
        return str(self.price) + ' руб.'

    def mileage_value(self):
        return str(self.mileage) + ' км.'

    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = datetime.datetime.now().replace(tzinfo=pytz.timezone(self.owner.zoner))
        else:
            self.date = self.date.replace(tzinfo=pytz.timezone(self.owner.zoner))
        super().save(*args, **kwargs)



    def __str__(self):
        return 'Номер: ' + str(self.id)

    price_currency.short_description = 'Стоимость'
    mileage_value.short_description = 'Пробег'


class Driver(models.Model):
    name = models.CharField(max_length=70, help_text='Введите ФИО', verbose_name='Имя сотрудника')
    # date_of_birthday = models.DateField(verbose_name='Дата рождения')
    residential_address = models.TextField(help_text='Введите адрес места проживания', verbose_name='Адрес')
    phone = models.CharField(max_length=70, verbose_name='Телефон')
    job = models.ForeignKey(Enterprise,verbose_name='Место работы', on_delete=models.SET_NULL,blank=True,null=True)
    car = models.ForeignKey(Vehicle,verbose_name='Машина', on_delete=models.SET_NULL,blank=True,null=True)

    STATUS = [
        ('ACT','Занят'),
        ('NACT','Свободен'),
    ]
    status = models.CharField(choices=STATUS, max_length=4, default='NACT', verbose_name='Статус', null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return str(self.id)



class Routes(models.Model):
    car = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    route = models.MultiPointField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # time_zone = models.TimeField(default=pytz.UTC)
    objects = models.Manager()
#     name = models.CharField(max_length=255)
    # path = models.MultiPointField()
    # objects = models.Manager()
    class Meta:
        ordering = ['car']
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'

    def __str__(self):
        return str(self.id)