# Generated by Django 4.2 on 2024-03-27 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_events'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumni',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Batch', models.CharField(max_length=10)),
                ('Course', models.CharField(max_length=10)),
                ('Branch', models.CharField(max_length=10)),
                ('Company', models.CharField(blank=True, max_length=100, null=True)),
                ('Role', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
