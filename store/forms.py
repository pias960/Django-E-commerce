from django import forms

from.models import *

class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
      
        fields = '__all__'
        widgets = {
                'first_name': forms.TextInput(attrs={'class':'form-control pias'}),
                'last_name': forms.TextInput(attrs={'class':'form-control  pias'}),
                'street_address': forms.TextInput(attrs={'class':'form-control pias'}),
                'town_city': forms.TextInput(attrs={'class':'form-control  pias'}),
                'postcode_zip': forms.TextInput(attrs={'class':'form-control  pias'}),
                'notes': forms.TextInput(attrs={'class':'form-control pias', 'placeholder' : 'Enter the quantity here and descriptions'}),
                'phone': forms.TextInput(attrs={'class':'form-control  pias'}),
               
              
              }
        