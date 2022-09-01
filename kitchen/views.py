from ast import Delete
from http.client import HTTPResponse
from importlib.metadata import distribution
import json
from multiprocessing import context
from pyexpat.errors import messages
from re import L, template
from unicodedata import name
from urllib import response
from django.http.response import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import DistributionUnit, Menu, Product
from .forms import NewDate, NewDistributionUnit, NewMenu, NewOrder, NewProduct
import math
import numpy as np
from django.forms import formset_factory
import logging
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse


logger = logging.getLogger("django")


def print_orders(request):
    total_distribution_units = len(DistributionUnit.objects.all())
    total_pages = math.ceil(total_distribution_units/5)
    distribution_unit_sets = np.array_split(
        DistributionUnit.objects.all(), total_pages)

    context = {}

    if 'week' in request.session and 'day' in request.session:

        week = request.session['week']
        day = request.session['day']

        menus_1 = Menu.objects.filter(
            week=week, day=day, meal=1)
        menus_2 = Menu.objects.filter(
            week=week, day=day, meal=2)
        menus_3 = Menu.objects.filter(
            week=week, day=day, meal=3)

        page_contents = []

        for distribution_unit_set in distribution_unit_sets:

            products_1 = [
                {'product': product, 'product_amounts': product_amounts(product, distribution_unit_set, 1)} for menu in menus_1 for product in Product.objects.filter(menu=menu)]
            products_2 = [
                {'product': product, 'product_amounts': product_amounts(product, distribution_unit_set, 2)} for menu in menus_2 for product in Product.objects.filter(menu=menu)]
            products_3 = [
                {'product': product, 'product_amounts': product_amounts(product, distribution_unit_set, 3)} for menu in menus_3 for product in Product.objects.filter(menu=menu)]

            page_contents.append({'distribution_units': distribution_unit_set,
                                  'products_1': products_1,
                                  'products_2': products_2,
                                 'products_3': products_3})
        context['contents'] = page_contents

    template_path = 'print_table.html'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="orders.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)

    return response


def product_amounts(product, distribution_units, meal_no):
    product_amount = []
    for distribution_unit in distribution_units:
        if distribution_unit.unit_type == 'k':
            if meal_no == 1:
                product_amount.append(
                    {'amount': product.small_portion_amount * distribution_unit.meal_1, 'containers': math.ceil((product.small_portion_amount * distribution_unit.meal_1)/product.amount_per_container)})
            if meal_no == 2:
                product_amount.append(
                    {'amount': product.small_portion_amount * distribution_unit.meal_2, 'containers': math.ceil((product.small_portion_amount * distribution_unit.meal_2)/product.amount_per_container)})
            if meal_no == 3:
                product_amount.append(
                    {'amount': product.small_portion_amount * (distribution_unit.meal_1 + distribution_unit.meal_2), 'containers': math.ceil((product.small_portion_amount * (distribution_unit.meal_1 + distribution_unit.meal_2))/product.amount_per_container)})
        else:
            if meal_no == 1:
                product_amount.append(
                    {'amount': product.large_portion_amount * distribution_unit.meal_1, 'containers': math.ceil((product.large_portion_amount * distribution_unit.meal_1)/product.amount_per_container)})
            if meal_no == 2:
                product_amount.append(
                    {'amount': product.large_portion_amount * distribution_unit.meal_2, 'containers': math.ceil((product.large_portion_amount * distribution_unit.meal_2)/product.amount_per_container)})
            if meal_no == 3:
                product_amount.append(
                    {'amount': product.large_portion_amount * (distribution_unit.meal_1 + distribution_unit.meal_2), 'containers': math.ceil((product.large_portion_amount * (distribution_unit.meal_1 + distribution_unit.meal_2))/product.amount_per_container)})
    return product_amount


def home(request, page=None):

    context = {}
    date_form = None

    context['total_products'] = len(Product.objects.all())
    context['total_menus'] = len(Menu.objects.all())
    context['total_distribution_units'] = len(DistributionUnit.objects.all())
    total_pages = math.ceil(context['total_distribution_units']/8)
    distribution_units = np.array_split(
        DistributionUnit.objects.all(), total_pages)
    context['page'] = page

    if page is None:
        context['distribution_units'] = distribution_units[0]
    elif page < total_pages:
        context['distribution_units'] = distribution_units[page]
    else:
        context['distribution_units'] = distribution_units[total_pages-1]

    if request.method == 'POST':
        form = NewDate(request.POST)
        if form.is_valid():
            week = form.cleaned_data['week']
            day = form.cleaned_data['day']

            request.session['week'] = week
            request.session['day'] = day

        date_form = form
    else:
        date_form = NewDate()

    if 'week' in request.session and 'day' in request.session:

        context['week'] = request.session['week']
        context['day'] = request.session['day']

        menus_1 = Menu.objects.filter(
            week=context['week'], day=context['day'], meal=1)
        menus_2 = Menu.objects.filter(
            week=context['week'], day=context['day'], meal=2)
        menus_3 = Menu.objects.filter(
            week=context['week'], day=context['day'], meal=3)

        context['products_1'] = [
            {'product': product, 'product_amounts': product_amounts(product, context['distribution_units'], 1)} for menu in menus_1 for product in Product.objects.filter(menu=menu)]
        context['products_2'] = [
            {'product': product, 'product_amounts': product_amounts(product, context['distribution_units'], 2)} for menu in menus_2 for product in Product.objects.filter(menu=menu)]
        context['products_3'] = [
            {'product': product, 'product_amounts': product_amounts(product, context['distribution_units'], 3)} for menu in menus_3 for product in Product.objects.filter(menu=menu)]

    else:
        date_form = NewDate()

    context['form'] = date_form

    return render(request, 'home.html', context)


