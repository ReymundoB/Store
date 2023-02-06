# Generated by Django 4.1.3 on 2023-02-06 03:17

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(orders.models.OrderStatus['CREATED'], 'CREATED'), (orders.models.OrderStatus['PAYED'], 'PAYED'), (orders.models.OrderStatus['COMPLETED'], 'COMPLETED'), (orders.models.OrderStatus['CANCELED'], 'CANCELED')], default=orders.models.OrderStatus['CREATED'], max_length=50),
        ),
    ]
