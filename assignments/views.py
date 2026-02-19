from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseForbidden
from assignments.utils import is_student
from .forms import AssignmentForm, AssignmentSubmissionForm   
from .models import Assignment, AssignmentSubmission
from django.contrib import messages
from classes.models import StudentProfile
from django.core.cache import cache


@login_required
def assignment_list_view(request):
    user = request.user
    is_teacher = user.groups.filter(name='Teacher').exists()

    role = "principal" if user.is_superuser else "teacher" if is_teacher else "student"
    cache_key = f"assignment_list:{role}:{user.id}"

    cached_data = cache.get(cache_key)
    if cached_data:
        return render(request, 'assignments/assignment_list.html', cached_data)

    # Principal / superuser -> see all
    if user.is_superuser:
        assignments = Assignment.objects.filter(is_active=True)

    # Teacher -> see only their assignments 
    elif is_teacher:
        assignments = Assignment.objects.filter(teacher=user, is_active=True)

    # Student -> see their class assignments
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

    context = {
        'assignments': assignments,
        'is_teacher': is_teacher
    }

    cache.set(cache_key, context, timeout=300)

    return render(request, 'assignments/assignment_list.html', context)


@login_required
def assignment_create_view(request):
    user = request.user

    if not user.groups.filter(name='Teacher').exists():
        return HttpResponseForbidden("You do not have permission to create assignments.")

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = user
            assignment.save()

            cache.delete(f"assignment_list:teacher:{user.id}")

            messages.success(request, "Assignment created successfully.")
            return redirect('assignment-list')
    else:
        form = AssignmentForm()

    return render(request, 'assignments/assignment_form.html', {'form': form})


@login_required
def assignment_edit_view(request,pk):
    user = request.user
    assignment = Assignment.objects.get(pk=pk)

    if not user.groups.filter(name='Teacher').exists():
        return HttpResponseForbidden("You do not have permission to edit assignments.")
    
    if assignment.teacher != user:
        return HttpResponseForbidden("You can only edit your own assignments.")
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()

            cache.delete(f"assignment_list:teacher:{user.id}")
            cache.delete(f"teacher_submissions:{assignment.id}")

            messages.success(request, "Assignment updated successfully.")
            return redirect("assignment-list")
    else:
        form = AssignmentForm(instance=assignment)
    
    return render(request, 'assignments/assignment_form.html', {'form': form, 'assignment': assignment})


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

        cache.delete(f"assignment_list:teacher:{user.id}")
        cache.delete(f"teacher_submissions:{assignment.id}")

        messages.success(request, "Assignment deleted successfully.")
        return redirect('assignment-list')  
    
    return render(request, 'assignments/assignment_confirm_delete.html', {'assignment': assignment})


@login_required
def teacher_Assignment_submissions_view(request, pk):
    user = request.user

    if not user.groups.filter(name='Teacher').exists():
        return HttpResponseForbidden("You do not have permission to view submissions.")

    cache_key = f"teacher_submissions:{pk}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return render(request, 'assignments/teacher_assignment_submissions.html', cached_data)

    assignment = get_object_or_404(Assignment, pk=pk, teacher=user, is_active=True)

    students = StudentProfile.objects.filter(
        school_class=assignment.school_class,
        section=assignment.section
    )
    
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)

    submissions_map = {submission.student_id: submission for submission in submissions}

    context = {
        'assignment': assignment,
        'students': students,
        'submissions_map': submissions_map
    }

    cache.set(cache_key, context, timeout=300)

    return render(request, 'assignments/teacher_assignment_submissions.html', context)


# Student Views

@login_required
@user_passes_test(is_student)
def student_assignment_list(request):
    cache_key = f"student_assignment_list:{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return render(request, "assignments/student_assignment_list.html", cached_data)

    profile = request.user.studentprofile

    assignment = Assignment.objects.filter(
        school_class=profile.school_class,
        section=profile.section,
        is_active=True
    ).order_by('due_date')

    submitted_assignments_ids = AssignmentSubmission.objects.filter(
        student=request.user,
        is_submitted=True
    ).values_list('assignment__id', flat=True)

    context = {
        'assignments': assignment,
        'submitted_assignments_ids': submitted_assignments_ids
    }

    cache.set(cache_key, context, timeout=300)

    return render(request, "assignments/student_assignment_list.html", context)


@login_required
@user_passes_test(is_student)
def student_assignment_detail(request, pk):

    assignment = get_object_or_404(Assignment, pk=pk)

    submission, created = AssignmentSubmission.objects.get_or_create(
        assignment=assignment,
        student=request.user,
        defaults={'is_submitted': False}
    )

    form = AssignmentSubmissionForm(instance=submission)

    if request.method == "POST":

        old_file = submission.file

        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=submission)

        if form.is_valid():

            new_file = request.FILES.get('file')
            remove_file = request.POST.get('remove_file')

            submission_obj = form.save(commit=False)
            submission_obj.assignment = assignment
            submission_obj.student = request.user

            if remove_file and old_file and not new_file:
                old_file.delete(save=False)
                submission_obj.file = None

            elif new_file:
                if old_file:
                    old_file.delete(save=False)
                submission_obj.file = new_file

            submission_obj.is_submitted = True
            submission_obj.save()

            cache.delete(f"student_assignment_list:{request.user.id}")
            cache.delete(f"teacher_submissions:{assignment.id}")

            messages.success(request, "Submission updated successfully.")
            return redirect(request.path)

    return render(request, "assignments/student_assignment_detail.html", {
        "assignment": assignment,
        "submission": submission,
        "form": form,
    })
