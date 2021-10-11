from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer

# To make password encryption
from django.contrib.auth.hashers import make_password

# API view for django.contrib.auth.models.User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # it takes recent instance from serialzer and uses `make_password` to encrypt
    def perform_create(self, serializer):
    # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()
    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()
