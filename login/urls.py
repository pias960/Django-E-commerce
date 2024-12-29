from django.contrib import admin
from django.urls import path
from . import views
from .views import *
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import views as auth_view 
from django.contrib.auth.views import *
urlpatterns = [
  
    path('reg/', views.registration, name='register'),
    path('verify/', views.otp_confirmation, name='verify_otp'),

    ########login url###########
    path('login/', views.Userlogin, name='login'),

    ########profile url###########
    path("Update-profile/",UpdateProfileView.as_view(), name="update-profile"),

    path("profile/", views.profile, name="profile"),

     path("success/", views.Successpage, name="success_page"),



    ########logout url###########
    path('logout/', views.custom_logout, name='logout' ),


    ########password change done url###########
    path("passwordchangedone/", auth_view.PasswordChangeDoneView.as_view(template_name='dashboard/passwordchangedone.html'), 
         name="passswordchangedone"),

    ########password change url###########
    path('password_change/',login_required( auth_view.PasswordChangeView.as_view(template_name='dashboard/passwordchange.html',
              form_class=PasswordChangeForm, success_url='passswordchangedone')), name='passwordchange'),
    

    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='dashboard/passwordreset.html',
              form_class=passwordresetform, ), name='password-reset'),
            
    path("password_reset/done/", auth_view.PasswordResetDoneView.as_view(template_name='dashboard/passwordresetdone.html'), 
    name="password_reset_done"),


     path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='dashboard/passwordresetconfirm.html',
              form_class=setpasswordform, ), name='password_reset_confirm'),

     path("password_reset_complete/",               auth_view.PasswordResetCompleteView.as_view(template_name='dashboard/passwordresetcomplete.html'), 
    name="password_reset_complete"),
   

]
