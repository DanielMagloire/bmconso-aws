# Generated by Django 3.2.6 on 2022-10-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmconso', '0008_auto_20221013_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='hour_begin',
            field=models.PositiveIntegerField(default=16),
        ),
        migrations.AlterField(
            model_name='rule',
            name='hour_end',
            field=models.PositiveIntegerField(default=16),
        ),
    ]