# Generated by Django 4.2 on 2024-04-09 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0010_alter_notif_faculty_m'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pciture'),
        ),
    ]