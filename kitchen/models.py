from django.db import models


class Menu(models.Model):

    MEAL_1 = 1
    MEAL_2 = 2
    SPECIAL = 3

    MEALS = [
        (MEAL_1, 1),
        (MEAL_2, 2),
        (SPECIAL, 3)
    ]

    name = models.CharField(max_length=4, unique=True)
    week = models.IntegerField()
    day = models.IntegerField()
    meal = models.IntegerField(choices=MEALS)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):

    name = models.CharField(max_length=128, unique=True)
    small_portion_amount = models.DecimalField(max_digits=6, decimal_places=2)
    large_portion_amount = models.DecimalField(max_digits=6, decimal_places=2)
    amount_per_container = models.DecimalField(
        max_digits=6, decimal_places=2)
    GRAMS = 'g'
    PIECES = 'p'
    UNIT_CHOICES = [
        (GRAMS, 'Grams'),
        (PIECES, 'Pieces')
    ]
    unit = models.CharField(max_length=1, choices=UNIT_CHOICES, default=PIECES)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        ordering = ['menu']

    def __str__(self):
        return f'{self.name}'


class DistributionUnit(models.Model):

    name = models.CharField(max_length=128, unique=True)
    KINDERGARTEN = 'k'
    SCHOOL = 's'
    TYPE = [
        (KINDERGARTEN, 'Kindergarten'),
        (SCHOOL, 'School')
    ]
    unit_type = models.CharField(max_length=1, choices=TYPE, default=SCHOOL)
    meal_1 = models.IntegerField()
    meal_2 = models.IntegerField()
    lunch = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
