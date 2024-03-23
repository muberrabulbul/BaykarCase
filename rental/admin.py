from django.contrib import admin

from .models import Rental


class RentalAdmin(admin.ModelAdmin):
    list_display = ("user", "iha", "rental_start", "rental_end")


admin.site.register(Rental, RentalAdmin)
