# Generated by Django 3.1.1 on 2020-09-23 12:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0002_auto_20200923_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=128, validators=[django.core.validators.MinLengthValidator(6, 'Password must contain atleast 6 characters')]),
        ),
    ]