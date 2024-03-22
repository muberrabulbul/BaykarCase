from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from django.http import Http404

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from ihas.models import IHA

from .serializers import IHASerializer


@permission_classes((AllowAny,))
class IHAListView(ListAPIView):
    queryset = IHA.objects.all()
    serializer_class = IHASerializer


@permission_classes((AllowAny,))
class IHADetail(RetrieveAPIView):
    serializer_class = IHASerializer
    lookup_field = ["slug", "id"]

    def get_object(self):
        slug = self.kwargs.get("slug")
        id_ = self.kwargs.get("id")
        iha_qs = IHA.objects.filter(slug=slug, id=id_)
        if not iha_qs.exists():
            raise Http404
        return iha_qs.first()
