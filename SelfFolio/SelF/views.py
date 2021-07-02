from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import CreateUserForm, addSubject, addLog, addPointer, UpdateUserForm


# Create your views here.

def logout_func(request):
    logout(request)
    return redirect('login_page')

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if User.objects.filter(username=request.POST['username']).exists():
            messages.error(request, "The username you entered is already taken")
            return redirect('signup')
        if form.is_valid():
            form.save()
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.DOB = form.cleaned_data.get('DOB')
            user.profile.Bio = form.cleaned_data.get('Bio')
            user.profile.Profession = form.cleaned_data.get('Profession')
            user.profile.University = form.cleaned_data.get('University')
            user.save()
            username = form.cleaned_data['username']
            messages.success(request, 'Account was created for ' + username)
            return redirect("login_page")
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('signup')

    else:
        return render(request, "registration/signup.html", {"form": form})

'''
def home(request):
    Username = request.Profile.UserName
    return render(request, 'home.html', {
        'Username': Username,
        'FirstName': content.FirstName,
        'LastName': content.LastName,
        'Email': content.UserEmail,
        'DOB': content.DOB,
        'Bio': content.Bio,
        'University': content.University,
        'Profession': content.Profession,
    })
'''

@login_required(login_url='login_page')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login_page')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='login_page')
def editProfile(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id)
    form = UpdateUserForm(initial={
        'first_name': user[0].first_name,
        'last_name': user[0].last_name,
        'Bio': user[0].profile.Bio,
        'DOB': user[0].profile.DOB,
        'University': user[0].profile.University,
        'Profession': user[0].profile.Profession,
        'profile_pic': user[0].profile.profile_pic,
    })
    if request.method == 'GET':
        return render(request, 'editProfile.html', {
            'form': form
        })
    else:
        form = UpdateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            Bio = form.cleaned_data.get('Bio')
            DOB = form.cleaned_data.get('DOB')
            University = form.cleaned_data.get('University')
            Profession = form.cleaned_data.get('Profession')
            profile_pic = form.cleaned_data.get('profile_pic')
            user.first_name = first_name
            user.last_name = last_name
            user.profile.Bio = Bio
            user.profile.DOB = DOB
            user.profile.University = University
            user.profile.Profession = Profession
            user.profile.profile_pic = profile_pic
            user.save()
            return redirect('profile')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('editProfile')

'''
def login_func(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    elif request.method == 'POST':
        user_name = request.POST['user_name']
        user_password = request.POST['user_password']
        if Profile.objects.filter(UserName=request.POST['user_name']).exists():
            if Profile.objects.get(UserName=request.POST['user_name']).Password == request.POST['user_password']:
                content = Profile.objects.get(UserName=user_name)
                #return redirect('home')
                return render(request, 'home.html', {
                    'Username': content.UserName,
                    'FirstName': content.FirstName,
                    'LastName': content.LastName,
                    'Email': content.UserEmail,
                    'DOB': content.DOB,
                    'Bio': content.Bio,
                    'University': content.University,
                    'Profession': content.Profession,
                })
            else:
                messages.error(request, "The email or password you entered is incorrect!")
                return render(request, 'registration/login.html')
        else:
            messages.error(request, "The email or password you entered is incorrect!")
            return render(request, 'registration/login.html')
'''

def login_func(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'registration/login.html')

'''
@login_required(login_url='login_page')
def attendance(request):
    if request.method == 'GET':
        labels = []
        data = []

        queryset = Attendance.objects.order_by('-present').distinct()
        for subject in queryset:
            labels.append(subject.code)
            total=subject.present + subject.absent
            percent=subject.present/total
            data.append(percent)

        return render(request, 'attendance.html', {
            'labels': labels,
            'data': data,
        })

    else:
        sub = request.POST['subject']
        c = request.POST['code']
        present = request.POST['present']
        absent = request.POST['absent']
        attendance_info = Attendance.objects.create(
            subject = sub,
            code = c,
            present = present,
            absent =absent,
        )
        attendance_info.save()

        labels = []
        data = []

        queryset = Attendance.objects.order_by('-present').distinct()
        for subject in queryset:
            labels.append(subject.code)
            total=(subject.present) + (subject.absent)
            percent=(subject.present)/total
            data.append(percent)

        return render(request, 'attendance.html', {
            'labels': labels,
            'data': data,
        })
'''

@login_required(login_url='login_page')
def attendance(request):
    if request.method == 'GET':
        user_id = request.user.id
        courses = Attendance.objects.filter(userProfile=user_id)
        return render(request, 'attendance.html', {
            'courses': courses,
        })

