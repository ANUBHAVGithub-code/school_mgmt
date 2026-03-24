from django.db import models
from django.contrib.auth.models import User
from classes.models import Class, Section
from django.conf import settings #this was added when we are working with custom user model for assignment submission
from django.utils.translation import gettext as _

class Assignment(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    subject = models.CharField(max_length= 100)

    teacher = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= "created_assignments"
    )

    school_class= models.ForeignKey(
        Class,
        on_delete= models.CASCADE
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    due_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_At = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.school_class} - {self.section})"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name = "submissions"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    file = models.FileField(upload_to='assignments/submissions/',blank=True,null=True) #blank and null added to add remove and edit submission without file
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('assignment', 'student')
    
    def __str__(self):
        return _("Submission of %(assignment)s by %(student)s") % {
            "assignment": self.assignment.title,
            "student": self.student.username,
        }
