from django.urls import path

from .api import CategoryListView, IHACategoryView

urlpatterns = [
    path("list/", CategoryListView.as_view()),
    path("iha-filter/<str:slug>/", IHACategoryView.as_view()),
]
