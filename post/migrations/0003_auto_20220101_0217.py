# Generated by Django 3.1 on 2022-01-01 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20220101_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
