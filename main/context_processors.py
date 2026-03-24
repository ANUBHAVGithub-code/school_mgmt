def user_roles(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {
            "is_student": False,
            "is_teacher": False,
            "is_principal": False,
        }

    return {
        "is_student": user.groups.filter(name="Student").exists(),
        "is_teacher": user.groups.filter(name="Teacher").exists(),
        "is_principal": user.groups.filter(name="Principal").exists(),
    }
