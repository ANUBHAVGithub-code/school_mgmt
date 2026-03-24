
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class LoginRecord(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _("%(username)s logged in at %(login_time)s") % {
            "username": self.user.username,
            "login_time": self.login_time,
        }
    
