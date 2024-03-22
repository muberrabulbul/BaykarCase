from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import IHA, IHAPhoto
from .permissions import IsAdminUserOrReadOnly
from .api.serializers import IHAPhotoSerializer, IHASerializer


class IHAViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for staff
    and 'list' , 'retrieve' for any user.
    """

    queryset = IHA.objects.all()
    serializer_class = IHASerializer
    permission_classes = [IsAdminUserOrReadOnly]


class IHAPhotoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for staff
    """

    queryset = IHAPhoto.objects.all()
    serializer_class = IHAPhotoSerializer
    permission_classes = [IsAdminUser]
