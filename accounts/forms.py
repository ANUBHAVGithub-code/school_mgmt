from django import forms
from django.contrib.auth.models import User

ROLE_CHOICES  = [
    ('student','Student'),
    ('teacher','Seacher'),
    ('principal','Principal')
]

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username','email','password']