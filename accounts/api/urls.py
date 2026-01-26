from django.urls import path
from .views import UserListAPIView

urlpatterns = [
    path('users/',UserListAPIView.as_view(),name= 'user_list'),
]

# this is where our backend officially became API backend
# here we wired our APIs