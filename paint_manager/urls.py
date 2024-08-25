"""URLs specific to this project."""

from django.urls import path

from paint_manager.views import PaintDetailView

urlpatterns = [
    path("paint/<int:pk>/", PaintDetailView.as_view(), name="paint_detail"),
]
