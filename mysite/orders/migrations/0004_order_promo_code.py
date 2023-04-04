# Generated by Django 4.1.3 on 2023-04-04 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promo_codes', '0001_initial'),
        ('orders', '0003_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promo_codes.promocode'),
        ),
    ]