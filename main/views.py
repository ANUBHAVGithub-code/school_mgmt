from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User, Group
from .models import LoginRecord

@login_required
def home(request):
    user_groups = request.user.groups.values_list('name', flat = True)
    login_record = LoginRecord.objects.filter(user = request.user).order_by('-login_time')
    last_login_record = login_record[1] if login_record.count() >1 else None
    return render(request, 'home.html',{"groups":list(user_groups),"last_login":last_login_record})

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)

            #save login timestamp
            LoginRecord.objects.create(user = user)

            return redirect("home")
        else:
            messages.error(request, "invalid username or password")
        
    return render(request, "log_in.html")

def logout_view(request):
    logout(request)
    return redirect("login")
