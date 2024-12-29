from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm,SetPasswordForm, PasswordResetForm
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'name'}),
            'email': forms.EmailInput(attrs={'class':'email'}),
            'password1': forms.PasswordInput(attrs={'class':'pass1'}),
            'password2': forms.PasswordInput(attrs={'class':'pass2'}),
        }
      
class profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'address', 'country', 'city', 'zip', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control pias'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'country': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'zip': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            
            }
        labels = {
            'full_name': 'Full Name',
            'address': 'Address',
            'country': 'Country',
            'city': 'City',
            'zip': 'Zip',
            'phone': 'Phone',
            }

class passwordChangeForm(PasswordChangeForm):
    PasswordChangeForm.base_fields['old_password'].widget.attrs['class'] = 'form-control'
    PasswordChangeForm.base_fields['new_password1'].widget.attrs['class'] = 'form-control'
    PasswordChangeForm.base_fields['new_password2'].widget.attrs['class'] = 'form-control'
    
class setpasswordform(SetPasswordForm):
    PasswordChangeForm.base_fields['new_password1'].widget.attrs['class'] = 'form-control'
    PasswordChangeForm.base_fields['new_password2'].widget.attrs['class'] = 'form-control'
    
class passwordresetform(PasswordResetForm):
    PasswordResetForm.base_fields['email'].widget.attrs['class'] = 'form-control'


class OTPConfirmationForm(forms.Form):
    otp_code = forms.CharField(label='OTP Code', max_length=6)

