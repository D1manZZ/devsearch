from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Message


class CreateUser(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password again')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'image', 'short_intro', 'bio', 'skills', 'social_linkedin',
                  'social_github', 'social_twitter', 'social_youtube', 'social_website']

    def __init__(self, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class SendMessage(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'message...'}), label='')

    class Meta:
        model = Message
        fields = ['text']