@login_required(login_url='login_page')
def addSub(request):
    form = addSubject()
    if request.method == 'GET':
        return render(request, 'addSub.html', {
            'form': form
        })
    else:
        form = addSubject(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.filter(id=user_id)
            subject = form.cleaned_data.get('subject')
            code = form.cleaned_data.get('code')
            new_subject = Attendance.objects.create(
                userProfile= user[0],
                code= code,
                subject= subject,
                present= 0,
                absent= 0,
                attendance= 0.0,
            )
            new_subject.save()
            return redirect('attendance')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('addSub')

@login_required(login_url='login_page')
def markAttendance(request):
    if request.method=='GET':
        return render(request, 'markAttendance.html')
    else:
        course_id=request.GET.get('id')
        status = request.POST['attendance']
        course = Attendance.objects.filter(id=course_id)
        present = course[0].present
        absent = course[0].absent
        if status == 'present':
            present += 1
            Attendance.objects.filter(id=course_id).update(present=present)
        else:
            absent += 1
            Attendance.objects.filter(id=course_id).update(absent=absent)
        total = present+absent
        attendance = present/total * 100
        Attendance.objects.filter(id=course_id).update(attendance=attendance)
        return redirect('attendance')

@login_required(login_url='login_page')
def editSub(request):
    subject_id = request.GET.get('id')
    course = Attendance.objects.filter(id=subject_id)
    form = addSubject(initial={
        'code': course[0].code,
        'subject': course[0].subject,
    })
    if request.method == 'GET':
        return render(request, 'addSub.html', {
            'form': form
        })
    else:
        form = addSubject(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.filter(id=user_id)
            code = form.cleaned_data.get('code')
            subject = form.cleaned_data.get('subject')
            updated_course = course.update(
                userProfile=user[0],
                code=code,
                subject=subject,
            )
            return redirect('attendance')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('addSub')

@login_required(login_url='login_page')
def deleteSub(request):
    subject_id = request.GET.get('id')
    course = Attendance.objects.filter(id=subject_id)
    if request.method == 'GET':
        return render(request, 'deleteSub.html', {
            'course': course[0],
        })
    else:
        course.delete()
        return redirect('attendance')


@login_required(login_url='login_page')
def expense(request):
    if request.method == 'GET':
        labels = []
        data = []
        
        user_id = request.user.id
        entries = reversed(Expense.objects.filter(userProfile=user_id).order_by('date'))
        healthLogs = Expense.objects.filter(userProfile=user_id, category='Health').order_by('date').reverse()
        total1=0
        for entry in healthLogs:
            total1 = total1 + entry.total
        labels.append('Health')
        data.append(total1)
        foodLogs = Expense.objects.filter(userProfile=user_id, category='Food').order_by('date').reverse()
        total2 = 0
        for entry in foodLogs:
            total2 = total2 + entry.total
        labels.append('Food')
        data.append(total2)
        eduLogs = Expense.objects.filter(userProfile=user_id, category='Education').order_by('date').reverse()
        total3 = 0
        for entry in eduLogs:
            total3 = total3 + entry.total
        labels.append('Education')
        data.append(total3)
        personalLogs = Expense.objects.filter(userProfile=user_id, category='Personal').order_by('date').reverse()
        total4 = 0
        for entry in personalLogs:
            total4 = total4 + entry.total
        labels.append('Personal')
        data.append(total4)
        complete_total = total1+total2+total3+total4

        return render(request, 'expense.html', {
            'complete_total': complete_total,
            'entries': entries,
            'total1': total1,
            'healthLogs': healthLogs,
            'total2': total2,
            'foodLogs': foodLogs,
            'total3': total3,
            'eduLogs': eduLogs,
            'total4': total4,
            'personalLogs': personalLogs,
            'labels': labels,
            'data': data,
        })

@login_required(login_url='login_page')
def addEntry(request):
    form = addLog()
    if request.method == 'GET':
        return render(request, 'addLog.html', {
            'form': form
        })
    else:
        form = addLog(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.filter(id=user_id)
            price = form.cleaned_data.get('price')
            item = form.cleaned_data.get('item')
            category = form.cleaned_data.get('category')
            date = form.cleaned_data.get('date')
            quantity = form.cleaned_data.get('quantity')
            total = price*quantity
            new_log = Expense.objects.create(
                userProfile= user[0],
                price = price,
                item = item,
                category = category,
                date = date,
                quantity = quantity,
                total = total,
            )
            new_log.save()
            return redirect('expense')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('addLog')

@login_required(login_url='login_page')
def editEntry(request):
    log_id = request.GET.get('id')
    expense = Expense.objects.filter(id=log_id)
    form = addLog(initial={
        'item': expense[0].item,
        'price': expense[0].price,
        'quantity': expense[0].quantity,
        'date': expense[0].date,
        'category': expense[0].category,
    })
    if request.method == 'GET':
        return render(request, 'addLog.html', {
            'form': form
        })
    else:
        form = addLog(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.filter(id=user_id)
            item = form.cleaned_data.get('item')
            price = form.cleaned_data.get('price')
            quantity = form.cleaned_data.get('quantity')
            date = form.cleaned_data.get('date')
            category = form.cleaned_data.get('category')
            total = price * quantity
            updated_expense = expense.update(
                userProfile=user[0],
                price=price,
                item=item,
                quantity=quantity,
                date=date,
                category=category,
                total=total,
            )
            return redirect('expense')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('addLog')

@login_required(login_url='login_page')
def deleteEntry(request):
    log_id = request.GET.get('id')
    expense = Expense.objects.filter(id=log_id)
    if request.method == 'GET':
        return render(request, 'deleteLog.html', {
            'expense': expense[0],
        })
    else:
        expense.delete()
        return redirect('expense')

@login_required(login_url='login_page')
def grade(request):
    if request.method == 'GET':
        user_id = request.user.id
        grades = Grade.objects.filter(userProfile=user_id)
        Sem1 = Grade.objects.filter(userProfile=user_id, semester='Sem 1')
        total1=0
        total11=0
        for entry in Sem1:
            total1 = total1 + entry.creditsEarned
            total11 = total11 + entry.credits
        cpi_sem1 = 0
        if total11 > 0:
            cpi_sem1 = total1/total11
        total_credits_earned = total1
        total_credits = total11
        spi_sem1 = 0
        if total_credits > 0:
            spi_sem1 = total_credits_earned/total_credits
        Sem2 = Grade.objects.filter(userProfile=user_id, semester='Sem 2')
        total2 = 0
        total22 = 0
        for entry in Sem2:
            total2 = total2 + entry.creditsEarned
            total22 = total22 + entry.credits
        cpi_sem2 = 0
        if total22 > 0:
            cpi_sem2 = total2 / total22
        total_credits_earned += total2
        total_credits += total22
        spi_sem2 = 0
        if total_credits > 0:
            spi_sem2 = total_credits_earned / total_credits
        Sem3 = Grade.objects.filter(userProfile=user_id, semester='Sem 3')
        total3 = 0
        total33 = 0
        for entry in Sem3:
            total3 = total3 + entry.creditsEarned
            total33 = total33 + entry.credits
        cpi_sem3 = 0
        if total33 > 0:
            cpi_sem3 = total3 / total33
        total_credits_earned += total3
        total_credits += total33
        spi_sem3 = 0
        if total_credits > 0:
            spi_sem3 = total_credits_earned / total_credits
        Sem4 = Grade.objects.filter(userProfile=user_id, semester='Sem 4')
        total4 = 0
        total44 = 0
        for entry in Sem4:
            total4 = total4 + entry.creditsEarned
            total44 = total44 + entry.credits
        cpi_sem4 = 0
        if total44 > 0:
            cpi_sem4 = total4 / total44
        total_credits_earned += total4
        total_credits += total44
        spi_sem4 = 0
        if total_credits > 0:
            spi_sem4 = total_credits_earned / total_credits
        Sem5 = Grade.objects.filter(userProfile=user_id, semester='Sem 5')
        total5 = 0
        total55 = 0
        for entry in Sem5:
            total5 = total5 + entry.creditsEarned
            total55 = total55 + entry.credits
        cpi_sem5 = 0
        if total55 > 0:
            cpi_sem5 = total5 / total55
        total_credits_earned += total5
        total_credits += total55
        spi_sem5 = 0
        if total_credits > 0:
            spi_sem5 = total_credits_earned / total_credits
        Sem6 = Grade.objects.filter(userProfile=user_id, semester='Sem 6')
        total6 = 0
        total66 = 0
        for entry in Sem6:
            total6 = total6 + entry.creditsEarned
            total66 = total66 + entry.credits
        cpi_sem6 = 0
        if total66 > 0:
            cpi_sem6 = total6 / total66
        total_credits_earned += total6
        total_credits += total66
        spi_sem6 = 0
        if total_credits > 0:
            spi_sem6 = total_credits_earned / total_credits
        Sem7 = Grade.objects.filter(userProfile=user_id, semester='Sem 7')
        total7 = 0
        total77 = 0
        for entry in Sem7:
            total7 = total7 + entry.creditsEarned
            total77 = total77 + entry.credits
        cpi_sem7 = 0
        if total77 > 0:
            cpi_sem7 = total7 / total77
        total_credits_earned += total7
        total_credits += total77
        spi_sem7 = 0
        if total_credits > 0:
            spi_sem7 = total_credits_earned / total_credits
        Sem8 = Grade.objects.filter(userProfile=user_id, semester='Sem 8')
        total8 = 0
        total88 = 0
        for entry in Sem8:
            total8 = total8 + entry.creditsEarned
            total88 = total88 + entry.credits
        cpi_sem8 = 0
        if total88 > 0:
            cpi_sem8 = total8 / total88
        total_credits_earned += total8
        total_credits += total88
        spi_sem8 = 0
        if total_credits > 0:
            spi_sem8 = total_credits_earned / total_credits
        return render(request, 'grade.html', {
            'total_credits_earned': total_credits_earned,
            'total_credits': total_credits,
            'grades': grades,
            'cpi_sem1': cpi_sem1,
            'spi_sem1': spi_sem1,
            'Sem1': Sem1,
            'cpi_sem2': cpi_sem2,
            'spi_sem2': spi_sem2,
            'Sem2': Sem2,
            'cpi_sem3': cpi_sem3,
            'spi_sem3': spi_sem3,
            'Sem3': Sem3,
            'cpi_sem4': cpi_sem4,
            'spi_sem4': spi_sem4,
            'Sem4': Sem4,
            'cpi_sem5': cpi_sem5,
            'spi_sem5': spi_sem5,
            'Sem5': Sem5,
            'cpi_sem6': cpi_sem6,
            'spi_sem6': spi_sem6,
            'Sem6': Sem6,
            'cpi_sem7': cpi_sem7,
            'spi_sem7': spi_sem7,
            'Sem7': Sem7,
            'cpi_sem8': cpi_sem8,
            'spi_sem8': spi_sem8,
            'Sem8': Sem8,
        })

@login_required(login_url='login_page')
def addGrade(request):
    form = addPointer()
    if request.method == 'GET':
        return render(request, 'addGrade.html', {
            'form': form
        })
    else:
        form = addPointer(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.filter(id=user_id)
            code = form.cleaned_data.get('code')
            subject = form.cleaned_data.get('subject')
            credits = form.cleaned_data.get('credits')
            pointer = form.cleaned_data.get('pointer')
            semester = form.cleaned_data.get('semester')
            creditsEarned = credits*pointer
            new_grade = Grade.objects.create(
                userProfile= user[0],
                semester = semester,
                code = code,
                subject = subject,
                credits = credits,
                pointer = pointer,
                creditsEarned = creditsEarned,
            )
            new_grade.save()
            return redirect('grade')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('addGrade')

@login_required(login_url='login_page')
def editGrade(request):
    grade_id = request.GET.get('id')
    grade = Grade.objects.filter(id=grade_id)
    form = addPointer(initial={
        'semester': grade[0].semester,
        'code': grade[0].code,
        'subject': grade[0].subject,
        'credits': grade[0].credits,
        'pointer': grade[0].pointer,
    })
    if request.method == 'GET':
        return render(request, 'addGrade.html', {
            'form': form
        })
    else:
        form = addPointer(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.filter(id=user_id)
            code = form.cleaned_data.get('code')
            subject = form.cleaned_data.get('subject')
            credits = form.cleaned_data.get('credits')
            pointer = form.cleaned_data.get('pointer')
            semester = form.cleaned_data.get('semester')
            creditsEarned = credits * pointer
            updated_grade = grade.update(
                userProfile=user[0],
                semester=semester,
                code=code,
                subject=subject,
                credits=credits,
                pointer=pointer,
                creditsEarned=creditsEarned,
            )
            return redirect('grade')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('addGrade')


@login_required(login_url='login_page')
def deleteGrade(request):
    grade_id = request.GET.get('id')
    grade = Grade.objects.filter(id=grade_id)
    if request.method == 'GET':
        return render(request, 'deleteGrade.html', {
            'grade': grade[0],
        })
    else:
        grade.delete()
        return redirect('grade')



'''
def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html')
        
    elif request.method == 'POST':
        #form = event_registration_form(request.POST)
        #if form.is_valid():
        #    form.save()
        #    return HttpResponse("Saved")
        user_name = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        bio = request.POST['bio']
        univ = request.POST['univ']
        date = request.POST['date']
        prof = request.POST['prof']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        if Profile.objects.filter(UserName=request.POST['user_name']).exists():
            messages.error(request, "The username you entered is already taken")
            return render(request, 'registration/signup.html')
        user_info = Profile.objects.create(
            UserName = user_name,
            FirstName = first_name,
            LastName = last_name,
            Bio = bio,
            University = univ,
            DOB = date,
            Profession = prof,
            UserEmail = user_email,
            Password = user_password
        )
        user_info.save()
        return redirect('login_page')
'''



def welcome(request):
    return redirect('login_page')

