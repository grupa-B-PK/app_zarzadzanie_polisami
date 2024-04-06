# Generated by Django 5.0.2 on 2024-04-06 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customer_first_name_remove_customer_last_name_and_more'),
        ('insurance_app', '0005_carinsurance_customer_houseinsurance_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinsurance',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
        migrations.AlterField(
            model_name='houseinsurance',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
    ]
