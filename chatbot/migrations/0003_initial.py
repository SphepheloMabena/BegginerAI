# Generated by Django 4.2.5 on 2023-09-16 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatbot', '0002_delete_fuelprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_type', models.CharField(choices=[('petrol', 'Petrol'), ('diesel', 'Diesel')], max_length=10)),
                ('litres_price', models.CharField(max_length=50)),
                ('gallons_price', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
