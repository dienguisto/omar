# Generated by Django 3.1.6 on 2021-02-21 12:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping'), ('D', 'Delivery'), ('X', 'Default')], default=django.utils.timezone.now, max_length=1),
            preserve_default=False,
        ),
    ]
