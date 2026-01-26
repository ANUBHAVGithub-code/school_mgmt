from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=10)
    school_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name= 'sections'
    )

    def __str__(self):
        return f"{self.school_class} - {self.name}"

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='studentprofile'
    )

    school_class = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.school_class} - {self.section}"