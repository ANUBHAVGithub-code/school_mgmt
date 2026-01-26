from django.contrib.auth.models import User
from rest_framework import serializers

#converts django models into JSON
#validates incoming data
#controls what fields are visible 

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'is_active',
            'date_joined',
        ]

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None
