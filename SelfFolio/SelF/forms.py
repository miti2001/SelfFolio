from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import *
from django.forms import DateTimeInput

class CreateUserForm(UserCreationForm):
    PROFILE_CATEGORY = (
        ('Student', 'Student'),
        ('Professional', 'Professional'),
    )

    DOB = forms.DateField(
        help_text='Required.',
        widget=forms.SelectDateWidget(years=range(1960, 2030))
    )
    Bio = forms.CharField(
        widget=forms.Textarea(attrs={
           'cols': 30,
           'rows': 3
        }),
        required=False
    )
    University = forms.CharField(help_text='Required.')
    Profession = forms.CharField(
        widget=forms.Select(choices=PROFILE_CATEGORY),
        help_text='Required.'
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "DOB", "Bio", "University", "Profession", "password1", "password2"]

class addSubject(forms.ModelForm):
    code = forms.CharField(help_text='Required.')
    subject = forms.CharField(help_text='Required.')

    class Meta:
        model = Attendance
        fields = ["code", "subject"]


class addLog(forms.ModelForm):
    EXPENSE_CATEGORY = (
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Food', 'Food'),
        ('Personal', 'Personal'),
    )
    item = forms.CharField(help_text='Required.')
    price = forms.IntegerField(
        help_text='Required.',
        validators=[MinValueValidator(1)]
    )
    date = forms.DateField(
        help_text='Required.',
        widget= forms.SelectDateWidget(years=range(2010, 2030)),
        initial=timezone.now()
    )
    category = forms.Select(choices=EXPENSE_CATEGORY)
    quantity = forms.IntegerField(
        help_text='Required.',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        model = Expense
        fields = ['item', 'price', 'date', 'category', 'quantity']


class addPointer(forms.ModelForm):
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
    semester = forms.Select(choices=SEM_CATEGORY)
    code = forms.CharField(help_text='Required.')
    subject = forms.CharField(help_text='Required.')
    credits = forms.FloatField(help_text='Required.')
    pointer = forms.IntegerField(
        help_text='Required.',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        model = Grade
        fields = ['semester', 'code', 'subject', 'credits', 'pointer']