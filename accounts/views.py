from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import IntegrityError

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        group_name = request.POST.get("group", "")

        # Check if username exists first (case-sensitive)
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken!")
            return render(request, "sign_up.html", {
                "username": username,
                "email": email,
                "group": group_name
            })

        try:
            user = User.objects.create_user(username=username, password=password, email=email)

            # Assign group if selected
            if group_name:
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)

            messages.success(request, "Signup successful! Please login.")
            return redirect("login")

        except IntegrityError:
            # Catch any duplicates that slipped through
            messages.error(request, f"Username '{username}' is already taken!")
            return render(request, "sign_up.html", {
                "username": username,
                "email": email,
                "group": group_name
            })

    # GET request
    return render(request, "sign_up.html")