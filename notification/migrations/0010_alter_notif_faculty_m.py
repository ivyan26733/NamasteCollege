# Generated by Django 4.2 on 2024-03-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0009_dpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notif',
            name='faculty_m',
            field=models.CharField(blank=True, choices=[('Engineering', 'Faculty of Engineering'), ('Science', 'Faculty of Science'), ('Arts', 'Faculty of Arts'), ('Arch', 'Faculty of Architecture'), ('Comm', 'Faculty of Commerce'), ('Ayush', 'Faculty of Integrated Alternative Medicine (AYUSH)'), ('SocialS', 'Faculty of Social Science'), ('Edu', 'Faculty of Education'), ('TC', 'Technical College')], max_length=100, null=True),
        ),
    ]
