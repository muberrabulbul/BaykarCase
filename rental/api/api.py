from rental.models import Rental
from django.http import Http404
from rest_framework.generics import ListAPIView

from ihas.models import IHA
from ihas.api.serializers import IHASerializer

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from .serializers import RentalSerializer


@permission_classes((AllowAny,))
class RentalListView(ListAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


@permission_classes((AllowAny,))
class IHARentalView(ListAPIView):
    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs["slug"]
        qs = IHA.objects.filter(rental__slug=slug)
        if qs.exists():
            return qs
        else:
            return Http404

    serializer_class = IHASerializer
