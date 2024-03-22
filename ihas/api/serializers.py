from rest_framework import serializers

from ihas.models import IHA, IHAPhoto
from category.models import Category
from category.api.serializers import CategorySerializer


class IHAPhotoSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializer to enable nesting in IHA serializer
    """

    class Meta:
        model = IHAPhoto
        fields = ["url", "iha", "photo"]
        extra_kwargs = {
            "iha": {"write_only": True},
        }


class IHASerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    photos = IHAPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = IHA
        fields = (
            "id",
            "title",
            "url",
            "brand",
            "category",
            "serial_number",
            "model",
            "weight",
            "engine",
            "year",
            "mileage",
            "location",
            "condition",
            "day_price",
            "photos",
        )

    def get_category(self, obj):
        response = CategorySerializer(obj.category).data
        return response
