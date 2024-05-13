# Generated by Django 4.2 on 2024-01-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0006_auto_20220211_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='branch',
            field=models.CharField(blank=True, choices=[('ME', 'ME'), ('EE', 'EE'), ('physics', 'Physics'), ('English', 'English')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='course',
            field=models.CharField(blank=True, choices=[('B.Tech', 'B.Tech'), ('B.Sc', 'B.Sc'), ('B.A', 'B.A'), ('M.Tech', 'M.Tech')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='faculty',
            field=models.CharField(blank=True, choices=[('Engineering', 'Faculty of Engineering'), ('Science', 'Faculty of Science'), ('Arts', 'Faculty of Arts')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='year',
            field=models.CharField(blank=True, choices=[('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pciture'),
        ),
    ]