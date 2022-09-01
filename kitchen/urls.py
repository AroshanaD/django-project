from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:page>', views.home, name='home'),
    path('menu/add', views.add_menu, name='add_menu'),
    path('menu/view', views.view_menu, name='view_menu'),
    path('product/add', views.add_product, name='add_product'),
    path('product/view', views.view_product, name='view_product'),
    path('product/edit', views.edit_product, name='edit_product'),
    path('product/edit/<int:pk>', views.edit_product, name='edit_product'),
    path('product/delete', views.delete_product, name='delete_product'),
    path('product/delete/<int:pk>', views.delete_product, name='delete_product'),
    path('menu/edit', views.edit_menu, name='edit_menu'),
    path('menu/edit/<int:pk>', views.edit_menu, name='edit_menu'),
    path('menu/delete', views.delete_menu, name='delete_menu'),
    path('menu/delete/<int:pk>', views.delete_menu, name='delete_menu'),
    path('distribution_unit/edit', views.edit_distribution_unit,
         name='edit_distribution_unit'),
    path('distribution_unit/edit/<int:pk>',
         views.edit_distribution_unit, name='edit_distribution_unit'),
    path('distribution_unit/add', views.add_distribution_unit,
         name='add_distribution_unit'),
    path('distribution_unit/view', views.view_distribution_unit,
         name='view_distribution_unit'),
    path('distribution_unit/delete', views.delete_distribution_unit,
         name='delete_distribution_unit'),
    path('distribution_unit/delete/<int:pk>',
         views.delete_distribution_unit, name='delete_distribution_unit'),
    path('orders',
         views.edit_orders, name='edit_orders'),
    path('print_orders', views.print_orders, name='print_orders')
]
