from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.contrib import messages
from  .forms import *
from django.contrib.auth import *
from django.views import View
from store.models import Category
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages

from datetime import timedelta

from datetime import timedelta
from django.template.loader import render_to_string
from .forms import *
import random



def registration(request):
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    if request.user.is_authenticated:
        return redirect("Uhome")
    else:
        form = RegistrationForm()
        if request.method =='post' or request.method == 'POST':

            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'registreted succesfully')
                return redirect('success_page') 
            else:
                messages.error(request, 'Please correct the errors in the form.')
  
        else:
            form = RegistrationForm()  

    context = {'form': form,
               'cats': category, 
                'sub': subcategory
               }     
    return render(request, 'login/login.html',context)

def Userlogin(request):
    if request.user.is_authenticated:
        return redirect("Uhome")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_authenticated:  # Check if the user is authenticated
                otp_code = ''.join(random.choices('0123456789', k=6))  # Generate a 6-digit OTP code

                # Send OTP code via email
                subject = 'Your OTP Code'
                html_content = render_to_string('login/otp_email_templates.html', {'otp_code': otp_code})
                expiration_time = timezone.now() + timedelta(minutes=2)
                request.session['otp_expiration_time'] = expiration_time.strftime('%Y-%m-%d %H:%M:%S')
        
                send_mail(
                    subject,
                    'Verify your otp',
                    'pickashaw',
                    [user.email],
                    fail_silently=False,
                    html_message=html_content,
                )

                # Store OTP code in session
                request.session['otp_code'] = otp_code
                request.session['user_id'] = user.id  # Store user id in session
                return redirect('verify_otp')
            else:
                # Handle invalid login credentials
                # You may want to display an error message to the user
                pass
    return render(request, 'login/signin.html',)

def otp_confirmation(request):
    if request.user.is_authenticated:
        return redirect("Uhome")
    else:
        user_id = request.session.get('user_id')
        if user_id is None:
            return redirect('login')  # Redirect to login page if user_id is not found in session

        user = User.objects.get(pk=user_id)
        if request.method == 'POST':
            form = OTPConfirmationForm(request.POST)
            if form.is_valid():
                entered_otp_code = form.cleaned_data['otp_code']
                stored_otp_code = request.session.get('otp_code')
                if entered_otp_code == stored_otp_code:
                    # OTP code matches, authenticate user
                    login(request, user)
                    # Optionally, clear OTP code and user_id from session
                    del request.session['otp_code']
                    del request.session['user_id']
                    return redirect('Uhome')  # Redirect to home page after successful authentication
                else:
                    messages.error(request, 'OTP code does not match')
                   
        else:
            form = OTPConfirmationForm()
    return render(request, 'login/verify_otp.html', {'form': form})






#User login

# def userlogin(request):
#  category = Category.objects.filter(parent=None)
#  subcategory = Category.objects.exclude(parent=None)
#  if request.user.is_authenticated:
#      return redirect("Uhome")
#  else:
#     if request.method == "post" or request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         customer = authenticate(request, username=username, password=password)
#         if customer is not None:
#             login(request, customer)
#             subject = 'A new member logged in'
#             message = f' {request.user}, logged in!'
                
#             from_email = EMAIL_HOST_USER
#             recipient_list = ['mpias3721@gmail.com']
#             send_mail(subject, message, from_email, recipient_list)
#             return redirect('Uhome')
#         else:
#             messages.error(request, 'Invalid email or password')
#     return render(request, 'login/signin.html', {'cats': category, 
#         'sub': subcategory})
 

#  User Profile view 
class UpdateProfileView(View):
    def get(self,request):
        form = profileform(instance=request.user.profile)
        return render(request, "dashboard/UpdateProfile.html", {'form': form})
    def post(self, request):
        if request.method == "POST":
            form = profileform(request.POST, instance=request.user.profile)
            if form.is_valid():
                form.save()

                messages.success(request, 'Profile updated succesfully')
                return redirect('profile')
            else:
                messages.error(request, 'Something Wrong here')

        
        return render(request, 'dashboard/UpdateProfile.html', {'form': form})



def profile(request):
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    add = Profile.objects.filter(user=request.user)

    return render(request,'dashboard/profile.html', {'user' : add,'cats': category, 
        'sub': subcategory})

def Successpage(request):
   

    return render(request,'login/success.html')

from django.contrib.auth import logout
def custom_logout(request):
    logout(request)
    return redirect('login')