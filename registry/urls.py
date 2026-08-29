from django.urls import path
from .views import GiftListCreateView, ReserveGiftView

urlpatterns = [
    path('gifts/', GiftListCreateView.as_view(), name='gift-list'),
    path('gifts/<int:gift_id>/reserve/', ReserveGiftView.as_view(), name='gift-reserve'),
]