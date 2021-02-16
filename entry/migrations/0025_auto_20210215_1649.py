# Generated by Django 3.1.1 on 2021-02-15 11:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0024_remove_visitor_qrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='mobile',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)], verbose_name='Mobile number'),
        ),
    ]
