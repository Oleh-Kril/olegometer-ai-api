from django.urls import path
from .views import ImageURLView

urlpatterns = [
    path('compare/', ImageURLView.as_view(), name='compare'),
]
