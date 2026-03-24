from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES  = [
    ('student', _("Student")),
    ('teacher', _("Teacher")),
    ('principal', _("Principal"))
]

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    role = forms.ChoiceField(choices=ROLE_CHOICES, label=_("Role"))

    class Meta:
        model = User
        fields = ['username','email','password']

#never mind this just doing so to make changes in PR branch
