from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Assignment, AssignmentSubmission

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        exclude = ('teacher', 'created_At','updated_At')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError(_("Title is required."))
        if len(title) < 5:
            raise forms.ValidationError(_("Title must be at least 5 characters long."))
        return title

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if not desc:
            raise forms.ValidationError(_("Description is required."))
        if len(desc) < 10:
            raise forms.ValidationError(_("Description must be at least 10 characters long."))
        return desc

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < timezone.now().date():
            raise forms.ValidationError(_("Due date cannot be in the past."))
        return due_date


class AssignmentSubmissionForm(forms.ModelForm):

    remove_file = forms.BooleanField(
        required=False,
        label=_("Remove existing file")
    )

    class Meta:
        model = AssignmentSubmission
        fields = ['file']
        widgets= {
            'file': forms.FileInput(attrs={'class':'form-control-file'})
        }
    
    def save(self, commit=True):
        submission = super().save(commit=False)

        if self.cleaned_data.get('remove_file'):
            if submission.file:
                submission.file.delete(save=False) # Delete the file from storage
            submission.file = None
        
        if commit:
            submission.save()
        return submission

