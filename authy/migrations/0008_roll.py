# Generated by Django 4.2 on 2024-03-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0007_profile_branch_profile_course_profile_faculty_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
    ]
