# Generated by Django 5.0.7 on 2024-07-13 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='cloud',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='condition',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='gust_speed',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='heatindex',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='humidity',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='precip',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='pressure',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='wind_speed',
            field=models.CharField(max_length=50),
        ),
    ]
