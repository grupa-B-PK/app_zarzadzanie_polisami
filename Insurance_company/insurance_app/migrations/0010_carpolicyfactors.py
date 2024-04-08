# Generated by Django 5.0.2 on 2024-04-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0009_alter_carinsurance_average_year_mileage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarPolicyFactors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_factor', models.IntegerField(default=1)),
                ('mileage_factor_1', models.IntegerField(default=0.002)),
                ('mileage_factor_2', models.IntegerField(default=0.0033)),
                ('mileage_factor_3', models.IntegerField(default=0.0044)),
                ('avg_year_mileage_1', models.IntegerField(default=0.05)),
                ('avg_year_mileage_2', models.IntegerField(default=0.07)),
                ('avg_year_mileage_3', models.IntegerField(default=0.09)),
                ('avg_year_mileage_4', models.IntegerField(default=0.1)),
                ('rented_factor_1', models.IntegerField(default=1)),
                ('rented_factor_2', models.IntegerField(default=3)),
                ('owners_factor_1', models.IntegerField(default=1)),
                ('owners_factor_2', models.IntegerField(default=1.2)),
                ('owners_factor_3', models.IntegerField(default=1.8)),
                ('owners_factor_4', models.IntegerField(default=2)),
            ],
        ),
    ]
