# Generated by Django 2.2.8 on 2021-05-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SelF', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=32)),
                ('present', models.IntegerField()),
                ('absent', models.IntegerField()),
            ],
        ),
    ]
