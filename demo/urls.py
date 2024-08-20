"""List of URLs for the demo app."""

from django.urls import path

from demo.views import DemoView, PopupDemoView, RibbonDetailView

urlpatterns = [
    path("demo/", DemoView.as_view(), name="demo"),
    path("ribbon/<int:pk>/", RibbonDetailView.as_view(), name="ribbon"),
    path("popup-demo/", PopupDemoView.as_view(), name="popup-demo"),
]
