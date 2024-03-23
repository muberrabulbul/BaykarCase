from io import BytesIO
import uuid

from django.core.files.base import ContentFile
from django.db import models
from category.models import Category

from PIL import Image


class IHA(models.Model):
    CONDITION = (
        ("used", "used"),
        ("new", "new"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    brand = models.CharField(max_length=40)
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    engine = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    mileage = models.DecimalField(max_digits=6, decimal_places=0)
    location = models.CharField(max_length=50)
    condition = models.CharField(max_length=50, choices=CONDITION)
    day_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{}".format(self.title)


class IHAPhoto(models.Model):
    iha = models.ForeignKey(IHA, related_name="photos", on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True, upload_to="photos")
