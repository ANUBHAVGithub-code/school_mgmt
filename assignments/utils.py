def is_student(user):
    return user.groups.filter(name='Student').exists()

#this is a little helper function to check if a user is a student