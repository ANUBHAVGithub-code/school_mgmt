from django.urls import path
from . import views

print("Assignments URLs loaded")
urlpatterns = [
    path('', views.assignment_list_view, name = 'assignment-list'),
    path('create/',views.assignment_create_view, name = 'assignment-create'),
    path('edit/<int:pk>/', views.assignment_edit_view, name = 'assignment-edit'),
    path('delete/<int:pk>/', views.assignment_delete_view, name = 'assignment-delete'),
    path("student/", views.student_assignment_list, name="student-assignment-list"),
    path("student/assignment/<int:pk>/", views.student_assignment_detail, name="student-assignment-detail"),
    path("student/assignment/<int:pk>/submissions/", views.teacher_Assignment_submissions_view, name="teacher-assignment-submissions-view"), 
]