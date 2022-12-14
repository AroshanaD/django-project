# Generated by Django 4.1 on 2022-08-23 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DistributionUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('unit', models.CharField(choices=[('k', 'Kindergarten'), ('s', 'School')], default='s', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('day', models.IntegerField()),
                ('meal', models.IntegerField(choices=[(1, 'Meal 1'), (2, 'Meal 2'), (3, 'Special')])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('small_portion_amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('large_portion_amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('amount_per_container', models.DecimalField(decimal_places=2, max_digits=6)),
                ('unit', models.CharField(choices=[('g', 'Grams'), ('p', 'Pieces')], default='p', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen.menu')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='menu',
            field=models.ManyToManyField(through='kitchen.ProductMenu', to='kitchen.menu'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_1', models.IntegerField()),
                ('meal_2', models.IntegerField()),
                ('lunch', models.IntegerField()),
                ('distribution_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen.distributionunit')),
            ],
        ),
    ]
