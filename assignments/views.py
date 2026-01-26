from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseForbidden
from assignments.utils import is_student
from .forms import AssignmentForm, AssignmentSubmissionForm   
from .models import Assignment, AssignmentSubmission
from django.contrib import messages
from classes.models import StudentProfile


@login_required
def assignment_list_view(request):
    user = request.user

    is_teacher = user.groups.filter(name='Teacher').exists()

    # Principal / superuser -> see all
    if user.is_superuser:
        assignments = Assignment.objects.filter(is_active=True)

    #teacher -> see only their assignments 
    elif user.groups.filter(name = 'Teacher').exists():
        assignments = Assignment.objects.filter(
            teacher = user,
            is_active=True
            )

    # student -> see their assignment for their class and section 
    elif user.groups.filter(name='Student').exists():
        try:
            student_profile = user.studentprofile
            assignments = Assignment.objects.filter(
            school_class=student_profile.school_class,
            section=student_profile.section,
            is_active=True
        )
        except:
            assignments = Assignment.objects.none()

    
    else: 
        assignments = Assignment.objects.none()
    
    return render(
        request,
        'assignments/assignment_list.html',
        {'assignments':assignments,
          'is_teacher': is_teacher
        }
    )

@login_required
def assignment_create_view(request):
    user = request.user

    # Only teachers can create assignments
    if not user.groups.filter(name='Teacher').exists():
        return HttpResponseForbidden("You do not have permission to create assignments.")

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = user
            assignment.save()
            messages.success(request, "Assignment created successfully.")
            return redirect('assignment-list')
    else:
        form = AssignmentForm()

    return render(
        request,
        'assignments/assignment_form.html',
        {'form': form}
    )

@login_required
def assignment_edit_view(request,pk):
    user = request.user
    assignment = Assignment.objects.get(pk=pk)

    # Only the teacher who created the assignment can edit it
    if not user.groups.filter(name='Teacher').exists():
        return HttpResponseForbidden("You do not have permission to edit assignments.")
    
    #teacher can only edit their own assignments
    if assignment.teacher != user:
        return HttpResponseForbidden("You can only edit your own assignments.")
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully.")
            return redirect("assignment-list")
    else:
        form = AssignmentForm(instance=assignment)
    
    return render(
        request,
        'assignments/assignment_form.html',
        {
            'form': form,
            'assignment': assignment
        }
    )

@login_required
def assignment_delete_view(request,pk):
    user = request.user
    assignment = Assignment.objects.get(pk=pk)

    if not user.groups.filter(name = 'Teacher').exists():
        return HttpResponseForbidden("You do not have permission to delete assignments.")
    
    if assignment.teacher != user:
        return HttpResponseForbidden("You can only delete your own assignments.")
    
    if request.method == 'POST':
        assignment.is_active = False
        assignment.save()
        messages.success(request, "Assignment deleted successfully.")
        return redirect('assignment-list')  
    
    return render(
        request,
        'assignments/assignment_confirm_delete.html',
        {'assignment': assignment}
    )

@login_required
def teacher_Assignment_submissions_view(request, pk):
    user = request.user

    # Only the teacher who created the assignment can view submissions
    if not user.groups.filter(name='Teacher').exists():
        return HttpResponseForbidden("You do not have permission to view submissions for this assignment.")

    assignment = get_object_or_404(Assignment, pk=pk, teacher=user, is_active=True)

    #all student in this class and section
    students = StudentProfile.objects.filter(
        school_class=assignment.school_class,
        section=assignment.section
    )
    
    #fetch submissions for this assignment
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)

    #map student_id to submissions 
    submissions_map = {submission.student_id: submission for submission in submissions}

    context = {
        'assignment':assignment,
        'students': students,
        'submissions_map': submissions_map
    }

    return render(
        request,
        'assignments/teacher_assignment_submissions.html',
        context
    )

# Student Views

@login_required
@user_passes_test(is_student)
def student_assignment_list(request):
    profile = request.user.studentprofile

    assignment = Assignment.objects.filter(
        school_class = profile.school_class,
        section = profile.section,
        is_active = True
    ).order_by('due_date')

    submitted_assignments_ids = AssignmentSubmission.objects.filter(
        student = request.user,
        is_submitted=True  # only consider submitted assignments
    ).values_list('assignment__id', flat=True)

    return render(
        request,
        "assignments/student_assignment_list.html",
        {'assignments': assignment,
         'submitted_assignments_ids': submitted_assignments_ids
        }
    )

@login_required
def student_assignment_detail(request, pk):
    user = request.user

    # only students can access this view
    if not user.groups.filter(name= 'Student').exists():
        return render(request, '403.html', status=403)
    
    student_profile = get_object_or_404(StudentProfile, user=user)

    assignment = get_object_or_404(
        Assignment,
        pk=pk,
        school_class=student_profile.school_class,
        section=student_profile.section,
        is_active=True
    )

    #check submission status
    submission, created = AssignmentSubmission.objects.get_or_create(
        assignment= assignment,
        student = request.user,
        defaults={'is_submitted': False} # set is_submitted to False if new submission is created
    )

    if request.method == 'POST':
        form = AssignmentSubmissionForm(
            request.POST, 
            request.FILES,
            instance=submission  # this added to handle edit submission without file
        )

        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.assignment = assignment
            new_submission.student = request.user
            new_submission.is_submitted = True # mark as submitted
            new_submission.save()
            messages.success(request, "Assignment submitted successfully.")
            return redirect('student-assignment-detail', 
                            pk=assignment.pk
                        )
    
    else:
        form = AssignmentSubmissionForm(instance=submission)

    context = {
        'assignment': assignment,
        'submission': submission,
        'form': form
    }


    return render(
        request,
        "assignments/student_assignment_detail.html",
        context
    )

