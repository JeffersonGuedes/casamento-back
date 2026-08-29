from django.shortcuts import render
from rest_framework import generics
from .models import Guest
from .serializers import GuestSerializer

class GuestCreateView(generics.CreateAPIView):
    """
    Endpoint para o Next.js enviar o formulário de confirmação.
    Método permitido: POST
    """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer