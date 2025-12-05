from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Handle user management"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """ overide permission to allow strangers to register"""
        if self.action == 'create':
            return [AllowAny()]
        """ requre authenticated user to perform action"""
        """ requre authenticated user to perform action"""
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        return self.serializer_class

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(id=self.request.user.id).order_by('-id')

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me')
    def me(self, request):
        """Retrieve or update the authenticated user"""
        user = self.request.user
        serializer = self.get_serializer(user)

        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)