def add_menu(request):

    menu_form = None

    if request.method == 'POST':
        form = NewMenu(request.POST)
        if form.is_valid():
            menu = Menu(name=form.cleaned_data['name'],
                        week=form.cleaned_data['week'],
                        day=form.cleaned_data['day'],
                        meal=form.cleaned_data['meal'])

            menu.save()
        return HttpResponseRedirect('../menu/view')
    else:
        menu_form = NewMenu()

    context = {
        'form': menu_form,
        'form_title': 'Add Menu'
    }
    return render(request, 'form.html', context)


def view_menu(request):
    menus = Menu.objects.all()
    context = {
        'type': 'menu',
        'items': menus,
        'table_title': 'Menus'
    }
    return render(request, 'table.html', context)


def add_product(request):
    product_form = None

    if request.method == 'POST':
        product_form = NewProduct(request.POST)
        if product_form.is_valid():
            product_menu = Menu.objects.get(id=request.POST['menu'])
            product = Product(name=product_form.cleaned_data['name'],
                              small_portion_amount=product_form.cleaned_data[
                'small_portion_amount'],
                large_portion_amount=product_form.cleaned_data[
                'large_portion_amount'],
                amount_per_container=product_form.cleaned_data[
                'amount_per_container'],
                unit=product_form.cleaned_data['unit'],
                menu=product_menu)

            product.save()
            return HttpResponseRedirect('../product/view')
    else:
        product_form = NewProduct()

    context = {
        'form': product_form,
        'form_title': 'Add Product'

    }

    return render(request, 'form.html', context)


def view_product(request):
    search_form = None
    context = {
        'type': 'product',
        'table_title': 'Products'
    }
    products = None

    if request.method == 'POST':
        search_form = NewDate(request.POST)
        if search_form.is_valid():
            request.session['week'] = search_form.cleaned_data['week']
            request.session['day'] = search_form.cleaned_data['day']
    else:
        search_form = NewDate()

    if 'week' in request.session and 'day' in request.session:
        menus = Menu.objects.filter(
            week=request.session['week'], day=request.session['day'])
        products = [
            product for menu in menus for product in Product.objects.filter(menu=menu)]
    else:
        products = Product.objects.all()

    context['form'] = search_form
    context['items'] = products

    return render(request, 'table.html', context)


def edit_product(request, pk=None):
    context = {}
    context['page_title'] = "Edit Product"
    if not pk is None:
        if request.method == 'POST':
            product = Product.objects.get(name=request.POST['name'])

            updated_product = NewProduct(request.POST)
            if updated_product.is_valid():
                product.small_portion_amount = updated_product.cleaned_data['small_portion_amount']
                product.large_portion_amount = updated_product.cleaned_data['large_portion_amount']
                product.amount_per_container = updated_product.cleaned_data['amount_per_container']
                product.unit = updated_product.cleaned_data['unit']
                product.menu = Menu.objects.get(
                    id=request.POST['menu'])

                product.save()

            return HttpResponseRedirect('../../product/view')
        else:
            product = Product.objects.get(id=pk)
            product_form = NewProduct(initial={'name': product.name,
                                               'small_portion_amount': product.small_portion_amount,
                                               'large_portion_amount': product.large_portion_amount,
                                               'amount_per_container': product.amount_per_container,
                                               'unit': product.unit,
                                               'menu': product.menu})
            context['form'] = product_form
            context['form_title'] = 'Edit Product'
    else:
        context['form'] = {}

    return render(request, 'edit_form.html', context)


