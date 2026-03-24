from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = (
    ("Principal", _("Principal")),
    ("Teacher", _("Teacher")),
    ("Student", _("Student")),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
