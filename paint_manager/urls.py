"""URLs specific to this project."""

from django.urls import path

from df_site.urls import urlpatterns
from paint_manager.views import PaintAddView, PaintDetailView

urlpatterns += [
    path("paint/<int:pk>/", PaintDetailView.as_view(), name="paint_detail"),
    path("paint/add/", PaintAddView.as_view(), name="paint_add"),
]
