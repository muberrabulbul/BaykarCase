from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Category
from .permissions import IsAdminUserOrReadOnly
from .api.serializers import CategorySerializer
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for staff
    and 'list' , 'retrieve' for any user.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filterset_fields = ["category"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "category",
    ]  # Specify the fields you want to search on

    def filter_queryset(self, queryset):
        filtered_queryset = super().filter_queryset(queryset)

        # Check if filtered_queryset is empty
        if not filtered_queryset.exists():
            raise NotFound(detail="No results found based on the applied filters.")

        return filtered_queryset
