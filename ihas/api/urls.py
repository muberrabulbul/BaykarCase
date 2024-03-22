from django.urls import path

from .api import (
    IHAListView,
    IHADetail,
)

urlpatterns = [
    path("list-view/", IHAListView.as_view()),
    path("<uuid:id>/detail-view/<str:slug>/", IHADetail.as_view()),
]
