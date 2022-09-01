from django import forms

from .models import DistributionUnit, Menu


class NewProduct(forms.Form):
    name = forms.CharField(label='Name of the product', max_length=128, error_messages={
                           'required': 'Please enter product name'})
    small_portion_amount = forms.DecimalField(label='Size of the small portion',
                                              required=True, max_digits=6, decimal_places=2)
    large_portion_amount = forms.DecimalField(label='Size of the large portion',
                                              required=True, max_digits=6, decimal_places=2)
    amount_per_container = forms.DecimalField(label='Amount per container',
                                              required=True, max_digits=6, decimal_places=2)
    GRAMS = 'g'
    PIECES = 'p'
    UNIT_CHOICES = [
        (GRAMS, 'Grams'),
        (PIECES, 'Pieces')
    ]
    unit = forms.ChoiceField(
        label='Unit of measurement (grams/pieces)', choices=UNIT_CHOICES)
    menu = forms.ModelChoiceField(
        label='Menus included in', queryset=Menu.objects.all())


class NewMenu(forms.Form):

    name = forms.CharField(label='Short code', max_length=4)
    week = forms.IntegerField(label='Week', max_value=15)
    day = forms.IntegerField(label='Day', max_value=7)

    MEAL_TYPE = (
        (1, 'Meal 1'),
        (2, 'Meal 2'),
        (3, 'Special')
    )
    meal = forms.ChoiceField(label='Meal', choices=MEAL_TYPE)


class NewDistributionUnit(forms.Form):

    name = forms.CharField(label='Name of the Distribution Unit', max_length=128, error_messages={
                           'required': 'Please enter name'})
    UNIT_TYPE = (
        ('k', 'Kindergarten'),
        ('s', 'School')
    )
    unit_type = forms.ChoiceField(
        label='Distribution unit type', choices=UNIT_TYPE)
    meal_1 = forms.IntegerField(
        label='No.of meals 1 packages', max_value=10000)
    meal_2 = forms.IntegerField(
        label='No.of meals 2 packages', max_value=10000)
    lunch = forms.IntegerField(label='No.of lunch packages', max_value=10000)


class NewDate(forms.Form):
    week = forms.IntegerField(label='Week', max_value=15)
    day = forms.IntegerField(label='Day', max_value=7)


class NewOrder(forms.Form):
    distribution_unit = forms.CharField(max_length=128)
    meal_1 = forms.IntegerField(max_value=10000)
    meal_2 = forms.IntegerField(max_value=10000)
    lunch = forms.IntegerField(max_value=10000)
