# Generated by Django 5.0 on 2025-04-07 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('company_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('signup_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
