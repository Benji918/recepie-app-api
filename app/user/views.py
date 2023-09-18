"""Views for the user API"""

from rest_framework import generics
from .serializer import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the database"""
    serializer_class = UserSerializer
    