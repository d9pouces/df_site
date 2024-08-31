"""URLs specific to this project."""

from django.urls import path

from df_site.urls import urlpatterns
from paint_manager.views import PaintAddView, PaintDetailView, UserPaintDeleteView, UserPaintUpdateView

urlpatterns += [
    path("paint/<int:pk>/", PaintDetailView.as_view(), name="paint_detail"),
    path("paint/add/<int:pk>/", PaintAddView.as_view(), name="paint_add"),
    path("paint/update/<int:pk>/", UserPaintUpdateView.as_view(), name="paint_update"),
    path("paint/delete/<int:pk>/", UserPaintDeleteView.as_view(), name="paint_delete"),
]
