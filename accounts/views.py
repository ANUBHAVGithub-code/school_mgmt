from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        group_name = request.POST.get("group")   # <-- FIXED

        user = User.objects.create_user(username=username, password=password)

        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return redirect('login')

    return render(request, "sign_up.html")
