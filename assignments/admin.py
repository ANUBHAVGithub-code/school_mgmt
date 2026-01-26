from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'subject',
        'teacher',
        'school_class',
        'section',
        'due_date',
        'is_active',
    )