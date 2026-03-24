from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import LoginRecord
from django.utils.translation import gettext as _


@login_required
def home(request):
    user = request.user

    # User groups (for display)
    user_groups = user.groups.values_list('name', flat=True)

    # Role checks (THIS FIXES YOUR TEMPLATE ERROR)
    is_teacher = user.groups.filter(name="Teacher").exists()
    is_principal = user.groups.filter(name="Principal").exists()

    # Login history
    login_records = LoginRecord.objects.filter(user=user).order_by('-login_time')
    last_login_record = login_records[1] if login_records.count() > 1 else None

    context = {
        "groups": list(user_groups),
        "last_login": last_login_record,
        "is_teacher": is_teacher,
        "is_principal": is_principal,
    }

    return render(request, "home.html", context)

# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username", "").strip()
#         email = request.POST.get("email", "").strip()
#         password = request.POST.get("password", "")
#         group_name = request.POST.get("group", "")
#
#         # Check if username exists first (case-sensitive)
#         if User.objects.filter(username=username).exists():
#             messages.error(request, f"Username '{username}' is already taken!")
#             return render(request, "sign_up.html", {
#                 "username": username,
#                 "email": email,
#                 "group": group_name
#             })
#
#         try:
#             user = User.objects.create_user(username=username, password=password, email=email)
#
#             # Assign group if selected
#             if group_name:
#                 group, created = Group.objects.get_or_create(name=group_name)
#                 user.groups.add(group)
#
#             messages.success(request, "Signup successful! Please login.")
#             return redirect("login")
#
#         except IntegrityError:
#             # Catch any duplicates that slipped through
#             messages.error(request, f"Username '{username}' is already taken!")
#             return render(request, "sign_up.html", {
#                 "username": username,
#                 "email": email,
#                 "group": group_name
#             })
#
#     # GET request
#     return render(request, "sign_up.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Clear any stale messages
            storage = messages.get_messages(request)
            for _ in storage:
                pass

            # Save login timestamp
            LoginRecord.objects.create(user=user)

            return redirect("home")
        else:
            messages.error(request, _("Invalid username or password"))

    return render(request, "log_in.html")


def logout_view(request):
    #messages.get_messages(request)  # Clear existing messages
    logout(request)
    return redirect("login")


# Templates render data.
# Views decide data.
