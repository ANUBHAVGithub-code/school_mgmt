from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .permissions import IsPrincipal

class UserListAPIView(ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsPrincipal]