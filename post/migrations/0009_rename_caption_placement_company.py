# Generated by Django 4.2 on 2024-03-26 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_placement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='placement',
            old_name='caption',
            new_name='company',
        ),
    ]
