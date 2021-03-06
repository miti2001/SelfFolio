# Generated by Django 2.2.8 on 2021-06-14 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SelF', '0003_expense'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Password',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='UserEmail',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='UserName',
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='DOB',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='FirstName',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='LastName',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Profession',
            field=models.CharField(choices=[('Student', 'Student'), ('Professional', 'Professional')], default='Student', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='University',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
