from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  # student / teacher / principal

        if User.objects.filter(username = username).exists():
            return render(request,'sign_up.html',{'error':'username taken, choose another.'})

        user = User.objects.create_user(username=username, password=password)

        # Add user to selected role group
        group = Group.objects.get(name=role)
        user.groups.add(group)

        login(request, user)
        return redirect("home")

    return render(request, "sign_up.html")
