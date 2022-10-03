from cProfile import label
from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField, UserChangeForm
from django.contrib.auth.models import User
from .models import Account, UserAddressBook
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class RegisterForm(UserCreationForm):
    password1=  forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(label='Password Again', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email= forms.CharField( error_messages={'invalid': 'This is an invalid  email.'}, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = Account      
        fields = {'email','first_name','last_name','username','phone_number'}
        widgets = {'first_name':forms.TextInput(attrs={'class':'form-control'}),
                  'last_name':forms.TextInput(attrs={'class':'form-control'}), 
                  'username':forms.TextInput(attrs={'class':'form-control'}),
                  'phone_number':forms.TextInput(attrs={'class':'form-control'})
                }


class AddressBookForm(forms.ModelForm):
    lname = forms.CharField(label= "Name", widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model= UserAddressBook
        fields = ( 'lname', 'phone','address', 'country','state','city', 'pincode')
        widgets = {'lname':forms.TextInput(attrs={'class':'form-control'}),
                  'phone':forms.TextInput(attrs={'class':'form-control'}), 
                  'address':forms.TextInput(attrs={'class':'form-control'}),
                  'country':forms.TextInput(attrs={'class':'form-control'}),
                  'state':forms.TextInput(attrs={'class':'form-control'}),
                  'city':forms.TextInput(attrs={'class':'form-control'}),
                  'pincode':forms.TextInput(attrs={'class':'form-control'}),}



class ProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields=('username', 'email', 'phone_number')
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'phone_number':forms.TextInput(attrs={'class':'form-control'})}

