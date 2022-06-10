from django import forms
from django.contrib.auth.models import User
from blogApp.models import AuthorProfile

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class UpdateProfileForm(forms.ModelForm):
    description = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = AuthorProfile
        fields = ['description']

