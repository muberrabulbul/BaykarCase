from django.urls import path

from .api import RentalListView, IHARentalView

urlpatterns = [
    path("list/", RentalListView.as_view()),
    path("iha-filter/<str:slug>/", IHARentalView.as_view()),
]
