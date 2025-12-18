from django.urls import path, include
from .views import signup_view

urlpatterns = [
    path('signup/',signup_view, name = 'signup'),
    path('api/', include('accounts.api.urls')),
]