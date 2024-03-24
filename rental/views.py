from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Rental
from .api.serializers import RentalSerializer


class RentalViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    User have CRUD operations on own objects.
    Staff have CRUD operation on all objects.
    """

    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["rental_start", "rental_end", "created"]
    ordering_fields = ["rental_start", "rental_end"]

    def get_queryset(self):
        user = self.request.user
        if user.is_active:
            return Rental.objects.all()
        else:
            return Rental.objects.filter(user=user)
