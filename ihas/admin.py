from django.contrib import admin
from .models import IHA, IHAPhoto


class IHAPhotoInline(admin.StackedInline):
    model = IHAPhoto


class IHAAdmin(admin.ModelAdmin):
    inlines = [IHAPhotoInline]


admin.site.register(IHA, IHAAdmin)
