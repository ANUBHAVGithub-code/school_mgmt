from django import forms
from .models import Assignment, AssignmentSubmission

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        exclude = ('teacher', 'created_At','updated_At')

class AssignmentSubmissionForm(forms.ModelForm):

    remove_file = forms.BooleanField(
        required=False,
        label='Remove existing file'
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

