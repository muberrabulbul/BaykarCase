from ihas.models import IHA
from django.contrib.auth.models import User
from django.db import models


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    iha = models.ForeignKey(IHA, on_delete=models.CASCADE)
    rental_start = models.DateField()
    rental_end = models.DateField()
    rental_duration = models.DecimalField(max_digits=3, decimal_places=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        self.rental_duration = (self.rental_end - self.rental_start).days
        self.total_price = self.rental_duration * self.iha.day_price
        super(Rental, self).save(*args, **kwargs)
