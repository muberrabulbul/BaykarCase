from datetime import date, datetime

from ihas.models import IHA
from ihas.api.serializers import IHASerializer
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Rental


class RentalSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for rental that serialize 'url', 'user',
    'rental_start', 'rental_end', 'created', 'updated',
    'rental_duration', 'total_price'
    and relation to iha serializer
    """

    url = serializers.HyperlinkedIdentityField(view_name="rentals-detail")
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    # Nested IHASerializer on read
    # iha = IHASerializer(read_only=True)

    # IHAField on write
    iha_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source="iha", queryset=IHA.objects.all(), label="IHA"
    )

    class Meta:
        model = Rental
        fields = [
            "url",
            "user",
            "iha_id",
            "rental_start",
            "rental_end",
            "created",
            "updated",
            "rental_duration",
            "total_price",
        ]
        extra_kwargs = {
            "rental_duration": {"read_only": True},
            "total_price": {"read_only": True},
        }

    def validate(self, data):
        """
        Ensures that user can not book a iha this is already booked
        in selected period
        """
        rental_start = data.get("rental_start")
        rental_end = data.get("rental_end")
        iha = data.get("iha")
        instance = self.instance

        # Requested rental ends during existing rental,
        # select sooner rental end date
        case_1 = Rental.objects.filter(
            iha=iha, rental_start__lte=rental_start, rental_end__gte=rental_start
        ).exists()
        # Requested rental starts during existing rental,
        # select later rental start date
        case_2 = Rental.objects.filter(
            iha=iha, rental_start__lte=rental_end, rental_end__gte=rental_end
        ).exists()
        # Requested rental starts and ends during existing rental
        case_3 = Rental.objects.filter(
            iha=iha, rental_start__gte=rental_start, rental_end__lte=rental_end
        ).exists()

        if not (instance and instance.iha == iha):
            if case_1:
                raise ValidationError(
                    """Requested rental ends during existing rental, \
                    select sooner rental end date"""
                )
            elif case_2:
                raise ValidationError(
                    "Requested rental starts during existing rental, \
                        select later rental start date"
                )
            elif case_3:
                raise ValidationError(
                    "Requested rental starts and ends during existing rental"
                )
            return data
        return data

    def validate_rental_start(self, value):
        """
        Ensures that the earlies possible rental start day is today
        """
        rental_start = value
        today_value = timezone.now().today().date()
        if rental_start < today_value:
            raise ValidationError(
                f"Rental start date must be greater than {today_value}"
            )
        return super(RentalSerializer, self).validate(value)

    def validate_rental_end(self, value):
        """
        Ensures that rental end date can not be before rental start date
        """
        data = self.get_initial()
        rental_start = data.get("rental_start")
        rental_start = datetime.strptime(rental_start, "%Y-%m-%d").date()
        rental_end = value
        if rental_end < rental_start:
            raise ValidationError(
                "Rental end date must be greater than rental start date"
            )
        return super(RentalSerializer, self).validate(value)

    def save(self, **kwargs):
        """
        Include default for read_only `user` field
        """
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)
