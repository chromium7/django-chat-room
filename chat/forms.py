from django import forms
from django.contrib.auth.models import User

from .models import Room


class UserRegistrationForm(forms.ModelForm):
    """
    Form to create a new user accounts
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Password')
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, help_text='Repeat password')

    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email'}
        help_texts = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email'
        }
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.order_fields(['username', 'first_name', 'last_name', 'email'])


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class CreateRoomForm(forms.ModelForm):
    """
    Form to create a new room
    """
    class Meta:
        model = Room
        fields = {'name', 'password'}

    def __init__(self, *args, **kwargs):
        super(CreateRoomForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.order_fields(['name', 'password'])