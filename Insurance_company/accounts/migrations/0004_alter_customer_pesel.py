# Generated by Django 5.0.2 on 2024-04-13 07:29

import utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customer_pesel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pesel',
            field=models.CharField(max_length=11, validators=[utils.validators.validate_pesel, utils.validators.validate_pesel_unique]),
        ),
    ]
