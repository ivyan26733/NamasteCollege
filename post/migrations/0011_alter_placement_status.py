# Generated by Django 4.2 on 2024-03-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_alter_placement_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placement',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Ongoing', 'Ongoing'), ('Cancelled', 'Cancelled'), ('Waiting', 'Waiting'), ('Coming Soon', 'Coming Soon'), ('Postponed', 'Postponed'), ('Preponed', 'Preponed')], max_length=50),
        ),
    ]