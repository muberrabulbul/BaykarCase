from category.models import Category
from django.http import Http404
from rest_framework.generics import ListAPIView

from django.shortcuts import redirect
from ihas.models import IHA
from ihas.api.serializers import IHASerializer

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from .serializers import CategorySerializer


from ihas.api.serializers import IHASerializer


@permission_classes((AllowAny,))
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes((AllowAny,))
class IHACategoryView(ListAPIView):
    # queryset = IHA.objects.filter(category__category=)
    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs["slug"]
        qs = IHA.objects.filter(category__slug=slug)
        if qs.exists():
            return qs
        else:
            return Http404

    serializer_class = IHASerializer