def edit_menu(request, pk=None):
    context = {}
    context['page_title'] = "Edit Menu"
    if not pk is None:
        if request.method == 'POST':
            menu = Menu.objects.get(name=request.POST['name'])

            updated_menu = NewMenu(request.POST)
            if updated_menu.is_valid():
                menu.week = updated_menu.cleaned_data['week']
                menu.day = updated_menu.cleaned_data['day']
                menu.meal = updated_menu.cleaned_data['meal']

                menu.save()

            return HttpResponseRedirect('../../menu/view')
        else:
            menu = Menu.objects.get(id=pk)
            menu_form = NewMenu(initial={'name': menu.name,
                                         'week': menu.week,
                                         'day': menu.day,
                                         'meal': menu.meal})
            context['form'] = menu_form
            context['form_title'] = 'Edit Menu'
    else:
        context['form'] = {}

    return render(request, 'edit_form.html', context)


def edit_distribution_unit(request, pk=None):
    context = {}
    context['page_title'] = "Edit Distribution Unit"
    if not pk is None:
        if request.method == 'POST':
            distribution_unit = DistributionUnit.objects.get(
                name=request.POST['name'])

            updated_distribution_unit = NewDistributionUnit(request.POST)
            if updated_distribution_unit.is_valid():
                distribution_unit.unit_type = updated_distribution_unit.cleaned_data['unit_type']
                distribution_unit.meal_1 = updated_distribution_unit.cleaned_data['meal_1']
                distribution_unit.meal_2 = updated_distribution_unit.cleaned_data['meal_2']
                distribution_unit.lunch = updated_distribution_unit.cleaned_data['lunch']

                distribution_unit.save()

            return HttpResponseRedirect('../../distribution_unit/view')
        else:
            distribution_unit = DistributionUnit.objects.get(id=pk)
            distribution_unit_form = NewDistributionUnit(initial={'name': distribution_unit.name,
                                                                  'unit_type': distribution_unit.unit_type,
                                                                  'meal_1': distribution_unit.meal_1,
                                                                  'meal_2': distribution_unit.meal_2,
                                                                  'lunch': distribution_unit.lunch,
                                                                  })
            context['form'] = distribution_unit_form
            context['form_title'] = 'Update Distribution Unit'
    else:
        context['form'] = {}

    return render(request, 'edit_form.html', context)


def add_distribution_unit(request):

    unit_form = None

    if request.method == 'POST':
        unit_form = NewDistributionUnit(request.POST)
        if unit_form.is_valid():
            distribution_unit = DistributionUnit(
                name=unit_form.cleaned_data['name'], unit_type=unit_form.cleaned_data['unit_type'],
                meal_1=unit_form.cleaned_data['meal_1'], meal_2=unit_form.cleaned_data['meal_2'],
                lunch=unit_form.cleaned_data['lunch'])

            distribution_unit.save()
        return HttpResponseRedirect('../distribution_unit/view')
    else:
        unit_form = NewDistributionUnit()

    context = {
        'form': unit_form,
        'form_title': 'Add Distribution Unit'

    }

    return render(request, 'form.html', context)


def view_distribution_unit(request):
    distribution_units = DistributionUnit.objects.all()
    context = {
        'type': 'distribution_unit',
        'items': distribution_units,
        'table_title': 'Distribution Units'
    }
    return render(request, 'table.html', context)


def delete_product(request, pk=None):
    if not pk is None:
        try:
            product = Product.objects.get(id=pk)
            product.delete()
        except Exception as err:
            print(err)

    return HttpResponseRedirect('../../product/view')


def delete_menu(request, pk=None):
    if not pk is None:
        try:
            menu = Menu.objects.get(id=pk)
            menu.delete()
        except Exception as err:
            print(err)

    return HttpResponseRedirect('../../menu/view')


def delete_distribution_unit(request, pk=None):
    if not pk is None:
        try:
            distribution_unit = DistributionUnit.objects.get(id=pk)
            distribution_unit.delete()
        except Exception as err:
            print(err)

    return HttpResponseRedirect('../../distribution_unit/view')


def edit_orders(request):
    order_form = None
    distribution_units = DistributionUnit.objects.all()

    neworder_formset = formset_factory(
        NewOrder, min_num=len(distribution_units), extra=0)
    initial_fields = [{'distribution_unit': distribution_unit.name, 'meal_1': distribution_unit.meal_1,
                       'meal_2': distribution_unit.meal_2, 'lunch': distribution_unit.lunch} for distribution_unit in distribution_units]

    if request.method == 'POST':
        order_form = neworder_formset(request.POST)
        logger.info(order_form)
        if order_form.is_valid():
            logger.info('in valid')
            for order in order_form:
                distribution_unit = DistributionUnit.objects.get(
                    name=order.cleaned_data['distribution_unit'])
                distribution_unit.meal_1 = order.cleaned_data['meal_1']
                distribution_unit.meal_2 = order.cleaned_data['meal_2']
                distribution_unit.lunch = order.cleaned_data['lunch']

                distribution_unit.save()
        return HttpResponseRedirect('distribution_unit/view')
    else:
        order_form = neworder_formset(initial=initial_fields)

    context = {
        'form_set': order_form,
        'form_title': 'Edit Orders',
    }

    return render(request, 'table_form.html', context)
