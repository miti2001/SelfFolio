"""SelF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

#from django.contrib.auth import views as auth_views
from SelF import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', views.welcome, name='welcome'),
    url('', include("django.contrib.auth.urls")),
    path("signup/", views.signup, name="signup"),
    path('login_page/', views.login_func, name='login_page'),
    path('logout_page/', views.logout_func, name="logout_page"),
    path('home/', views.home, name='home'),
    path('profile/',views.profile, name='profile'),
    url('editProfile',views.editProfile, name='editProfile'),
    path('attendance/', views.attendance, name='attendance'),
    url('addSub/', views.addSub, name='addSub'),
    url('markAttendance/', views.markAttendance, name='markAttendance'),
    url('editSub', views.editSub, name='editSub'),
    url('deleteSub', views.deleteSub, name='deleteSub'),
    path('expense/', views.expense, name='expense'),
    url('addLog', views.addEntry, name='addLog'),
    url('editLog', views.editEntry, name='editLog'),
    url('deleteLog', views.deleteEntry, name='deleteLog'),
    path('grade/', views.grade, name='grade'),
    url('addGrade/', views.addGrade, name='addGrade'),
    url('editGrade/', views.editGrade, name='editGrade'),
    url('deleteGrade', views.deleteGrade, name='deleteGrade'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
