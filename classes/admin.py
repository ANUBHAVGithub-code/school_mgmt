from django.contrib import admin
from .models import Class,Section, StudentProfile
# Register your models here.

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_class')
    list_filter = ('school_class',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_class', 'section')
    list_filter = ('school_class', 'section')