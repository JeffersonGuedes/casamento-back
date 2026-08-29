from django.urls import path
from .views import GuestCreateView

urlpatterns = [
    path('confirm/', GuestCreateView.as_view(), name='guest-confirm'),
]