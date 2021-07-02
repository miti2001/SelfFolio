from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone
import os

class Profile (models.Model):
    PROFILE_CATEGORY = (
        ('Student','Student'),
        ('Professional','Professional'),
    )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    Bio = models.TextField(blank = True, null=True)
    University = models.CharField(max_length = 50, null=True, blank=True)
    Profession = models.CharField(max_length=32, default='Student', choices=PROFILE_CATEGORY, null=True)
    DOB = models.DateField(null=True)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    

    def __str__ (self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



class Attendance(models.Model):
    subject = models.CharField(max_length = 50)
    code = models.CharField(max_length=32)
    present = models.IntegerField()
    absent = models.IntegerField()
    attendance = models.FloatField(null=True)
    userProfile = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__ (self):
        return self.code

class Expense(models.Model):
    EXPENSE_CATEGORY = (
        ('Health','Health'),
        ('Education','Education'),
        ('Food','Food'),
        ('Personal','Personal'),
    )
    price = models.PositiveIntegerField(null=True)
    item = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    total = models.PositiveIntegerField(null=True)
    userProfile = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__ (self):
        return self.item


class Grade(models.Model):
    SEM_CATEGORY = (
        ('Sem 1', 'Sem 1'),
        ('Sem 2', 'Sem 2'),
        ('Sem 3', 'Sem 3'),
        ('Sem 4', 'Sem 4'),
        ('Sem 5', 'Sem 5'),
        ('Sem 6', 'Sem 6'),
        ('Sem 7', 'Sem 7'),
        ('Sem 8', 'Sem 8'),
    )
    semester = models.CharField(max_length=30, choices=SEM_CATEGORY)
    subject = models.CharField(max_length=50)
    code = models.CharField(max_length=32)
    credits = models.FloatField()
    pointer = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    creditsEarned = models.FloatField(null=True)
    userProfile = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject
